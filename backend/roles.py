from flask import render_template
from flask_wtf.csrf import Blueprint

import db
from auth import login_required
from helper.crud_helper import CrudHelper


bp = Blueprint('user_roles', __name__, url_prefix='/authorised/dash')

@bp.route('/roles/<project_name>')
@login_required
def roles_page(project_name):
    helper = CrudHelper(db.get_db())
    all_roles = helper.get_all_project_roles(project_name)
    return render_template('roles/role.html', project_name=project_name, all_roles=all_roles)