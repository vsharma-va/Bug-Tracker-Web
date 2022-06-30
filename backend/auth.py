import functools
from flask import flash, redirect, render_template, url_for
from flask_wtf.csrf import Blueprint, request, session
from auth_form import RegisterationForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf.csrf import g

import db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterationForm(request.form)
    if request.method == 'POST' and form.validate():
        conn = db.get_db()
        cursor = conn.cursor()
        username = request.form['email']
        password = request.form['password']
        try:
            print("Inserting user")
            cursor.execute(
                    "INSERT INTO cUser (username, password) VALUES (%s, %s)",
                    [username, generate_password_hash(password)],
                    )
            return redirect(url_for("auth.home"))
        except:
            flash("Hello there you have encountered a bug")
    return render_template('registeration.html', title='Register', form=form)

@bp.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        conn = db.get_db()
        cursor = conn.cursor()
        username = request.form['email']
        password = request.form['password']
        cursor.execute(
                "SELECT * FROM cUser where username = %s",
                [username]
                )
        user = cursor.fetchone()
        if user != None:
            if check_password_hash(user[2], password):
                session.clear()
                session['user_id'] = user[0]
                return redirect(url_for('auth.home'))
            else:
                flash("Wrong Password")
                # form.password.errors =list(form.password.errors).append('Wrong Password')
        else:
            # form.email.errors + ('No usernames found',)
            flash("Wrong Password")
    return render_template('login.html', title='Login', form=form)

# runs before every view is loaded
@bp.before_app_request
def check_user_status():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        conn = db.get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cUser WHERE id = %s", [user_id])
        g.user = cursor.fetchone()

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        print(g.user)
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view

@bp.route("/home")
@login_required
def home():
    return "<h1> welcome </h1>"


