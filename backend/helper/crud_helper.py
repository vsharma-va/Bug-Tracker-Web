from collections import Counter
from enum import Enum

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

    def get_project_cards_by_project_name(self, project_name: str, status: Status = Status.NONE) -> tuple:
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

    def update_data_and_reorder(self, order_dict: dict, update_card_data: dict, project_name: str) -> None:
        self.db.autocommit = True
        cursor = self.db.cursor()
        cursor.execute("SELECT id FROM projectUserInfo WHERE project_name = %s", [project_name])
        project_id = cursor.fetchone()[0]
        present_cards_counter = 0
        for key in order_dict.keys():
            # go to project.py to understand why key == 'add' or 'remove' is used
            if key == 'add':
                by_user = update_card_data['by'].split('->')[0].strip()
                assigned_to = update_card_data['by'].split('->')[1].strip()
                by_user_id = self.get_user_id_by_user_name(by_user)
                assigned_to_id = self.get_user_id_by_user_name(assigned_to)
                cursor.execute("INSERT INTO projectData (id, project_id, tag, tag_color, column_name, description, by_user, assigned_to, col_pos) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", [int(update_card_data['id']), project_id, update_card_data['tag'], update_card_data['tag_color'], update_card_data['column'], update_card_data['description'], by_user_id, assigned_to_id, order_dict[key]])
            elif key == 'remove':
                # column empty condition
                if order_dict[key] == 'all':
                    cursor.execute("DELETE FROM projectData WHERE column_name = %s AND project_id = %s AND id = %s", [update_card_data['column'], project_id, int(update_card_data['id'])])
                else:
                    cursor.execute("DELETE FROM projectData WHERE col_pos = %s AND project_id = %s AND column_name = %s AND id = %s", [order_dict[key], project_id, update_card_data['column'], int(update_card_data['id'])])
            else:
                cursor.execute("UPDATE projectData SET col_pos = %s WHERE col_pos = %s AND column_name = %s AND description != %s AND id = %s", [order_dict[key], key, update_card_data['column'], update_card_data['description'], update_card_data['id_in_order'][present_cards_counter]])
                present_cards_counter += 1
    
    def update_user_roles(self, user_id: int, project_id: int, new_role_name: str) -> None:
        cursor = self.db.cursor()
        cursor.execute("UPDATE userHierarchyProjects SET status = %s WHERE user_id = %s and project_id = %s", [new_role_name, user_id, project_id])
    
    def add_new_project(self, project_name: str, created_by_id: int) -> None:
        cursor = self.db.cursor()
        cursor.execute("INSERT INTO projectUserInfo (project_name, users) VALUES(%s, %s)", [project_name, created_by_id])
        next_serial_number = self.get_next_serial_num('projectUserInfo')
        cursor.execute("INSERT INTO projectRoles(project_id, can_delete_from, can_move_to_and_from, role_name)VALUES (%s, %s, %s, %s)", [next_serial_number-1, 'open, in-progress, to-be-tested, closed', 'open, in-progress, to-be-tested, closed', 'admin'])
        cursor.execute("INSERT INTO projectRoles(project_id, can_delete_from, can_move_to_and_from, role_name) VALUES (%s, %s, %s, %s)", [next_serial_number-1, '', '', 'read'])
        cursor.execute("INSERT INTO userHierarchyProjects (project_id, status, user_id) VALUES(%s, %s, %s)", [next_serial_number-1, 'admin', created_by_id])
        return 'ok'
    
    def get_user_name_by_user_id(self, user_id: int) -> str: 
        cursor = self.db.cursor()
        cursor.execute("SELECT username FROM cUser WHERE id = %s", [user_id])
        username = cursor.fetchone()
        try:
            return username[0]
        except TypeError:
            return None
    
    def get_user_id_by_user_name(self, user_name: str) -> str:
        cursor = self.db.cursor()
        cursor.execute("SELECT id FROM cUser WHERE username = %s", [user_name])
        user_id = cursor.fetchone()
        try:
            return user_id[0]
        except TypeError:
            return None
    
    def get_num_ele_in_all_columns_by_projectid(self, project_id: int) -> dict:
        cursor = self.db.cursor()
        cursor.execute("SELECT column_name FROM projectData WHERE project_id = %s order by column_name", [project_id])
        query_results = cursor.fetchall()
        clean_query_result = [ele[0] for ele in query_results]
        return Counter(clean_query_result)
    
    def get_projectid_by_project_name(self, project_name: str) -> str:
        cursor = self.db.cursor()
        cursor.execute("SELECT id FROM projectuserinfo WHERE project_name = %s", [project_name])
        project_id = cursor.fetchone()
        try: 
            return project_id[0]
        except TypeError:
            return None
    
    def get_next_serial_num(self, table_name: str) -> str:
        cursor = self.db.cursor()
        # cursor.execute(f"SELECT nextval({serial_name}::regclass)")
        cursor.execute(f"SELECT id FROM {table_name} ORDER BY id DESC LIMIT 1")
        serial_num = cursor.fetchone()
        if serial_num is None:
            return 1
        else:
            return serial_num[0] + 1
    
    def get_data_to_decode_invite(self, encoded_text: str):
        cursor = self.db.cursor()
        cursor.execute(f"SELECT * FROM userInvites WHERE encrypted_code = %s", [encoded_text])
        result = cursor.fetchone()
        data_to_decode = {}
        data_to_decode['created_by'] = result[1]
        data_to_decode['key'] = result[2]
        data_to_decode['encrypted_code'] = result[3]
        data_to_decode['nonce_length'] = result[4]
        return data_to_decode
    
    def insert_into_user_invites_table(self, created_by: int, key: bytes, encrypted_code: bytes, nonce_length: int, datetimestamp: str):
        cursor = self.db.cursor()
        cursor.execute("INSERT INTO userInvites (created_by, key, encrypted_code, nonce_length, date_time_created) VALUES (%s, %s, %s, %s, %s)", [created_by, key, encrypted_code, nonce_length, datetimestamp])
    
    def add_user_to_a_project(self, user_id_to_add: str, project_name: str):
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM projectUserInfo WHERE project_name = %s", [project_name])
        row = cursor.fetchone()
        new_users = ''
        project_id = self.get_projectid_by_project_name(project_name)
        if user_id_to_add not in str(row[2]):
            new_users = str(row[2]) + ', ' + user_id_to_add
            cursor.execute("UPDATE projectUserInfo SET users = %s WHERE id = %s", [new_users, row[0]])
            cursor.execute("INSERT INTO userHierarchyProjects (project_id, status, user_id) VALUES(%s, %s, %s)", [project_id, 'read', int(user_id_to_add)])
        else:
            new_users = row[2]
    
    def get_all_user_projects(self, user_id: int):
        cursor = self.db.cursor()
        cursor.execute(
                "SELECT * FROM projectUserInfo WHERE users LIKE '%%%s%%';", [int(str(user_id))])
        result = cursor.fetchall()
        if len(result) == 0:
            return 'none'
        else:
            return result
    
    def get_all_project_roles(self, project_name):
        cursor = self.db.cursor()
        project_id = self.get_projectid_by_project_name(project_name)
        cursor.execute("SELECT * FROM projectRoles WHERE project_id = %s", [project_id])
        return cursor.fetchall()
    
    def get_all_users(self, project_name):
        cursor = self.db.cursor()
        cursor.execute("SELECT users FROM projectUserInfo WHERE project_name = %s", [project_name])
        try:
            return cursor.fetchone()[0]
        except TypeError:
            return None
    
    def get_users_current_role_in_project(self, project_id: int, user_id: int):
        cursor = self.db.cursor()
        cursor.execute("SELECT status FROM userHierarchyProjects WHERE project_id = %s AND user_id = %s", [project_id, user_id])
        try:
            return cursor.fetchone()[0]
        except TypeError:
            return None
        
    def get_role_defintion(self, role_name: str, project_id: int):
        cursor = self.db.cursor()
        cursor.execute("SELECT can_delete_from, can_move_to_and_from FROM projectRoles WHERE role_name = %s AND project_id = %s", [role_name, project_id])
        query_result = cursor.fetchone()
        return_dict = {'can_delete_from': query_result[0], 'can_move_to_and_from': query_result[1]}
        return return_dict

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
                            tup_list[6] = self.get_user_name_by_user_id(
                                int(tup[6]))
                            tup_list[7] = self.get_user_name_by_user_id(
                                int(tup[7]))
                    updated_value.append(tup_list)
            ordered_html_dict[key] = updated_value
        return ordered_html_dict