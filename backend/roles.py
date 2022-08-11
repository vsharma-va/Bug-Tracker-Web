import json
from flask import render_template, request
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
    all_users_ids = helper.get_all_users(project_name)
    lst_all_users = [helper.get_user_name_by_user_id(int(x.strip())) for x in all_users_ids.split(',')]
    lst_all_users_ids = [int(x.strip()) for x in all_users_ids.split(',')]
    project_id = helper.get_projectid_by_project_name(project_name)
    all_user_roles_in_order = [helper.get_users_current_role_in_project(project_id, user_id) for user_id in lst_all_users_ids]
    return render_template('roles/role.html', project_name=project_name, all_roles=all_roles, all_users=lst_all_users, user_roles_in_order=all_user_roles_in_order)

@bp.route('/roles/<project_name>/updateUserRoles', methods=['POST'])
@login_required
def update_user_roles(project_name):
    # check if current users role changed and store that in cookies again
    if request.method == 'POST':
        data = request.get_json(force=True)
        helper = CrudHelper(db.get_db())
        project_id = helper.get_projectid_by_project_name(project_name)
        for key in data:
            user_id = helper.get_user_id_by_user_name(key)
            helper.update_user_roles(user_id, project_id, data[key])
        return json.dumps({'html': render_template('helper/flash_messages.html', flash_color="flash-green", message="Roles updated successfully !"), 'status': 'success'})
    return 'only accessible through post request'