"""Add min_combined_karma column

Revision ID: 0dd06194add3
Revises: 1e13ad86bf0d
Create Date: 2019-05-02 21:20:45.265064

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0dd06194add3'
down_revision = '1e13ad86bf0d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('raffle', sa.Column('min_combined_karma', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('raffle', 'min_combined_karma')
    # ### end Alembic commands ###
