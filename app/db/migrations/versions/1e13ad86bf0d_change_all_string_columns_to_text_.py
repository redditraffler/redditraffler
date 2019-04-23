"""Change all string columns to text columns

Revision ID: 1e13ad86bf0d
Revises: 6e2f1d9ef98c
Create Date: 2019-04-21 22:07:23.455182

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "1e13ad86bf0d"
down_revision = "6e2f1d9ef98c"
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column("user", "username", type_=sa.TEXT)

    op.alter_column("raffle", "submission_id", type_=sa.TEXT)
    op.alter_column("raffle", "submission_title", type_=sa.TEXT)
    op.alter_column("raffle", "submission_author", type_=sa.TEXT)
    op.alter_column("raffle", "subreddit", type_=sa.TEXT)

    op.alter_column("winner", "username", type_=sa.TEXT)
    op.alter_column("winner", "comment_url", type_=sa.TEXT)


def downgrade():
    op.alter_column("user", "username", type_=sa.String(512))

    op.alter_column("raffle", "submission_id", type_=sa.String(512))
    op.alter_column("raffle", "submission_title", type_=sa.String(512))
    op.alter_column("raffle", "submission_author", type_=sa.String(512))
    op.alter_column("raffle", "subreddit", type_=sa.String(512))

    op.alter_column("winner", "username", type_=sa.String(512))
    op.alter_column("winner", "comment_url", type_=sa.String(512))
