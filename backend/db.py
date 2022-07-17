import click
from flask.cli import with_appcontext
from flask_wtf.csrf import current_app, g
import psycopg2


def get_db():
    if 'db' not in g:
        g.db = psycopg2.connect(
            host='localhost',
            database="Bug-Tracker",
            user="postgres",
            password="Ihatepassword"
        )
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
