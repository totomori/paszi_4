"""create users table

Revision ID: 20250101_create_users_table
Revises:
Create Date: 2025-01-01 12:00:00
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "20250101_create_users_table"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("login", sa.String(length=50), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_unique_constraint("uq_users_login", "users", ["login"])


def downgrade():
    op.drop_constraint("uq_users_login", "users", type_="unique")
    op.drop_table("users")
