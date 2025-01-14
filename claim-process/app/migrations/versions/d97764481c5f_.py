"""

Revision ID: d97764481c5f
Revises: 
Create Date: 2025-01-14 20:40:05.056828

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'd97764481c5f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('claim',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('service_date', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('submitted_procedure', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('quadrant', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('plan_group', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('subscriber', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('provider_npi', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('provider_fees', sa.Float(), nullable=False),
    sa.Column('allowed_fees', sa.Float(), nullable=False),
    sa.Column('member_coinsurance', sa.Float(), nullable=False),
    sa.Column('member_copay', sa.Float(), nullable=False),
    sa.Column('net_fee', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('claim')
    # ### end Alembic commands ###