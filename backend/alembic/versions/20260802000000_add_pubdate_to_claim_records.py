# Copyright 2027 Bodapati Bharat Chandra. All rights reserved.
# Licensed under the Apache License, Version 2.0
# SPDX-License-Identifier: Apache-2.0
"""add pub_date to claim_records

Item 82: pub_date as model input for temporal claim validity.
Stores the publication date of the source article so the system
can understand time-dependent claims (e.g., "X is president").

Revision ID: 20260802000000
Revises: 20260417174717
Create Date: 2026-08-02
"""
from alembic import op
import sqlalchemy as sa

revision = '20260802000000'
down_revision = '20260417174717'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'claim_records',
        sa.Column('pub_date', sa.DateTime(), nullable=True)
    )
    op.create_index('ix_claim_records_pub_date', 'claim_records', ['pub_date'])


def downgrade():
    op.drop_index('ix_claim_records_pub_date', table_name='claim_records')
    op.drop_column('claim_records', 'pub_date')
