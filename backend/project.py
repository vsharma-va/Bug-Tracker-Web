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
    data_dict = helper.order_and_sub_username(data_dict, False)
    return render_template('project/project_main.html', data=data_dict)

@bp.route('/main/<project_name>/on/<event_type>', methods=["GET", "POST"])
@login_required
def on_receive_or_remove(project_name, event_type):
    if request.method == "POST":
        data = request.get_json(force=True)
        data['column'] = data['received_by']
        '''
        serialize returns a stringwith their ids in order seperated by &
        eg. if a card with id col1_1 is moved to column 2 at row 2. In column 2 there already is an item with id col2_1
        serialize will return -> col2[]=1&col1[]=1
        '''
        new_order: list = data['new_order'].split('&')
        original_order: list = data['original_order'].split('&')
        print(new_order)
        print(original_order)
        temp = {}
        if event_type == 'receive':
            if len(original_order) != 1 and original_order[0] != '':
                for idx, od in enumerate(original_order):
                    new_position = new_order.index(od)
                    temp[idx+1] = new_position + 1
                new_value = list(filter(lambda z: z not in original_order, new_order))[0]
                order_dict = {}
                order_dict['add'] = new_order.index(new_value) + 1
                # this step is necessary. If col_pos is update before removing an element
                # the wrong element may be deleted since to find the value col_pos is used
                order_dict.update(temp)
            else:
                order_dict = {}
                order_dict['add'] = 1

        elif event_type == 'remove':
            if len(new_order) != 1 and new_order[0] != '':
                for idx, od in enumerate(new_order):
                    old_position = original_order.index(od)
                    temp[old_position+1] = idx + 1
                removed_value = list(filter(lambda z: z not in new_order, original_order))[0]
                order_dict = {}
                order_dict['remove'] = original_order.index(removed_value) + 1
                order_dict.update(temp)
            else:
                order_dict = {}
                order_dict['remove'] = 'all'
        
        helper = CrudHelper(db.get_db())
        helper.update_data_and_reorder(order_dict, data, project_name.strip())
    return "ok"