from sys import maxsize


class Project():
    def __init__(self, project_name=None, status=None, view_status=None, description=None, id=None):
        self.project_name = project_name
        self.status = status
        self.view_status = view_status
        self.description = description
        self.id = id

    def __repr__(self):
        return "%s: %s" % (self.id, self.project_name)

    def __eq__(self, other):
        return self.project_name == other.project_name and (self.id is None or other.id is None or self.id == other.id)

    def id_or_max(self):
        if self.id:
            return int(self.id)
        else:
            return maxsize
