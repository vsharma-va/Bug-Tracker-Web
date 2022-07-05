import dashboard
import auth
import db
from flask import Flask
import os


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
app.config['SECRET_KEY'] = '755203b56dc7dccc4d7ee10503232e31'
app.config['TEMPLATES_AUTO_RELOAD'] = True
db.init_app(app)
app.register_blueprint(auth.bp)
app.register_blueprint(dashboard.bp)

if __name__ == '__main__':
    app.run(threaded=True, extra_files=extra_files)