"""project database ver1_4

Revision ID: a0283619aaea
Revises: 2defd593a924
Create Date: 2020-05-08 00:09:00.693628

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a0283619aaea'
down_revision = '2defd593a924'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###

    op.create_table('bets',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('amount', sa.Float(), nullable=False),
    sa.Column('win_sum', sa.Float(), nullable=True),
    sa.Column('user_fk', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_fk'], ['users.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('events',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=1000), nullable=False),
    sa.Column('coefficient', sa.Float(), nullable=False),
    sa.Column('match_fk', sa.Integer(), nullable=False),
    sa.Column('outcome_fk', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['match_fk'], ['matches.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['outcome_fk'], ['possible_outcomes.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_roles',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('role_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'role_id')
    )
    op.create_table('bet_details',
    sa.Column('bet_fk', sa.Integer(), nullable=False),
    sa.Column('event_fk', sa.Integer(), nullable=False),
    sa.Column('outcome_fk', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['bet_fk'], ['bets.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['event_fk'], ['events.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['outcome_fk'], ['possible_outcomes.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('bet_fk', 'event_fk', 'outcome_fk')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('bet_details')
    op.drop_table('user_roles')
    op.drop_table('events')
    op.drop_table('bets')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_table('roles')
    op.drop_table('possible_outcomes')
    op.drop_table('matches')
    # ### end Alembic commands ###
