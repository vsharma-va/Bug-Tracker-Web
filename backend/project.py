from flask import render_template, request, render_template_string
from flask_wtf.csrf import Blueprint
from helper.crud_helper import CrudHelper, Status
import json

import db
from auth import login_required

bp = Blueprint('project', __name__, url_prefix='/authorised/dash')

# main route. :w
@bp.route('/main/<project_name>')
@login_required
def project_details_page(project_name):
    """Loads the data and passes it to the html template

    Args:
        project_name (str): name of the project whose data is being displayed

    Returns:
        str: renders the template present at frontend/html/project/project_main.html
    """
    helper = CrudHelper(db.get_db())
    data_dict = {}
    for status in Status:
        # returns a tuple, Status is an enum present in crud_helper.py
        html_details = helper.get_project_cards_by_project_name(
            project_name, status)
        data_dict[status.value] = html_details
    data_dict = helper.order_and_sub_username(data_dict, False)
    return render_template('project/project_main.html', data=data_dict)

@bp.route('/main/<project_name>/on/<event_type>', methods=["GET", "POST"])
@login_required
def on_receive_or_remove(project_name, event_type):
    """This route is called whenever an item is removed or added to a column

    Args:
        project_name (str): name of the project
        event_type (str): remove or receive (event types of sortable jquery)

    Returns:
        str: returns the eventtype so that javascript can update the page with the correct ids
    """
    if request.method == "POST":
        data = request.get_json(force=True)
        data['column'] = data['received_by']
        id_str: str = data['id_in_order']
        data['id_in_order'] = id_str.replace('[', '').replace(']', '').split(',')
        '''
        serialize returns a stringwith their ids in order seperated by &
        eg. if a card with i
                        " {{ card_macro(value) }} "d col1_1 is moved to column 2 at row 2. In column 2 there already is an item with id col2_1
        serialize will return -> col2[]=1&col1[]=1
        '''
        new_order: list = data['new_order'].split('&')
        original_order: list = data['original_order'].split('&')
        temp = {}
        if event_type == 'receive':
            # if len == 1 and first element = empty strings then the column is empty
            if len(original_order) == 1 and original_order[0] == '':
                order_dict = {}
                order_dict['add'] = 1
            
            else:
                '''
                    In receive event the original order will not contain the value that was added
                    therefore it is compared with new_position list to find out the new position for 
                    existing elements
                '''
                order_dict = {}
                for idx, od in enumerate(original_order):
                    new_position = new_order.index(od)
                    temp[idx+1] = new_position + 1
                # the value which is not in original order is the one which was added
                new_value = list(filter(lambda z: z not in original_order, new_order))[0]
                order_dict['add'] = new_order.index(new_value) + 1
                order_dict.update(temp)
                data['id_in_order'].remove(data['id'])
                print(order_dict)
                # order_dict -> {'add': new_pos, original_pos: new_pos, ...}
        elif event_type == 'remove':
            if len(new_order) == 1 and new_order[0] == '':
                order_dict = {}
                order_dict['remove'] = 'all'
            else:
                '''
                    In remove event the new order will not contain the value that was removed
                    therefroe it is compared with original_order list to find out the new position for 
                    exisiting elements
                '''
                for idx, od in enumerate(new_order):
                    old_position = original_order.index(od)
                    temp[old_position+1] = idx + 1
                # the value which is not in new order is the one which was removed
                removed_value = list(filter(lambda z: z not in new_order, original_order))[0]
                order_dict = {}
                order_dict['remove'] = original_order.index(removed_value) + 1
                order_dict.update(temp)
                print(order_dict, 'remove')
                # order_dict -> {'remove': new_pos, original_pos: new_pos, ...}
                    
        helper = CrudHelper(db.get_db())
        helper.update_data_and_reorder(order_dict, data, project_name.strip())
    return event_type

@bp.route('/main/<project_name>/update')
@login_required
def update_page(project_name):
    """This route is called periodically and also when receive event is completed

    Args:
        project_name (str): name of the project

    Returns:
        json: contains the html for all the cards present eg {'open': data, 'in-progress': data ...}
    """
    helper = CrudHelper(db.get_db())
    data_dict = {}
    for status in Status:
        html_details = helper.get_project_cards_by_project_name(
            project_name, status)
        data_dict[status.value] = html_details
    data_dict = helper.order_and_sub_username(data_dict, False)
    keys = list(data_dict.keys())
    html = {}
    card_html_list = []
    # instead of returning the whole template only cards are returned and javascript adds it to html
    for idx, data in enumerate(data_dict.values()):
        for index, card in enumerate(data):
            if keys[idx] != None:
                # macro present at frontend/html/helper/card_macro.html
                card_html = render_template_string(
                    "{% from 'helper/card_macro.html' import card_macro %}"
                    "{{ card_macro(value, column_name, idx) }}",
                    value = card,
                    column_name = keys[idx],
                    idx = index + 1,
                )
                card_html_list.append(card_html)
        html[keys[idx]] = card_html_list
        card_html_list = []
    return json.dumps(html)

@bp.route('/main/<project_name>/loadoverlay')
def on_click_overlay(project_name):
    pass