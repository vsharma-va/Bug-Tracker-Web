class DashHelper():
    def __init__(self, db):
        self.db = db

    def get_project_cards(self, filter: str, user_id: int, filter_on: str = 'None') -> dict:
        html_details = {}
        projects = []
        if user_id is not None:
            cursor = self.db.cursor()
            cursor.execute(
                "SELECT * FROM projectUserInfo WHERE users LIKE '%%%s%%';", [int(str(user_id))])
            user_projects = cursor.fetchall()
            if user_projects is not None:
                project_and_user_role = {}
                for project in user_projects:
                    cursor.execute(
                        "SELECT status FROM userHierarchyProjects WHERE project_id = %s", [project[0]])
                    user_role = cursor.fetchone()
                    if user_role is not None:
                        projects.append(project[1])
                        project_and_user_role['project_id'] = project[0]
                        project_and_user_role['project_name'] = project[1]
                        project_and_user_role['user_role'] = user_role[0]
                        if filter == "all":
                            cursor.execute(
                                "SELECT * FROM projectData where project_id = %s", [project_and_user_role['project_id']])
                        elif filter == "assigned-to-me":
                            if filter_on != 'None':
                                if filter_on == project_and_user_role['project_name']:
                                    cursor.execute("SELECT * FROM projectData where project_id = %s and asigned_to = %s", [
                                                   project_and_user_role['project_id'], user_id])
                                else:
                                    cursor.execute(
                                        "SELECT * FROM projectDATA where project_id = %s", [project_and_user_role['project_id']])
                        else:
                            cursor.execute(
                                "SELECT * FROM projectData where project_id = %s", [project_and_user_role['project_id']])
                        card = cursor.fetchall()
                        tmp_list = []
                        for tup in card:
                            tmp_list.append(tup)
                            html_details[project_and_user_role['project_name']] = tmp_list
        testing = list(html_details.keys())
        for i in projects:
            if i not in testing:
                html_details[i] = ''
        return html_details
