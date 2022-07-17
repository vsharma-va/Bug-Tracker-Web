import json
from flask import render_template, request
from flask_wtf.csrf import Blueprint, session

import db
from auth import login_required
from helper.crud_helper import CrudHelper

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
        helper = CrudHelper(db.get_db())
        user_id = session['user_id']
        # all the filters are passed to this function which searches and returns cards based on filters given
        html_details = helper.get_all_project_cards_by_id_with_filter(
            filter_list, user_id)
        # due to json serialization order of dictionary is lost. Therefore I am adding indexes to keys
        html_details = CrudHelper.serialize_dict(html_details)
        session['html_details'] = html_details
        session['details_for_filter'] = {'filter_type': filter_list}
        # this is the redirect url which is send to dashboard.js
        return f'/authorised/dash/filtered?{filter_list}'
    else:
        helper = CrudHelper(db.get_db())
        user_id = session['user_id']
        html_details = helper.get_all_project_cards_by_id_with_filter("all", user_id)
        user_sub_details = helper.order_and_sub_username(
            html_details, False)
        return render_template('dashboard/dashboard.html', dict_keys=list(user_sub_details.keys()), value=user_sub_details)


'''
    this is the page javascript redirects to after all the card data has been collected
'''


@bp.route('/dash/filtered/<filter_type>', methods=["GET", "POST"])
@login_required
def filtered(filter_type):
    html_details = session['html_details']
    helper = CrudHelper(db.get_db)
    # since json serialization messes up with order of the dictionary an index has been added to every key
    # (refer to dash() function in this file for details)
    ordered_html_dict = helper.order_and_sub_username(html_details)
    return render_template('dashboard/dashboard.html', dict_keys=list(ordered_html_dict.keys()), value=ordered_html_dict)


'''
    this route is used to return data to javascript so that it can set the value of the combo boxes
    refer to (dashboard.js comboLoaded() for details)
'''


@bp.route('/filtered/type/fetch', methods=['GET', 'POST'])
@login_required
def filter_type_fetch():
    try:
        details = session['details_for_filter']
    except KeyError:
        return ":"
    return f"{details['filter_type']}:"

@bp.route('/dash/update', methods=['GET', 'POST'])
@login_required
def dash_update():
    if request.method == "POST":
        data = request.get_json(force=True)
        filter_type = data['type']
        filter_list = filter_type.split(',')
        helper = CrudHelper(db.get_db())
        user_id = session['user_id']
        html_details = helper.get_all_project_cards_by_id_with_filter(
            filter_list, user_id)
        html_details = helper.order_and_sub_username(html_details, False)
        card_dict = {}
        template_list = []
        for key in html_details.keys():
            for property_list in html_details[key]:
                template_list.append(render_template(
                    'dashboard/helper/card.html', property_list=property_list))
            card_dict[key] = template_list
            template_list = []
        return json.dumps(card_dict)
    return "NONE"
