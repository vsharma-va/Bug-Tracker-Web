from crypt import methods
from flask import render_template, request
from flask_wtf.csrf import Blueprint, session
from sqlalchemy import true

import db
from auth import login_required
from dashboard_helpers.dashboard_helper import DashHelper

bp = Blueprint('dashboard', __name__, url_prefix='/authorised')

@bp.route('/dash', methods=["GET", "POST"])
@login_required
def dash():
    html_details = {}
    if request.method == "POST":
        data = request.get_json(force=True)
        filter_type = data['type']
        project_name = data['project_name']
        helper = DashHelper(db.get_db())
        user_id = session['user_id']
        html_details = helper.get_project_cards(f"{filter_type.lower()}", user_id, project_name)
        session['html_details'] = html_details
        session['details_for_filter'] = {'filter_type': filter_type, 'project_name': project_name}
        return f'/authorised/filtered?{filter_type}'
    else:
        helper = DashHelper(db.get_db())
        user_id = session['user_id']
        html_details = helper.get_project_cards("all", user_id)
        return render_template('dashboard.html', dict_keys=list(html_details.keys()), value=html_details)

@bp.route('/filtered/<filter_type>', methods=["GET", "POST"])
@login_required
def filtered(filter_type):
    html_details = session['html_details']
    session['filter_type'] = filter_type
    return render_template('dashboard.html', dict_keys=list(html_details.keys()), value=html_details)

@bp.route('/filtered/type/fetch', methods=['GET', 'POST'])
@login_required
def filter_type_fetch():
    details = session['details_for_filter']
    return str([details['filter_type'], details['project_name']])