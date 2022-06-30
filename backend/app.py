from flask import Flask;

app = Flask(__name__, template_folder="../frontend/html", static_folder='../frontend/static/')
app.config['SECRET_KEY'] = '755203b56dc7dccc4d7ee10503232e31'
import db
db.init_app(app)
import auth
app.register_blueprint(auth.bp)
