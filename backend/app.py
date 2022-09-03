import dashboard as dashboard
import auth as auth
import project as project
import db as db
import roles as roles
from flask import Flask, redirect, url_for
from flask_wtf.csrf import session
import os
from dotenv import load_dotenv

'''
    can integrate github api to show recent commits and changes
'''

load_dotenv()

extra_dirs = [
    "../frontend/html"
]

extra_files = extra_dirs[:]
for extra_dir in extra_dirs:
    for dirname, dirs, files in os.walk(extra_dir):
        for filename in files:
            filename = os.path.join(dirname, filename)
            if os.path.isfile(filename):
                extra_files.append(filename)

app = Flask(__name__, template_folder="../frontend/html",
            static_folder='../frontend/static/')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
# app.config['SECRET_KEY'] = '755203b56dc7dccc4d7ee10503232e31'
app.config['TEMPLATES_AUTO_RELOAD'] = True
db.init_app(app)

@app.route('/')
def checkUserStatus():
    try:
        session['user_id']
        return redirect(url_for('dashboard.dash'))
    except KeyError:
        return redirect(url_for('auth.register'))

app.register_blueprint(auth.bp)
app.register_blueprint(dashboard.bp)
app.register_blueprint(project.bp)
app.register_blueprint(roles.bp)

if __name__ == '__main__':
    app.run(debug=True, threaded=True, extra_files=extra_files)