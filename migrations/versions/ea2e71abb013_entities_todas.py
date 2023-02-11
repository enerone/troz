"""entities todas

Revision ID: ea2e71abb013
Revises: 
Create Date: 2023-02-11 18:06:13.358163

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ea2e71abb013'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('bank',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('qr', sa.String(length=255), nullable=True),
    sa.Column('name', sa.String(length=70), nullable=True),
    sa.Column('phone', sa.String(length=20), nullable=True),
    sa.Column('contact_name', sa.String(length=100), nullable=True),
    sa.Column('comments', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('employee',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('qr', sa.String(length=255), nullable=True),
    sa.Column('supervisor', sa.Integer(), nullable=True),
    sa.Column('state', sa.String(length=50), nullable=True),
    sa.Column('first_name', sa.String(length=50), nullable=True),
    sa.Column('last_name', sa.String(length=100), nullable=True),
    sa.Column('address', sa.String(length=100), nullable=True),
    sa.Column('phone', sa.String(length=100), nullable=True),
    sa.Column('birthdate', sa.DateTime(), nullable=True),
    sa.Column('notifications_profile_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['notifications_profile_id'], ['notification.id'], ),
    sa.ForeignKeyConstraint(['supervisor'], ['employee.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('line',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('qr', sa.String(length=255), nullable=True),
    sa.Column('x_axix_qty', sa.Integer(), nullable=True),
    sa.Column('y_axix_qty', sa.Integer(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('notification',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('employee_id', sa.Integer(), nullable=True),
    sa.Column('type', sa.String(length=50), nullable=True),
    sa.Column('message', sa.String(length=255), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('priority', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['employee_id'], ['employee.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('room',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('qr', sa.String(length=255), nullable=True),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('type', sa.String(length=50), nullable=True),
    sa.Column('size', sa.Float(), nullable=True),
    sa.Column('state', sa.String(length=50), nullable=True),
    sa.Column('max_plants', sa.Integer(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('about_me', sa.String(length=140), nullable=True),
    sa.Column('last_seen', sa.DateTime(), nullable=True),
    sa.Column('token', sa.String(length=32), nullable=True),
    sa.Column('token_expiration', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_user_email'), ['email'], unique=True)
        batch_op.create_index(batch_op.f('ix_user_token'), ['token'], unique=True)
        batch_op.create_index(batch_op.f('ix_user_username'), ['username'], unique=True)

    op.create_table('cycle',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('qr', sa.String(length=255), nullable=True),
    sa.Column('room_id', sa.Integer(), nullable=True),
    sa.Column('start_date', sa.DateTime(), nullable=True),
    sa.Column('end_date', sa.DateTime(), nullable=True),
    sa.Column('type', sa.String(length=50), nullable=True),
    sa.Column('plants_qty', sa.Integer(), nullable=True),
    sa.Column('comments', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['room_id'], ['room.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('followers',
    sa.Column('follower_id', sa.Integer(), nullable=True),
    sa.Column('followed_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['followed_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['follower_id'], ['user.id'], )
    )
    op.create_table('genetic',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('qr', sa.String(length=255), nullable=True),
    sa.Column('bank_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('genealogy', sa.String(length=100), nullable=True),
    sa.Column('parent1_id', sa.Integer(), nullable=True),
    sa.Column('parent2_id', sa.Integer(), nullable=True),
    sa.Column('flowering_days', sa.Integer(), nullable=True),
    sa.Column('ratio', sa.String(length=100), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['bank_id'], ['bank.id'], ),
    sa.ForeignKeyConstraint(['parent1_id'], ['genetic.id'], ),
    sa.ForeignKeyConstraint(['parent2_id'], ['genetic.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('body', sa.String(length=140), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('language', sa.String(length=5), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_post_timestamp'), ['timestamp'], unique=False)

    op.create_table('spot',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('qr', sa.String(length=255), nullable=True),
    sa.Column('room_id', sa.Integer(), nullable=True),
    sa.Column('line_id', sa.Integer(), nullable=True),
    sa.Column('coor_x', sa.Integer(), nullable=True),
    sa.Column('coord_y', sa.Integer(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['line_id'], ['line.id'], ),
    sa.ForeignKeyConstraint(['room_id'], ['room.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('germoplasm',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('qr', sa.String(length=255), nullable=True),
    sa.Column('genetic_id', sa.Integer(), nullable=True),
    sa.Column('format', sa.String(length=50), nullable=True),
    sa.Column('start_date', sa.DateTime(), nullable=True),
    sa.Column('comments', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['genetic_id'], ['genetic.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('plant',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('qr', sa.String(length=255), nullable=True),
    sa.Column('cycle_id', sa.Integer(), nullable=True),
    sa.Column('genetic_id', sa.Integer(), nullable=True),
    sa.Column('germoplasm_id', sa.Integer(), nullable=True),
    sa.Column('spot_id', sa.Integer(), nullable=True),
    sa.Column('trimmer_id', sa.Integer(), nullable=True),
    sa.Column('start_date', sa.DateTime(), nullable=True),
    sa.Column('end_date', sa.DateTime(), nullable=True),
    sa.Column('plants_qty', sa.Integer(), nullable=True),
    sa.Column('comments', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['cycle_id'], ['cycle.id'], ),
    sa.ForeignKeyConstraint(['genetic_id'], ['genetic.id'], ),
    sa.ForeignKeyConstraint(['germoplasm_id'], ['germoplasm.id'], ),
    sa.ForeignKeyConstraint(['spot_id'], ['spot.id'], ),
    sa.ForeignKeyConstraint(['trimmer_id'], ['employee.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('bitacora',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('plant_id', sa.Integer(), nullable=True),
    sa.Column('cycle_id', sa.Integer(), nullable=True),
    sa.Column('room_id', sa.Integer(), nullable=True),
    sa.Column('title', sa.String(length=255), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['cycle_id'], ['cycle.id'], ),
    sa.ForeignKeyConstraint(['plant_id'], ['plant.id'], ),
    sa.ForeignKeyConstraint(['room_id'], ['room.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('multimedia',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('plant_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('url', sa.String(length=100), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['plant_id'], ['plant.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('multimedia')
    op.drop_table('bitacora')
    op.drop_table('plant')
    op.drop_table('germoplasm')
    op.drop_table('spot')
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_post_timestamp'))

    op.drop_table('post')
    op.drop_table('genetic')
    op.drop_table('followers')
    op.drop_table('cycle')
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_username'))
        batch_op.drop_index(batch_op.f('ix_user_token'))
        batch_op.drop_index(batch_op.f('ix_user_email'))

    op.drop_table('user')
    op.drop_table('room')
    op.drop_table('notification')
    op.drop_table('line')
    op.drop_table('employee')
    op.drop_table('bank')
    # ### end Alembic commands ###