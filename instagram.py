from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from random import random
import urllib
import getpass
import time
import os


def login_from_fb(b, username, password):
    login_username = b.find_element_by_id('email')
    login_password = b.find_element_by_id('pass')
    login_username.send_keys(username)
    login_password.send_keys(password)
    login_button = b.find_element_by_id('loginbutton')
    login_button.click()

def login_from_insta(b, username, password):
    login_username = b.find_elements_by_xpath('//input')[0]
    login_password = b.find_elements_by_xpath('//input')[1]
    login_username.send_keys(username)
    login_password.send_keys(password)
    log_in = b.find_element_by_xpath('//button[contains(text(), "Log in")]')
    log_in.click()
login_via_fb = raw_input("If you want to login via Facebook press y/Y else login via instagram credentials by pressing n/N: ")

if login_via_fb.lower() == 'y':
    username = raw_input("Enter your Facebook username: ")
    password = getpass.getpass("Enter your Facebook password: ")
    password_match = getpass.getpass("Enter your Facebook password again: ")
else:
    username = raw_input("Enter your Instagram username: ")
    password = getpass.getpass("Enter your Instagram password: ")
    password_match = getpass.getpass("Enter your Instagram password again: ")

while (password != password_match):
    password = getpass.getpass("Your password did NOT match. Please enter your password again: ")
    password_match = getpass.getpass("Enter your password again: ")


'''
CREATING FOLDER WITH THE NAME OF THE
PERSON YOU WANT TO DOWNLOAD PICTURES OF
'''
friend = raw_input("Enter the username of the person you want to like and download all the photos of: ")
if os.path.exists(friend):
    folder_name = raw_input("The folder with the name '" + friend + "' already exists. Enter the name of folder you want to save all photos to: ")
    while os.path.exists(folder_name):
        folder_name = raw_input("The folder with the name '" + folder_name + "' also exists. Enter the name of folder you want to save all photos to: ")

else:
    folder_name = friend

os.mkdir(folder_name)

b = webdriver.Firefox()
b.implicitly_wait(5)
b.get('http://instagram.com')

'''
FINDING THE LOGIN BUTTON TO GO TO THE LOGIN PAGE
'''
if login_via_fb.lower() == 'y':
        try:
            log_in = WebDriverWait(b, 20).until(
                EC.presence_of_element_located((By.XPATH, '//button[contains(text(), "Facebook")]'))
                )
        except:
            b.quit()
        log_in.click()

else:
    try:
        log_in = WebDriverWait(b, 20).until(
            EC.presence_of_element_located((By.XPATH, '//a[contains(text(), "Log in")]'))
            )
    except:
        b.quit()
    log_in.click()


'''
CALLING THE LOGIN FUNCTION DEPENDING UPON THE
USER PREFERENCE OF LOGIN VIA FB OR INSTA
'''
if login_via_fb.lower() == 'y':
    login_from_fb(b, username, password)
else:
    login_from_insta(b, username, password)

time.sleep(5)

'''
GOING TO THE PROFILE OF THE SPECIFIED USER
'''
b.get('http://instagram.com/' + friend + '/')


'''
LOADING MORE PICTURES IN THEIR PROFILE
'''
try:
    load_more = WebDriverWait(b, 10).until(
        EC.presence_of_element_located((By.XPATH, '//a[contains(text(), "Load more")]'))
        )
    load_more.click()
except:
    pass

last_height = b.execute_script("return document.body.scrollHeight")
while True:
    b.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)
    new_height = b.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height


b.execute_script("window.scrollTo(0, 0);")
'''
all IS THE VARIABLE NAME THAT IS THE DIV THAT CONTAINS ALL THE PICTURES
'''
all = b.find_element_by_xpath('//article/div/div')
def do(b, all):
    pictures = all.find_elements_by_xpath('./div/div')
    for pic in pictures:
        pic.click()
        time.sleep(1)

        #TRY IF YOU GET A VIDEO OR ELSE DOWNLOAD THE IMAGE.
        try:
            src =  b.find_element_by_xpath('//article/div/div/div/div//video').get_attribute('src')
            urllib.urlretrieve(src, os.getcwd() + '/' + folder_name + '/' + src.split('/')[-1])
        except:
            src =  b.find_element_by_xpath('//article/div/div/div/div/img').get_attribute('src')
            urllib.urlretrieve(src, os.getcwd() + '/' + folder_name + '/' + src.split('/')[-1])
        finally:
            pass


        try:
            liked = b.find_element_by_xpath('//article/div[2]/section[1]/a[1]/span[contains(text(), "Like")]')
            liked.click()
        except:
            pass

        text = b.find_element_by_xpath('//form/textarea')
        # REPLACE 'YOUR COMMENT' ON THE NEXT LINE WITH WHAT YOU WANT TO COMMENT
        # comment = raw_input("Enter what do you want to comment: ")
        # text.send_keys(str(random()) + Keys.RETURN)
        cross = b.find_element_by_xpath('//body/div[2]/div/button')
        cross.click()
do(b,all)
b.quit()
