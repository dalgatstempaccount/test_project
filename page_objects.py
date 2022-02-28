# -*- coding: utf-8 -*- 

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from configparser import ConfigParser

class BasePage:

    locators = ConfigParser()
    locators.read('locators.ini')

    def __init__(self, driver ):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def __getattr__(self, name):

        if(name.startswith('click_')):
            loc = self.locators[self.__class__.__qualname__][name.replace('click_', '', 1)]
            return lambda : self.find_clickable_element(loc).click()

        elif(name.startswith('send_keys_')):
            loc = self.locators[self.__class__.__qualname__][name.replace('send_keys_', '', 1)]
            return lambda text: self.find_element(loc).send_keys(text)
        
        elif(name.startswith('get_text_')):
            loc = self.locators[self.__class__.__qualname__][name.replace('get_text_', '', 1)]
            return lambda : self.find_element(loc).text
        
        elif(name.startswith('get_value_')):
            loc = self.locators[self.__class__.__qualname__][name.replace('get_value_', '', 1)]
            return lambda : self.find_element(loc).get_property('value')

        else:
            print('Unknown operation')

    def find_element(self, locator ):
        return self.wait.until( ec.presence_of_element_located((By.XPATH, locator)),
        message=f"Can't find element by locator {locator}")

    def find_clickable_element(self, locator ):
        return self.wait.until( ec.element_to_be_clickable((By.XPATH, locator)),
        message=f"Can't find element by locator {locator}")       

    def find_elements(self, locator ):
        return self.wait.until(ec.presence_of_all_elements_located((By.XPATH, locator)),
        message=f"Can't find elements by locator {locator}")

    def get_driver(self):
        return self.driver
    
class InstallConfiguration(BasePage):
    def configure(self, ssh_port=22):
        self.send_keys_ssh_port(ssh_port)
        self.click_install_button()

class LoginPage(BasePage):
    pass

class SignUpPage(BasePage):
    def sign_up( self, username=' ', email=' ', password=' ' ):
        self.send_keys_username(username)
        self.send_keys_email(email)
        self.send_keys_password(password)
        self.send_keys_retype_password(password)
        self.click_register_account_button()

class MainPage(BasePage):
    pass

class NewRepositoryPage(BasePage):
    def create_repository(self, repo_name):
        self.send_keys_repo_name(repo_name)
        # self.send_description(repo_desc)
        self.click_create_repo_button()

class RepositoryPage(BasePage):
    def get_repo_url(self):
        return self.get_value_repo_url()
    
    def open_file(self, filename):
        self.find_clickable_element('//a[@title=\'{}\']'.format(filename)).click()
    
    def get_raw_source_code_of_selected_element(self):
        self.click_view_raw()
        rv_page = FileRawViewPage(self.driver)
        return rv_page.get_text_preview()


class FileRawViewPage(BasePage):
    pass