import sqlite3

import click

from flask import current_app
from flask import g
from flask.cli import with_appcontext

def get_db():
    """
    The global context is accessed to understand if 'db' has been registered.
    """
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db

# What is the e argument used for...?
def close_db(e=None):
    """Remove the database from the global app context."""
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    """initializes the database using the schema"""
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

@click.command('init-db')
@with_appcontext
def init_db_command():
    """
    Define what we do as a result of the command line argument to make the
    database.

    Call with: flask init-db

    This action will delete all resident data and recreate the tables by
    calling the init_db function defined above.
    """

    init_db()
    click.echo("Initialized the database")

def init_app(app):
    """
    Given an app instance, register functions used to interact with the app
    """

    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
