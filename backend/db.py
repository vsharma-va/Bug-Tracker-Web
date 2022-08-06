import os
import click
from flask.cli import with_appcontext
from flask_wtf.csrf import current_app, g
from urllib.parse import urlparse
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

def get_db():
    if 'db' not in g:
        uri = os.getenv('DATABASE_URL')
        if uri and uri.startswith("postgres://"):
            uri = uri.replace("postgres://", "postgresql://", 1)
        engine = create_engine(uri)
        g.db = scoped_session(sessionmaker(bind=engine))
        g.db.autocommit = True
    return g.gb
    # conn_str = os.environ.get('DATABASE_URI')
    # url = urlparse(conn_str)
    # if 'db' not in g:
    #     g.db =psycopg2.connect(
    #         dbname = url.path[1:],
    #         user=url.username,
    #         password=url.password,
    #         host=url.hostname,
    #         port=5432
    #     )
    #     g.db.autocommit = True
    # return g.db

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
