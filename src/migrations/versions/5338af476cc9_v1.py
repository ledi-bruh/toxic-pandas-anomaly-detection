"""v1

Revision ID: 5338af476cc9
Revises:
Create Date: 2024-08-30 20:35:24.525058

"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5338af476cc9'
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute('create schema anomaly')

    op.create_table(
        'anomaly_detections',
        sa.Column('timestamp', sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column('valves', sa.Float(), nullable=False),
        sa.Column('pumps', sa.Float(), nullable=False),
        sa.Column('fans', sa.Float(), nullable=False),
        sa.Column('slide', sa.Float(), nullable=False),
        sa.PrimaryKeyConstraint('timestamp', name=op.f('pk_anomaly_detections')),
        schema='anomaly',
    )


def downgrade() -> None:
    op.drop_table('anomaly_detections', schema='anomaly')
