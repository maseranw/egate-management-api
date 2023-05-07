"""make changes to database

Revision ID: 16a65f59a08c
Revises: 
Create Date: 2023-05-01 23:10:10.116505

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '16a65f59a08c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cars',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('make', sa.String(), nullable=True),
    sa.Column('model', sa.String(), nullable=True),
    sa.Column('year', sa.String(), nullable=True),
    sa.Column('code', sa.Numeric(), nullable=True),
    sa.Column('create_date', sa.DateTime(), nullable=True),
    sa.Column('update_date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_cars_code'), 'cars', ['code'], unique=False)
    op.create_index(op.f('ix_cars_create_date'), 'cars', ['create_date'], unique=False)
    op.create_index(op.f('ix_cars_id'), 'cars', ['id'], unique=False)
    op.create_index(op.f('ix_cars_make'), 'cars', ['make'], unique=False)
    op.create_index(op.f('ix_cars_model'), 'cars', ['model'], unique=False)
    op.create_index(op.f('ix_cars_update_date'), 'cars', ['update_date'], unique=False)
    op.create_index(op.f('ix_cars_year'), 'cars', ['year'], unique=False)
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('password', sa.String(), nullable=True),
    sa.Column('create_date', sa.DateTime(), nullable=True),
    sa.Column('update_date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_create_date'), 'users', ['create_date'], unique=False)
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_update_date'), 'users', ['update_date'], unique=False)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_table('visitors',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('phone', sa.String(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('car_id', sa.Integer(), nullable=True),
    sa.Column('create_date', sa.DateTime(), nullable=True),
    sa.Column('update_date', sa.DateTime(), nullable=True),
    sa.Column('check_in_time', sa.DateTime(), nullable=True),
    sa.Column('check_out_time', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_visitors_car_id'), 'visitors', ['car_id'], unique=False)
    op.create_index(op.f('ix_visitors_check_in_time'), 'visitors', ['check_in_time'], unique=False)
    op.create_index(op.f('ix_visitors_check_out_time'), 'visitors', ['check_out_time'], unique=False)
    op.create_index(op.f('ix_visitors_create_date'), 'visitors', ['create_date'], unique=False)
    op.create_index(op.f('ix_visitors_id'), 'visitors', ['id'], unique=False)
    op.create_index(op.f('ix_visitors_phone'), 'visitors', ['phone'], unique=False)
    op.create_index(op.f('ix_visitors_update_date'), 'visitors', ['update_date'], unique=False)
    op.create_index(op.f('ix_visitors_user_id'), 'visitors', ['user_id'], unique=False)
    op.create_table('tokens',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('visitor_id', sa.Integer(), nullable=True),
    sa.Column('code', sa.Numeric(), nullable=True),
    sa.Column('create_date', sa.DateTime(), nullable=True),
    sa.Column('update_date', sa.DateTime(), nullable=True),
    sa.Column('expiry_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['visitor_id'], ['visitors.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tokens_code'), 'tokens', ['code'], unique=True)
    op.create_index(op.f('ix_tokens_create_date'), 'tokens', ['create_date'], unique=False)
    op.create_index(op.f('ix_tokens_expiry_date'), 'tokens', ['expiry_date'], unique=False)
    op.create_index(op.f('ix_tokens_id'), 'tokens', ['id'], unique=False)
    op.create_index(op.f('ix_tokens_update_date'), 'tokens', ['update_date'], unique=False)
    op.create_index(op.f('ix_tokens_visitor_id'), 'tokens', ['visitor_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_tokens_visitor_id'), table_name='tokens')
    op.drop_index(op.f('ix_tokens_update_date'), table_name='tokens')
    op.drop_index(op.f('ix_tokens_id'), table_name='tokens')
    op.drop_index(op.f('ix_tokens_expiry_date'), table_name='tokens')
    op.drop_index(op.f('ix_tokens_create_date'), table_name='tokens')
    op.drop_index(op.f('ix_tokens_code'), table_name='tokens')
    op.drop_table('tokens')
    op.drop_index(op.f('ix_visitors_user_id'), table_name='visitors')
    op.drop_index(op.f('ix_visitors_update_date'), table_name='visitors')
    op.drop_index(op.f('ix_visitors_phone'), table_name='visitors')
    op.drop_index(op.f('ix_visitors_id'), table_name='visitors')
    op.drop_index(op.f('ix_visitors_create_date'), table_name='visitors')
    op.drop_index(op.f('ix_visitors_check_out_time'), table_name='visitors')
    op.drop_index(op.f('ix_visitors_check_in_time'), table_name='visitors')
    op.drop_index(op.f('ix_visitors_car_id'), table_name='visitors')
    op.drop_table('visitors')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_update_date'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_index(op.f('ix_users_create_date'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_cars_year'), table_name='cars')
    op.drop_index(op.f('ix_cars_update_date'), table_name='cars')
    op.drop_index(op.f('ix_cars_model'), table_name='cars')
    op.drop_index(op.f('ix_cars_make'), table_name='cars')
    op.drop_index(op.f('ix_cars_id'), table_name='cars')
    op.drop_index(op.f('ix_cars_create_date'), table_name='cars')
    op.drop_index(op.f('ix_cars_code'), table_name='cars')
    op.drop_table('cars')
    # ### end Alembic commands ###
