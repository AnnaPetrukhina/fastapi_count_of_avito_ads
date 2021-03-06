"""empty message

Revision ID: eff378f8268f
Revises: 14fb48bfc0ef
Create Date: 2020-12-04 12:04:17.563617

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eff378f8268f'
down_revision = '14fb48bfc0ef'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_params_id', table_name='params')
    op.drop_table('params')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('params',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('region', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('query', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='params_pkey')
    )
    op.create_index('ix_params_id', 'params', ['id'], unique=False)
    # ### end Alembic commands ###
