import logging
import time
from logging.config import fileConfig
from typing import Any

from flask import current_app
from sqlalchemy import MetaData
from sqlalchemy.engine import Engine

from alembic import context
from app.models.base import Base

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)
logger = logging.getLogger("alembic.env")


def get_engine() -> Engine:
    try:
        # this works with Flask-SQLAlchemy<3 and Alchemical
        return current_app.extensions["migrate"].db.get_engine()
    except (TypeError, AttributeError):
        # this works with Flask-SQLAlchemy>=3
        return current_app.extensions["migrate"].db.engine


def get_engine_url() -> str:
    try:
        engine_url = get_engine().url.render_as_string(hide_password=False)
        return str(engine_url.replace("%", "%%"))
    except AttributeError:
        return str(get_engine().url).replace("%", "%%")


target_metadata = Base.metadata

config.set_main_option("sqlalchemy.url", get_engine_url())
target_db = current_app.extensions["migrate"].db

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def get_metadata() -> MetaData:
    return target_metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=get_metadata(), literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    # this callback is used to prevent an auto-migration from being generated
    # when there are no changes to the schema
    # reference: http://alembic.zzzcomputing.com/en/latest/cookbook.html
    def process_revision_directives(
        context: Any, revision: Any, directives: Any
    ) -> None:
        if getattr(config.cmd_opts, "autogenerate", False):
            script = directives[0]
            if script.upgrade_ops.is_empty():
                directives[:] = []
                logger.info("No changes in schema detected.")

    conf_args = current_app.extensions["migrate"].configure_args
    if conf_args.get("process_revision_directives") is None:
        conf_args["process_revision_directives"] = process_revision_directives

    connectable = get_engine()

    # Retry connection logic for Vitess
    max_retries = 3
    for attempt in range(max_retries):
        try:
            with connectable.connect() as connection:
                context.configure(
                    connection=connection, target_metadata=get_metadata(), **conf_args
                )

                with context.begin_transaction():
                    context.run_migrations()
                return
        except Exception as e:
            if attempt < max_retries - 1:
                warning_msg = f"Connection attempt {attempt + 1} failed, retrying..."
                logger.warning(warning_msg)
                time.sleep(2)
            else:
                error_msg = f"Failed to connect after {max_retries} attempts: {e}"
                logger.error(error_msg)
                raise


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
