"""Phase 1: Add persistent fact memory tables (pgvector RAG foundation)

Adds:
  - pgvector extension (enables vector similarity search)
  - fact_checks table (persistent memory of every qualified fact-check)
  - evidence_documents table (persistent evidence corpus with embeddings)
  - fact_check_evidence table (many-to-many join with relevance scores)

Revision ID: 20260830000000
Revises: 20260829000000
Create Date: 2026-08-30
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine.reflection import Inspector

revision      = '20260830000000'
down_revision = '20260829000000'
branch_labels = None
depends_on    = None


def _table_exists(conn, table: str) -> bool:
    return table in Inspector.from_engine(conn).get_table_names()


def _index_exists(conn, index: str) -> bool:
    inspector = Inspector.from_engine(conn)
    for tbl in inspector.get_table_names():
        if any(ix["name"] == index for ix in inspector.get_indexes(tbl)):
            return True
    return False


def upgrade():
    conn = op.get_bind()

    # ── Enable pgvector extension (idempotent) ────────────────
    try:
        op.execute("CREATE EXTENSION IF NOT EXISTS vector")
    except Exception:
        pass  # Already exists or not supported — fallback to Text columns

    # ── fact_checks ───────────────────────────────────────────
    if not _table_exists(conn, "fact_checks"):
        op.create_table(
            "fact_checks",
            sa.Column("id",                   sa.Integer,     primary_key=True),
            sa.Column("claim_hash",           sa.String(64),  nullable=False, unique=True),
            sa.Column("claim_text",           sa.Text,        nullable=False),
            sa.Column("normalized_claim",     sa.Text,        nullable=True),
            # Vector column — stored as text if pgvector unavailable
            sa.Column("embedding",            sa.Text,        nullable=True),

            sa.Column("verdict",              sa.String(16),  nullable=False),
            sa.Column("confidence",           sa.Float,       nullable=False),
            sa.Column("verification_status",  sa.String(20),
                       nullable=False, server_default="model_only"),

            sa.Column("ml_score_a",           sa.Float,       nullable=True),
            sa.Column("ml_score_b",           sa.Float,       nullable=True),
            sa.Column("tfidf_score",          sa.Float,       nullable=True),
            sa.Column("llm_verdict",          sa.String(16),  nullable=True),
            sa.Column("llm_confidence",       sa.Float,       nullable=True),
            sa.Column("evidence_score",       sa.Float,       nullable=True),
            sa.Column("manipulation_score",   sa.Float,       nullable=True),
            sa.Column("rag_assessment",       sa.Text,        nullable=True),

            sa.Column("language",             sa.String(8),
                       nullable=True, server_default="en"),
            sa.Column("topic",                sa.String(64),  nullable=True),
            sa.Column("entities",             sa.Text,        nullable=True),
            sa.Column("model_version",        sa.String(32),  nullable=True),

            sa.Column("created_at",           sa.DateTime,
                       nullable=True, server_default=sa.func.now()),
            sa.Column("updated_at",           sa.DateTime,
                       nullable=True, server_default=sa.func.now()),
        )
        op.create_index("ix_fact_checks_claim_hash",      "fact_checks", ["claim_hash"])
        op.create_index("ix_fact_checks_verdict",         "fact_checks", ["verdict"])
        op.create_index("ix_fact_checks_status",          "fact_checks", ["verification_status"])
        op.create_index("ix_fact_checks_created_at",      "fact_checks", ["created_at"])
        op.create_index("ix_fact_checks_verdict_status",  "fact_checks",
                         ["verdict", "verification_status"])
        op.create_index("ix_fact_checks_topic_created",   "fact_checks",
                         ["topic", "created_at"])

    # ── evidence_documents ────────────────────────────────────
    if not _table_exists(conn, "evidence_documents"):
        op.create_table(
            "evidence_documents",
            sa.Column("id",           sa.Integer,      primary_key=True),
            sa.Column("url",          sa.String(2048), nullable=False, unique=True),
            sa.Column("title",        sa.Text,         nullable=True),
            sa.Column("content",      sa.Text,         nullable=True),
            sa.Column("domain",       sa.String(256),  nullable=True),
            sa.Column("embedding",    sa.Text,         nullable=True),

            sa.Column("stance",       sa.String(16),   nullable=True),
            sa.Column("trust_score",  sa.Float,
                       nullable=True, server_default="0.5"),
            sa.Column("bias_label",   sa.String(32),   nullable=True),
            sa.Column("source_tier",  sa.Integer,
                       nullable=True, server_default="4"),
            sa.Column("source_type",  sa.String(32),   nullable=True),

            sa.Column("published_at", sa.DateTime,     nullable=True),
            sa.Column("retrieved_at", sa.DateTime,
                       nullable=True, server_default=sa.func.now()),
        )
        op.create_index("ix_ed_url",              "evidence_documents", ["url"])
        op.create_index("ix_ed_domain",           "evidence_documents", ["domain"])
        op.create_index("ix_ed_stance",           "evidence_documents", ["stance"])
        op.create_index("ix_ed_source_tier",      "evidence_documents", ["source_tier"])
        op.create_index("ix_ed_published_at",     "evidence_documents", ["published_at"])
        op.create_index("ix_ed_stance_tier",      "evidence_documents",
                         ["stance", "source_tier"])
        op.create_index("ix_ed_domain_published", "evidence_documents",
                         ["domain", "published_at"])

    # ── fact_check_evidence ───────────────────────────────────
    if not _table_exists(conn, "fact_check_evidence"):
        op.create_table(
            "fact_check_evidence",
            sa.Column("id",                    sa.Integer, primary_key=True),
            sa.Column("fact_check_id",         sa.Integer,
                       sa.ForeignKey("fact_checks.id"), nullable=False),
            sa.Column("evidence_document_id",  sa.Integer,
                       sa.ForeignKey("evidence_documents.id"), nullable=False),
            sa.Column("relevance_score",       sa.Float,   nullable=True),
            sa.Column("stance",                sa.String(16), nullable=True),
        )
        op.create_index("ix_fce_fact_check_id",   "fact_check_evidence", ["fact_check_id"])
        op.create_index("ix_fce_evidence_id",     "fact_check_evidence", ["evidence_document_id"])

    # ── Upgrade embedding columns to native vector type (if pgvector available) ──
    # Try to ALTER the embedding columns to vector(384).
    # If pgvector is not installed, this silently skips — Text fallback is used.
    try:
        op.execute(
            "ALTER TABLE fact_checks ALTER COLUMN embedding TYPE vector(384) "
            "USING embedding::vector(384)"
        )
        op.execute(
            "ALTER TABLE evidence_documents ALTER COLUMN embedding TYPE vector(384) "
            "USING embedding::vector(384)"
        )
        # Create IVFFlat index for approximate nearest-neighbour search
        # lists=100 is appropriate for up to ~1M vectors
        op.execute(
            "CREATE INDEX IF NOT EXISTS ix_fact_checks_embedding_ivfflat "
            "ON fact_checks USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100)"
        )
        op.execute(
            "CREATE INDEX IF NOT EXISTS ix_evidence_embedding_ivfflat "
            "ON evidence_documents USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100)"
        )
    except Exception:
        # pgvector not available — Text fallback remains, app handles serialization
        pass


def downgrade():
    conn = op.get_bind()
    for table in ["fact_check_evidence", "evidence_documents", "fact_checks"]:
        if _table_exists(conn, table):
            op.drop_table(table)
