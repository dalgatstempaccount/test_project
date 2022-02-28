import gitea_docker
import git_interactions
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

from configparser import ConfigParser
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.firefox.service import Service as ServiceF
from webdriver_manager.firefox import GeckoDriverManager
from time import sleep
from page_objects import *

config = ConfigParser()
config.read('config.ini')

############ gitea docker deployment ##########################
@pytest.mark.order(1)
def test_gitea_installation_process(get_password):
    global container_id
    container_id, docker_start_code = gitea_docker.start_gitea_docker(get_password)
    print('Container id:', container_id, '\n', 'Docker dployment code:', docker_start_code)
    assert docker_start_code == 0

########### parsing with requests and bs4 ###################
@pytest.mark.order(2)
def test_paring_api_requests_with_bs():
    sleep(3)
    headers = {'Content-Type': 'text/html'}
    res = requests.get('http://localhost:3000', headers=headers).text
    soup = BeautifulSoup(res, 'html.parser')
    assert 'Install Gitea' == soup.find('button').text
    assert 'Initial Configuration' == soup.find('h3').text.strip()
    assert soup.find('p').findChild('a').text == 'documentation'

############## selenium startup ##############################
@pytest.mark.order(3)
def test_selenium_startup(get_browser_name):
    if(get_browser_name == 'chrome'):
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    elif(get_browser_name == 'firefox'):
        driver = webdriver.Firefox(service=ServiceF(GeckoDriverManager().install()))
    driver.implicitly_wait(30)
    driver.maximize_window()
    driver.get('{}:{}'.format(config['gitea']['url'], config['gitea']['port']))
    pytest.selenium_webdriver = driver

############## creating gitea account with selenium ##########
@pytest.mark.order(4)
def test_selenium_create_account():
    cf_page = InstallConfiguration(pytest.selenium_webdriver)
    cf_page.configure(ssh_port=2222)
    sleep(5)
    cf_page.get_driver().get('http://localhost:3000/user/login')
    lp_page = LoginPage(cf_page.get_driver())
    lp_page.click_sign_up_button()

    su_page = SignUpPage(lp_page.get_driver())
    su_page.sign_up(username=config['credentials']['name'],
        email=config['credentials']['email'], 
        password=config['credentials']['password'])
    
    pytest.selenium_webdriver = su_page.get_driver() 

############### creating new repo with selenium #########################
@pytest.mark.order(5)
def test_creation_of_new_repository_selenium():
    mp_page = MainPage( pytest.selenium_webdriver )
    mp_page.click_new_repo_button()

    nr_page = NewRepositoryPage( mp_page.get_driver())
    nr_page.create_repository(config['repo']['repo_name'])

    rp_page = RepositoryPage(nr_page.get_driver())
    global repository_url
    pytest.repo_url = rp_page.get_repo_url()
    pytest.selenium_webdriver = rp_page.get_driver()
    print( 'Repo URL:', pytest.repo_url )

################## git commit and push ###################################
@pytest.mark.order(6)
def test_push_file_to_origin():
    git_interactions.git_init()
    sleep(3)
    git_interactions.set_global_user(config['credentials']['email'])
    sleep(3)
    git_interactions.push_file_to_repo('config.ini', config['credentials']['name'],
    config['credentials']['password'], pytest.repo_url )

################### selenium get source code and compare ##################
@pytest.mark.order(7)
def test_checking_if_source_code_from_repo_is_identical_to_file():
    sleep(5)
    rp_page = RepositoryPage(pytest.selenium_webdriver)
    rp_page.get_driver().refresh()
    rp_page.open_file('config.ini')
    source_code = rp_page.get_raw_source_code_of_selected_element()
    with open ('config.ini', 'r') as f:
        file_content_read=f.read()

    assert source_code == file_content_read

#################### delete docker container ######################
@pytest.mark.order(8)
def test_gitea_container_delete(get_password):
    exit_code = gitea_docker.stop_gitea_docker(container_id=container_id, sudo_password=get_password)
    print('Gitea delete container exit_code:', exit_code)
