"""Enterprise optimizations: indexes, user_id on claim_records, timestamp on velocity_records

Revision ID: 20260829000000
Revises: 20260802000000
Create Date: 2026-08-29
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine.reflection import Inspector

revision = '20260829000000'
down_revision = '20260802000000'
branch_labels = None
depends_on = None


def _table_has_column(conn, table: str, column: str) -> bool:
    inspector = Inspector.from_engine(conn)
    return any(c["name"] == column for c in inspector.get_columns(table))


def _index_exists(conn, index: str) -> bool:
    inspector = Inspector.from_engine(conn)
    for table in inspector.get_table_names():
        if any(ix["name"] == index for ix in inspector.get_indexes(table)):
            return True
    return False


def upgrade():
    conn = op.get_bind()

    # ── claim_records: add user_id ────────────────────────────
    if not _table_has_column(conn, "claim_records", "user_id"):
        op.add_column(
            "claim_records",
            sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=True),
        )

    # ── velocity_records: add timestamp alias ────────────────
    if not _table_has_column(conn, "velocity_records", "timestamp"):
        op.add_column(
            "velocity_records",
            sa.Column("timestamp", sa.DateTime(), nullable=True),
        )
        # Back-fill from created_at
        op.execute(
            "UPDATE velocity_records SET timestamp = created_at WHERE timestamp IS NULL"
        )

    # ── New composite indexes ─────────────────────────────────
    indexes = [
        ("ix_claim_records_user_created",    "claim_records",    ["user_id", "created_at"]),
        ("ix_claim_records_verdict_created", "claim_records",    ["verdict", "created_at"]),
        ("ix_claim_records_hash_idx",        "claim_records",    ["claim_hash"]),
        ("ix_velocity_records_ts",           "velocity_records", ["timestamp"]),
    ]
    for idx_name, table, cols in indexes:
        if not _index_exists(conn, idx_name):
            op.create_index(idx_name, table, cols)


def downgrade():
    conn = op.get_bind()

    for idx_name in [
        "ix_claim_records_user_created",
        "ix_claim_records_verdict_created",
        "ix_claim_records_hash_idx",
        "ix_velocity_records_ts",
    ]:
        if _index_exists(conn, idx_name):
            op.drop_index(idx_name)

    if _table_has_column(conn, "velocity_records", "timestamp"):
        op.drop_column("velocity_records", "timestamp")

    if _table_has_column(conn, "claim_records", "user_id"):
        op.drop_column("claim_records", "user_id")
