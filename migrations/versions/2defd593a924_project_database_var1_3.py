"""project database var1_3

Revision ID: 2defd593a924
Revises: c310f4b44874
Create Date: 2020-05-05 16:05:20.345939

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '2defd593a924'
down_revision = 'c310f4b44874'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('events', 'datetime')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('events', sa.Column('datetime', postgresql.TIMESTAMP(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###