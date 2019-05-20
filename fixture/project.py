from model.project import Project
from selenium.webdriver.support.ui import Select
import urlparse


class ProjectHelper:
    project_cache = None

    def __init__(self, app):
        self.app = app

    def open_project_page(self):
        wd = self.app.wd
        if not (wd.current_url.endswith("/manage_proj_page.php") and len(
                wd.find_elements_by_xpath("/html/body/table[3]/tbody/tr[1]/td/form/input[2]")) > 0):
            wd.find_element_by_link_text("Manage").click()
            wd.find_element_by_link_text("Manage Projects").click()

    def return_to_project_page(self):
        wd = self.app.wd
        wd.find_element_by_xpath("/html/body/div[2]/span/a").click()

    def change_field_value(self, xPath, text):
        wd = self.app.wd
        if text is not None:
            wd.find_element_by_xpath(xPath).clear()
            wd.find_element_by_xpath(xPath).send_keys(text)

    def change_field_value_select_by_visible_text(self, feild_name, text):
        wd = self.app.wd
        if text is not None:
            wd.find_element_by_name(feild_name).click()
            Select(wd.find_element_by_name(feild_name)).select_by_visible_text(text)

    def fill_form_group(self, project):
        wd = self.app.wd
        self.change_field_value("/html/body/div[3]/form/table/tbody/tr[2]/td[2]/input", project.project_name)
        self.change_field_value_select_by_visible_text("status", project.status)
        self.change_field_value_select_by_visible_text("view_state", project.view_status)
        self.change_field_value("/html/body/div[3]/form/table/tbody/tr[6]/td[2]/textarea", project.description)

    def create(self, project):
        wd = self.app.wd
        self.open_project_page()
        wd.find_element_by_css_selector("input[value='Create New Project']").click()
        self.fill_form_group(project)
        wd.find_element_by_css_selector("input[value='Add Project']").click()
        self.return_to_project_page()
        self.project_cache = None

    def delete_project_by_id(self, id):
        wd = self.app.wd
        self.open_project_page()
        self.select_project_by_id(id)
        wd.find_element_by_css_selector("input[value='Delete Project']").click()
        wd.find_element_by_css_selector("input[value='Delete Project']").click()
        self.project_cache = None

    def select_project_by_id(self, id):
        wd = self.app.wd
        self.open_project_page()
        wd.find_element_by_css_selector("a[href='manage_proj_edit_page.php?project_id=%s']" % id).click()


    def get_project_list(self):
        if self.project_cache is None:
            wd = self.app.wd
            self.open_project_page()
            self.project_cache = []
            for row in wd.find_element_by_xpath("/html/body/table[3]/tbody").find_elements_by_tag_name("tr"):
                if row != wd.find_element_by_xpath("/html/body/table[3]/tbody").find_elements_by_tag_name("tr")[0] and \
                        row != wd.find_element_by_xpath("/html/body/table[3]/tbody").find_elements_by_tag_name("tr")[1]:
                    td = row.find_elements_by_tag_name("td")
                    name = td[0].find_element_by_tag_name("a").text
                    status = td[1].text
                    view_ststus = td[3].text
                    description = td[4].text
                    url = td[0].find_element_by_tag_name("a").get_attribute("href")
                    parsed = urlparse.urlparse(url)
                    id = urlparse.parse_qs(parsed.query)['project_id'][0]
                    self.project_cache.append(
                        Project(project_name=name, status=status, view_status=view_ststus, description=description,
                                id=id))
        return list(self.project_cache)
