""" Utility packages for instagram-automation. """
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def login_from_fb(browser_obj, username, password):
    """ If a user wants to login to instagram via facebook. """

    get_login_page('facebook', browser_obj)
    login_username = browser_obj.find_element_by_id('email')
    login_password = browser_obj.find_element_by_id('pass')
    login_username.send_keys(username)
    login_password.send_keys(password)
    login_button = browser_obj.find_element_by_id('loginbutton')
    login_button.click()


def login_from_insta(browser_obj, username, password):
    """  If a user wants to login using their instagram credentials. """

    get_login_page('instagram', browser_obj)
    login_username, login_password, *_ = browser_obj.find_elements_by_xpath('//input')
    login_username.send_keys(username)
    login_password.send_keys(password)
    log_in = browser_obj.find_element_by_xpath('//button[contains(text(), "Log in")]')
    log_in.click()


def get_login_page(login_method, browser_obj):
    """ W.R.T the login_method find and click on the login button """

    if login_method == 'facebook':
        try:
            log_in = WebDriverWait(browser_obj, 15).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//button[contains(text(), "Facebook")]'))
            )
        except BaseException:
            browser_obj.quit()
        log_in.click()

    else:
        try:
            log_in = WebDriverWait(browser_obj, 15).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//a[contains(text(), "Log in")]'))
            )
        except BaseException:
            browser_obj.quit()
        log_in.click()
        time.sleep(5)
