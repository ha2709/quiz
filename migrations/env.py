"""
Environment configuration for Alembic migrations.
This module sets up the database connection and manages migration contexts.
"""

import os
import sys
from logging.config import fileConfig

from alembic import context  # pylint: disable=no-member
from dotenv import load_dotenv
from sqlalchemy import engine_from_config, pool

from src.models import Base  # Adjust the import path as necessary

# from src.models import participant, question, quiz, user

# Load environment variables from .env
load_dotenv()

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config  # pylint: disable=no-member


# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


# Import your models
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


target_metadata = Base.metadata

# Retrieve synchronous database URL from environment variables
DATABASE_URL_SYNC = os.getenv("DATABASE_URL_SYNC")


def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = DATABASE_URL_SYNC
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        {"sqlalchemy.url": DATABASE_URL_SYNC},
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
