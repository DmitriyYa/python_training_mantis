from suds.client import Client
from suds import WebFault
from model.project import Project

class SoapHelper:
    def __init__(self, app):
        self.app = app

    def get_client(self):
        return Client("http://localhost/mantisbt-1.2.20/api/soap/mantisconnect.php?wsdl")

    def can_login(self, username, password):
        client = self.get_client()
        try:
            client.service.mc_login(username, password)
            return True
        except WebFault:
            return False

    def get_project_list(self, username, password):
        client = self.get_client()
        result_project_list = []
        try:
            # client.service.mc_login(username, password)
            project_data_lisr = client.service.mc_projects_get_user_accessible(username, password)
            for project in project_data_lisr:
                result_project_list.append(Project(project_name=project.name,status=project.status.name,
                                                   view_status=project.view_state.name, description=project.description, id=project.id))
            return result_project_list
        except WebFault:
            return False