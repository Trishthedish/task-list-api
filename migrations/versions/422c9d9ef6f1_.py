"""empty message

Revision ID: 422c9d9ef6f1
Revises: 3fa3879e3bef
Create Date: 2021-06-09 23:09:36.907328

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '422c9d9ef6f1'
down_revision = '3fa3879e3bef'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('goal', sa.Column('title', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('goal', 'title')
    # ### end Alembic commands ###
