import db
from enum import Enum
from flask import redirect, url_for

class Status(Enum):
    OPEN = 'open'
    IN_PROGRESS = 'in-progress'
    TO_BE_TESTED = 'to-be-tested'
    CLOSED = 'closed'
    NONE = None

class CrudHelper():
    def __init__(self, db):
        self.db = db

    def get_all_project_cards_by_id_with_filter(self, filters: list[str], user_id: int) -> dict:
        html_details = {}
        projects = []
        if user_id is not None:
            # projectUserInfo table contains all the projects with their members. Is used to find all the projects
            # the user is part of
            cursor = self.db.cursor()
            cursor.execute(
                "SELECT * FROM projectUserInfo WHERE users LIKE '%%%s%%';", [int(str(user_id))])
            user_projects = cursor.fetchall()
            if user_projects is not None:
                project_and_user_role = {}
                for idx, project in enumerate(user_projects):
                    # userHierarchyProjects table contains user permissions for all the projects they are a part of
                    cursor.execute(
                        "SELECT status FROM userHierarchyProjects WHERE user_id = %s", [user_id])
                    user_role = cursor.fetchone()
                    if user_role is not None:
                        # iterates over every project to find data wrt filters
                        # all project data is stored in projectData table
                        projects.append(project[1])
                        project_and_user_role['project_id'] = project[0]
                        project_and_user_role['project_name'] = project[1]
                        project_and_user_role['user_role'] = user_role[0]
                        if filters[idx] == "all":
                            cursor.execute(
                                "SELECT * FROM projectData where project_id = %s", [project_and_user_role['project_id']])
                        elif filters[idx] == "assigned-to-me":
                            cursor.execute("SELECT * FROM projectData where project_id = %s and assigned_to = %s", [
                                           project_and_user_role['project_id'], user_id])
                        else:
                            cursor.execute(
                                "SELECT * FROM projectData where project_id = %s", [project_and_user_role['project_id']])
                        card = cursor.fetchall()
                        tmp_list = []
                        if len(card) != 0:
                            for tup in card:
                                tmp_list.append(tup)
                                html_details[project_and_user_role['project_name']] = tmp_list
                        else:
                            tmp_list.append('')
                            html_details[project_and_user_role['project_name']] = tmp_list
        return html_details

    def get_project_cards_by_project_name(self, project_name: str, status: Status = Status.NONE):
        cursor = self.db.cursor()
        cursor.execute(
            "SELECT * FROM projectUserInfo WHERE project_name = %s ;", [project_name])
        project = cursor.fetchone()
        if project is not None:
            project_id = project[0] # project[0] = id, project[1] = project_name, project[2] = users
            if status != Status.NONE:
                status_value = status.value
                cursor.execute("SELECT * FROM projectData WHERE project_id = %s AND column_name = %s ORDER BY col_pos", [project_id, status_value])
                return cursor.fetchall()
            else:
                cursor.execute("SELECT * FROM projectData WHERE project_id = %s", [project_id])
                return cursor.fetchall()

    def update_data_and_reorder(self, order_dict: dict, update_card_data: dict, project_name: str):
        cursor = self.db.cursor()
        cursor.execute("SELECT id FROM projectUserInfo WHERE project_name = %s", [project_name])
        project_id = cursor.fetchone()[0]
        for key in order_dict.keys():    
            if key == 'add':
                by_user = update_card_data['by'].split('->')[0].strip()
                assigned_to = update_card_data['by'].split('->')[1].strip()
                by_user_id = self.get_user_id_from_user_name(by_user)
                assigned_to_id = self.get_user_id_from_user_name(assigned_to)
                cursor.execute("INSERT INTO projectData (project_id, tag, tag_color, column_name, description, by_user, assigned_to, col_pos) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", [project_id, update_card_data['tag'], update_card_data['tag_color'], update_card_data['column'], update_card_data['description'], by_user_id, assigned_to_id, order_dict[key]])
            elif key == 'remove':
                # column empty condition
                if order_dict[key] == 'all':
                    cursor.execute("DELETE FROM projectData WHERE column_name = %s AND project_id = %s", [update_card_data['column'], project_id])
                else:
                    cursor.execute("DELETE FROM projectData WHERE col_pos = %s AND project_id = %s AND column_name = %s", [order_dict[key], project_id, update_card_data['column']])
            else:
                cursor.execute("UPDATE projectData SET col_pos = %s WHERE col_pos = %s AND column_name = %s ", [order_dict[key], key, update_card_data['column']])
    
    def get_user_name_from_user_id(self, user_id: int): 
        cursor = self.db.cursor()
        cursor.execute("SELECT username FROM cUser WHERE id = %s", [user_id])
        username = cursor.fetchone()
        return username[0]
    
    def get_user_id_from_user_name(self, user_name: str):
        cursor = self.db.cursor()
        cursor.execute("SELECT id FROM cUser WHERE username = %s", [user_name])
        user_id = cursor.fetchone()
        return user_id[0]
    
    @staticmethod
    def serialize_dict(html_details: dict) -> dict:
        for idx, key in enumerate(html_details.copy().keys()):
            new_key = key + '/' + str(idx)
            html_details[new_key] = html_details.pop(key)
        return html_details

    def order_and_sub_username(self, html_details: dict, remove_serial=True) -> dict:
        if remove_serial:
            order_list = [None] * len(html_details.keys())
            for key in list(html_details.keys()):
                new_key, idx = key.split('/')
                order_list[int(idx.strip())] = (new_key, html_details[key])
        else:
            order_list = [None] * len(html_details.keys())
            for idx, key in enumerate(list(html_details.keys())):
                order_list[idx] = (key, html_details[key])

        ordered_html_dict = {}
        for key, value in order_list:
            updated_value = []
            if len(value) != 0:
                for tup in value:
                    tup_list = list(tup)
                    if len(tup_list) != 0:
                        if tup_list[6] != None and tup_list[7] != None:
                            tup_list[6] = self.get_user_name_from_user_id(
                                int(tup[6]))
                            tup_list[7] = self.get_user_name_from_user_id(
                                int(tup[7]))
                    updated_value.append(tup_list)
            ordered_html_dict[key] = updated_value
        return ordered_html_dict
