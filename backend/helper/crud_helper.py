import db
from enum import Enum

class Status(Enum):
    OPEN = 'open'
    IN_PROGRESS = 'in_progress'
    TO_BE_TESTED = 'to_be_tested'
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
                        "SELECT status FROM userHierarchyProjects WHERE project_id = %s", [project[0]])
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
                cursor.execute("SELECT * FROM projectData WHERE project_id = %s AND column_name = %s", [project_id, status_value])
                return cursor.fetchall()
            else:
                cursor.execute("SELECT * FROM projectData WHERE project_id = %s", [project_id])
                return cursor.fetchall()
                
    @staticmethod
    def serialize_dict(html_details: dict) -> dict:
        for idx, key in enumerate(html_details.copy().keys()):
            new_key = key + '/' + str(idx)
            html_details[new_key] = html_details.pop(key)
        return html_details

    @staticmethod
    def order_and_sub_username(html_details: dict, remove_serial=True) -> dict:
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
                            tup_list[6] = db.get_user_name_from_user_id(
                                int(tup[6]))
                            tup_list[7] = db.get_user_name_from_user_id(
                                int(tup[7]))
                    updated_value.append(tup_list)
            ordered_html_dict[key] = updated_value
        return ordered_html_dict
