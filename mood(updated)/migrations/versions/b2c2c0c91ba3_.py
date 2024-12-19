"""empty message

Revision ID: b2c2c0c91ba3
Revises: 35e8bb7d86c0
Create Date: 2024-12-18 19:53:06.233715

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b2c2c0c91ba3'
down_revision = '35e8bb7d86c0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('preferred_genre', sa.String(length=100), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('preferred_genre')

    # ### end Alembic commands ###
