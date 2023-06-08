"""Database module for the application."""
import sqlite3
from flask import g, current_app
import click


def get_db():
    """Returns a database connection, creating one if it doesn't exist."""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(current_app.config['DATABASE'])
        db.row_factory = sqlite3.Row
    return db


def close_db(e=None):
    """Closes the database connection."""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def init_db():
    """Initializes the database."""
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
def init_db_command():
    """Initialize the database."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    """Initializes the application."""
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
