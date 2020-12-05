"""empty message

Revision ID: 61d9d71d59ad
Revises: 0a25273bc1f0
Create Date: 2020-12-05 10:22:45.022615

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '61d9d71d59ad'
down_revision = '0a25273bc1f0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_params_id', table_name='params')
    op.drop_column('params', 'id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('params', sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False))
    op.create_index('ix_params_id', 'params', ['id'], unique=False)
    # ### end Alembic commands ###