from model.project import Project
from generator.project import *


def test_add_project(app):
    old_project_list = app.soap.get_project_list("administrator","root")

    project = Project(project_name=random_string("project_name", 10), description=random_string("description", 20))
    app.project.create(project)

    new_project_list = app.soap.get_project_list("administrator","root")

    old_project_list.append(project)

    assert sorted(old_project_list, key=Project.id_or_max) == sorted(new_project_list, key=Project.id_or_max)


def test_delete_project(app):
    if len(app.soap.get_project_list("administrator","root")) == 0:
        project = Project(project_name=random_string("project_name", 10), description=random_string("description", 20))
        app.project.create(project)

    old_project_list = app.soap.get_project_list("administrator","root")

    project = random.choice(old_project_list)

    app.project.delete_project_by_id(project.id)

    new_project_list = app.soap.get_project_list("administrator","root")
    assert len(old_project_list) - 1 == len(new_project_list)

    old_project_list.remove(project)
    assert sorted(old_project_list, key=Project.id_or_max) == sorted(new_project_list, key=Project.id_or_max)
