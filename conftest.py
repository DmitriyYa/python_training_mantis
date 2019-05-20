from fixture.application import Application
import pytest
import json
import os.path



fixture = None
config_file = None


def load_config(file):
    global config_file
    if config_file is None:
        config_file_json = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
        with open(config_file_json) as f:
            config_file = json.load(f)
    return config_file


@pytest.fixture
def app(request):
    global fixture

    browser = request.config.getoption("--browser")
    web_config = load_config(request.config.getoption("--target"))['web']
    web_admin = load_config(request.config.getoption("--target"))['webadmin']

    if fixture is None or not fixture.is_valid():
        fixture = Application(browser=browser, base_url=web_config["baseUrl"])
        fixture.session.login(username=web_admin["username"], password=web_admin["password"])
    return fixture


@pytest.fixture(scope="session", autouse=True)
def stop(request):
    def fin():
        fixture.destroy()

    request.addfinalizer(fin)
    return fixture


# parametri komandnoi ctroki
# hook function https://docs.pytest.org/en/latest/parametrize.html#basic-pytest-generate-tests-example
def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome")
    parser.addoption("--target", action="store", default="target.json")
