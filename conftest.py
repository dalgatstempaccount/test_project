import pytest

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome")
    parser.addoption("--password", action="store" )

@pytest.fixture
def get_password(request):
    return request.config.getoption("--password")

@pytest.fixture
def get_browser_name(request):
    return request.config.getoption("--browser")