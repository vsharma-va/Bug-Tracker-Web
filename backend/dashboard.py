from cgitb import html
from crypt import methods
from flask import render_template, request
from flask_wtf.csrf import Blueprint, session
from sqlalchemy import true

import db
from auth import login_required
from dashboard_helpers.dashboard_helper import DashHelper

bp = Blueprint('dashboard', __name__, url_prefix='/authorised')
'''
    redirected to this route after successfull registeration or login
'''


@bp.route('/dash', methods=["GET", "POST"])
@login_required
def dash():
    html_details = {}
    '''
        if this route is called through post that means value of one of the combo boxes has changed.
        the received data contains a json object.(refer to dashboard.js (comboChanged()) for content)
    '''
    if request.method == "POST":
        data = request.get_json(force=True)
        filter_type = data['type']
        filter_list = filter_type.split(',')
        project_name = data['project_name']
        helper = DashHelper(db.get_db())
        user_id = session['user_id']
        # all the filters are passed to this function which searches and returns cards based on filters given
        html_details = helper.get_project_cards(
            filter_list, user_id, project_name)
        print(html_details.keys())
        # due to json serialization order of dictionary is lost. Therefore I am adding indexes to keys
        for idx, key in enumerate(html_details.copy().keys()):
            new_key = key + '/' + str(idx)
            html_details[new_key] = html_details.pop(key)
        session['html_details'] = html_details
        session['details_for_filter'] = {
            'filter_type': filter_list, 'project_name': project_name}
        # this is the redirect url which is send to dashboard.js
        return f'/authorised/filtered?{filter_list}'
    else:
        helper = DashHelper(db.get_db())
        user_id = session['user_id']
        html_details = helper.get_project_cards("all", user_id)
        return render_template('dashboard.html', dict_keys=list(html_details.keys()), value=html_details)


'''
    this is the page javascript redirects to after all the card data has been collected
'''


@bp.route('/filtered/<filter_type>', methods=["GET", "POST"])
@login_required
def filtered(filter_type):
    html_details = session['html_details']
    # since json serialization messes up with order of the dictionary an index has been added to every key
    # (refer to dash() function in this file for details)
    order_list = [None] * len(html_details.keys())
    for key in list(html_details.keys()):
        new_key, idx = key.split('/')
        order_list[int(idx.strip())] = (new_key, html_details[key])

    ordered_html_dict = {}
    counter = 0
    for key, value in order_list:
        updated_value = []
        if len(value) != 0:
            for tup in value:
                tup_list = list(tup)
                if len(tup_list) != 0:
                    if tup_list[6] != None and tup_list[7] != None:
                        tup_list[6] = db.get_user_name_from_user_id(
                            int(tup[6]))
                        tup_list[7] = db.get_user_name_from_user_id(
                            int(tup[7]))
                updated_value.append(tup_list)
        ordered_html_dict[key] = updated_value

    return render_template('dashboard.html', dict_keys=list(ordered_html_dict.keys()), value=ordered_html_dict)


'''
    this route is used to return data to javascript so that it can set the value of the combo boxes
    refer to (dashboard.js comboLoaded() for details)
'''


@bp.route('/filtered/type/fetch', methods=['GET', 'POST'])
@login_required
def filter_type_fetch():
    details = session['details_for_filter']
    return f"{details['filter_type']}: {details['project_name']}"
