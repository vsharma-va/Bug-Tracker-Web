from datetime import datetime
import json
from flask import render_template, request, flash
from flask_wtf.csrf import Blueprint, session
import secrets
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import binascii

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
    """Loads all the data from database and renders template for the /dash route

    Returns:
        str: html
    """
    html_details = {}
    '''
        if this route is called through post that means value of one of the combo boxes has changed.
        the received data contains a json object.(refer to dashboard.js (comboChanged()) for content)
    '''
    helper = CrudHelper(db.get_db())
    user_id = session['user_id']
    html_details = helper.get_all_project_cards_by_id_with_filter("all", user_id)
    user_name = helper.get_user_name_by_user_id(user_id).split('@')
    user_sub_details = helper.order_and_sub_username(
        html_details, False)
    return render_template('dashboard/dashboard.html', dict_keys=list(user_sub_details.keys()), value=user_sub_details, user_name=user_name[0])


'''
    this is the page javascript redirects to after all the card data has been collected
'''


@bp.route('/dash/filter/<filter_type>', methods=["GET", "POST"])
@login_required
def filter(filter_type):
    if request.method == "POST":
        data = request.get_json(force=True)
        project_name = data['project_name']
        filter_type = data['type']
        filter_list = filter_type.split(',')
        helper = CrudHelper(db.get_db())
        user_id = session['user_id']
        # all the filters are passed to this function which searches and returns cards based on filters given
        html_details = helper.get_all_project_cards_by_id_with_filter(
            filter_list, user_id)
        html_details = helper.order_and_sub_username(html_details, False)
        # due to json serialization order of dictionary is lost. Therefore I am adding indexes to keys
        # html_details = CrudHelper.serialize_dict(html_details)
        session['html_details'] = html_details
        session['details_for_filter'] = {'filter_type': filter_list}
        card_dict = {}
        template_list = []
        for property_list in html_details[project_name]:
            template_list.append(render_template('dashboard/helper/card.html', property_list=property_list))
        card_dict[project_name] = template_list
        return json.dumps(card_dict)
        # this is the redirect url which is send to dashboard.js
        # return f'/authorised/dash/filtered?{filter_list}'

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

@bp.route("/dash/charts/gcps/<project_name>", methods=["GET"])
@login_required
def get_current_project_statistics(project_name):
    helper = CrudHelper(db.get_db())
    try:
        project_id = session['project_id_for_graph']
    except KeyError:
        if project_name == 'None':
            project_id = 'none'
        else:
            project_id = -1
    
    all_projects = helper.get_all_user_projects(int(session['user_id']))
    if project_id == 'none' or all_projects == 'none' or project_name == 'None':
        stats = {'status': 'none'}
        return json.dumps(stats)
    else:
        project_id = helper.get_projectid_by_project_name(project_name)
        session['project_id_for_graph'] = project_id
        stats = helper.get_num_ele_in_all_columns_by_projectid(project_id)
        return json.dumps(stats)

@bp.route("/dash/generateInvite", methods=["POST"])
@login_required
def generate_invite():
    if request.method == "POST":
        data = request.get_json(force=True)
        all_ids_str = data['user_ids']
        logged_in_user_id = session['user_id']
        project_name = data['project_name']
        helper = CrudHelper(db.get_db())
        serial_num = helper.get_next_serial_num('userInvites')
        invite = f'BugMania/Invite/UserIds={all_ids_str}/ProjectName={project_name}/CreatedBy={logged_in_user_id}/SerialNum={serial_num}' 
        key = secrets.token_bytes(32) 
        nonce_length = 12 ######SHOULD ALWAYS BE EQUAL TO 12
        nonce = secrets.token_bytes(12) 
        cipher_text = nonce + AESGCM(key).encrypt(nonce, bytes(invite, 'utf-8'), b'') 
        current_utc_time = datetime.utcnow() 
        helper.insert_into_user_invites_table(logged_in_user_id, binascii.hexlify(key), binascii.hexlify(cipher_text), nonce_length, current_utc_time) 
        return binascii.hexlify(cipher_text)
    return "Sorry this route is inaccessible manualy" 

@bp.route("/dash/joinWithInvite", methods=["POST"]) 
@login_required
def join_with_invite():
    if request.method == "POST":
        data = request.get_json(force=True)
        join_link_unclean = data['join_link']
        join_link_clean = bytes(join_link_unclean.strip(), 'utf-8')
        helper = CrudHelper(db.get_db())
        data_to_decode = helper.get_data_to_decode_invite(join_link_clean)
        key = binascii.unhexlify(data_to_decode['key'])
        cipher_text = binascii.unhexlify(data_to_decode['encrypted_code'])
        decrypt = AESGCM(key).decrypt(cipher_text[:int(data_to_decode['nonce_length'])], cipher_text[int(data_to_decode['nonce_length']):], b'')
        decrypt_str = decrypt.decode('utf-8')
        all_values = decrypt_str.split('/')
        invited_user_ids = all_values[2].split('=')[1]
        project_invited_to = all_values[3].split('=')[1]
        logged_in_userid = session['user_id']
        if str(logged_in_userid) not in invited_user_ids:
            return json.dumps({'html': render_template('helper/flash_messages.html', flash_color="flash-red", message="You were not invited. Ask the project admin to create another invite with your user id included"), 'status': 'error'})
        else:
            helper.add_user_to_a_project(str(logged_in_userid), project_invited_to)
            return{'html': render_template('helper/flash_messages.html', flash_color="flash-green", message="Added to project successfully !"), 'status': 'success'}
