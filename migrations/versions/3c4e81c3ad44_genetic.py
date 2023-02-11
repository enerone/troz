"""genetic

Revision ID: 3c4e81c3ad44
Revises: 5ec296379818
Create Date: 2023-02-10 19:08:30.658127

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3c4e81c3ad44'
down_revision = '5ec296379818'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('genetic',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('bank_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('genealogy', sa.String(length=100), nullable=True),
    sa.Column('parent1_id', sa.Integer(), nullable=True),
    sa.Column('parent2_id', sa.Integer(), nullable=True),
    sa.Column('flowering_time', sa.Integer(), nullable=True),
    sa.Column('ratio', sa.String(length=100), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['bank_id'], ['bank.id'], ),
    sa.ForeignKeyConstraint(['parent1_id'], ['genetic.id'], ),
    sa.ForeignKeyConstraint(['parent2_id'], ['genetic.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('genetic')
    # ### end Alembic commands ###