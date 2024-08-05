import os

from alembic import context
from app.models import Base
from sqlalchemy import create_engine

# config = context.config
DATABASE_URL = os.getenv(
    "USER_ALEMBIC_DB_URL",
    "postgresql://agendable:agendable@localhost:5432/user_db",
)
connectable = create_engine(DATABASE_URL)


def run_migrations_online():
    """Run migrations in 'online' mode with an established connection."""
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=Base.metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    raise Exception("Offline mode not supported here")
else:
    run_migrations_online()
