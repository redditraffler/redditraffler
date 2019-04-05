"""Transfer IgnoredUser data to a column in Raffle

Revision ID: 9cfa830d9291
Revises: dc43d91dc18a
Create Date: 2019-03-28 21:32:08.078232

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from collections import defaultdict

# revision identifiers, used by Alembic.
revision = '9cfa830d9291'
down_revision = 'dc43d91dc18a'
branch_labels = None
depends_on = None


def upgrade():
    # Create new column for Raffles
    op.add_column('raffle', sa.Column('ignored_users', sa.TEXT, nullable=True))

    # Fetch all ignored_users
    db_conn = op.get_bind()
    rows = db_conn.execute('SELECT raffle_id, username FROM ignored_user').fetchall()

    # Group ignored users by raffle ID
    ignored_users_by_raffle_id = defaultdict(list)
    for raffle_id, username in rows:
        ignored_users_by_raffle_id[raffle_id].append(username)

    # CSV-ify ignored users and set column value in Raffle
    for raffle_id, ignored_users in ignored_users_by_raffle_id.items():
        ignored_users_str = ','.join(ignored_users)
        db_conn.execute(
            sa.text(
                "UPDATE raffle SET ignored_users = :ignored_users_str WHERE raffle.id = :raffle_id"),
            ignored_users_str=ignored_users_str,
            raffle_id=raffle_id
        )


def downgrade():
    op.drop_column('raffle', 'ignored_users')
