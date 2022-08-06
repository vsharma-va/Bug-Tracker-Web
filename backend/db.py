import os
import click
from flask.cli import with_appcontext
from flask_wtf.csrf import current_app, g
from urllib.parse import urlparse
import psycopg2

def get_db():
    conn_str = os.environ.get('DATABASE_URI')
    pa = urlparse(conn_str)
    if 'db' not in g:
        connection_dict = {
            'dbname': pa.hostname,
            'user': pa.username,
            'password': pa.password,
            'port': pa.port,
            'host': pa.scheme,
        }
        g.db = psycopg2.connect(**connection_dict)
        g.db.autocommit = True
    return g.db

def close_db(e=None):
    db = g.pop('db', None)  # None if db doesn't exist
    if db is not None:
        db.close()


def init_db():
    db = get_db()
    cursor = db.cursor()
    cursor.execute(open("schema.sql", "r").read())


@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    # this calls the close_db function when everything is shutting down
    app.teardown_appcontext(close_db)
    # this allows this function to be called from the terminal
    app.cli.add_command(init_db_command)
