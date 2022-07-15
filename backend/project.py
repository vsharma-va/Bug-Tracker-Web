from flask import render_template, request
from flask_wtf.csrf import Blueprint, session
from helper.crud_helper import CrudHelper, Status

import db
from auth import login_required

bp = Blueprint('project', __name__, url_prefix='/authorised/dash')


@bp.route('/main/<project_name>')
@login_required
def project_details_page(project_name):
    helper = CrudHelper(db.get_db())
    data_dict = {}
    for status in Status:
        html_details = helper.get_project_cards_by_project_name(
            project_name, status)
        data_dict[status.value] = html_details
    data_dict = CrudHelper.order_and_sub_username(data_dict, False)
    return render_template('project/project_main.html', data=data_dict)
