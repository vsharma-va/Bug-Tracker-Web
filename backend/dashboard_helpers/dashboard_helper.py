class DashHelper():
    def __init__(self, db):
        self.db = db

    def get_project_cards(self, filters: list[str], user_id: int, filter_on: str = 'None') -> dict:
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
                            cursor.execute("SELECT * FROM projectData where project_id = %s and asigned_to = %s", [
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
