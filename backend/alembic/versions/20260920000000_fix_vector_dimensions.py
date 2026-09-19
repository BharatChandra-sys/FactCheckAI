"""Fix vector dimensions from 380 to 384

Revision ID: 20260920000000
Revises: 20260830000000
Create Date: 2026-09-20
"""
from alembic import op
import sqlalchemy as sa

revision = '20260920000000'
down_revision = '20260830000000'
branch_labels = None
depends_on = None


def upgrade():
    # Drop existing indexes
    op.execute("DROP INDEX IF EXISTS ix_fact_checks_embedding_ivfflat")
    op.execute("DROP INDEX IF EXISTS ix_evidence_embedding_ivfflat")
    
    # Alter vector columns to correct dimension (384)
    try:
        op.execute(
            "ALTER TABLE fact_checks ALTER COLUMN embedding TYPE vector(384) "
            "USING embedding::vector(384)"
        )
        op.execute(
            "ALTER TABLE evidence_documents ALTER COLUMN embedding TYPE vector(384) "
            "USING embedding::vector(384)"
        )
    except Exception:
        # If casting fails (wrong dimension), drop and recreate
        op.execute("ALTER TABLE fact_checks ALTER COLUMN embedding TYPE text")
        op.execute("ALTER TABLE fact_checks ALTER COLUMN embedding TYPE vector(384) USING NULL")
        
        op.execute("ALTER TABLE evidence_documents ALTER COLUMN embedding TYPE text")
        op.execute("ALTER TABLE evidence_documents ALTER COLUMN embedding TYPE vector(384) USING NULL")
    
    # Recreate indexes with correct dimension
    op.execute(
        "CREATE INDEX ix_fact_checks_embedding_ivfflat "
        "ON fact_checks USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100)"
    )
    op.execute(
        "CREATE INDEX ix_evidence_embedding_ivfflat "
        "ON evidence_documents USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100)"
    )


def downgrade():
    # No downgrade - we don't want to go back to wrong dimensions
    pass
