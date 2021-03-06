"""empty message

Revision ID: 0a25273bc1f0
Revises: 41480d7a9dd4
Create Date: 2020-12-05 10:19:32.251440

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0a25273bc1f0'
down_revision = '41480d7a9dd4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_params_id'), 'params', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_params_id'), table_name='params')
    # ### end Alembic commands ###
