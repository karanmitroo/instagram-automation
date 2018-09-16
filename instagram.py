from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from comment_list import comment_list
import random
import urllib
import getpass
import time
import os

login_mode = input(
    "If you want to login via Facebook press y/Y else login via instagram credentials by pressing n/N: ")

login_method = 'facebook' if login_mode.lower == 'y' else 'instagram'

# Get the users username and password
username = input("Enter your {} username: ".format(login_method.upper()))
password = getpass.getpass("Enter your {} password: ".format(login_method.upper()))
password_match = getpass.getpass("Enter your {} password again: ".format(login_method.upper()))

# Keep getting the password until two consecutive inputs do NOT match
while password != password_match:
    password = getpass.getpass("Your password did NOT match. Please enter your password again: ")
    password_match = getpass.getpass("Please enter your password again: ")


'''
CREATING FOLDER WITH THE NAME OF THE
PERSON YOU WANT TO DOWNLOAD PICTURES OF
'''
friend_username = input("Enter the INSTAGRAM username of the person you want to like and download all the photos of: ")
folder_name = friend_username

# Check if the directory with the name already exists. If yes then ask for some other directory name.
if os.path.exists(folder_name):
    folder_name = input("The folder with the name '{}' already exists. "
                        "Enter the name of folder you want to save all photos to: ".format(friend_username))

    while os.path.exists(folder_name):
        folder_name = input("The folder with the name '{}' also exists. "
                            "Enter the name of folder you want to save all photos to: ".format(folder_name))

os.mkdir(folder_name)

b = webdriver.Chrome('/Users/karanmitroo/Downloads/chromedriver')
b.get('http://instagram.com')

'''
FINDING THE LOGIN BUTTON TO GO TO THE LOGIN PAGE
'''



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
        EC.presence_of_element_located(
            (By.XPATH, '//a[contains(text(), "Load more")]'))
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
    comment_counter = 0
    for pic in pictures:
        pic.click()

        # TRY IF YOU GET A VIDEO OR ELSE DOWNLOAD THE IMAGE.
        try:
            src = WebDriverWait(b, 2).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//article/div/div/div/div/div//video'))
            )
            src = src.get_attribute('src')
            urllib.urlretrieve(src, os.getcwd() + '/' +
                               folder_name + '/' + src.split('/')[-1])
        except:
            # FOUND TWO XPATHS FOR IMAGES. INSTAGRAM RANDOMLY PLACES PICTURE IN ONE OF THEM.
            try:
                src = WebDriverWait(b, 2).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//article/div/div/div/div/img'))
                )
            except:
                src = WebDriverWait(b, 2).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//article/div/div/div/div/div/img'))
                )
            src = src.get_attribute('src')
            urllib.urlretrieve(src, os.getcwd() + '/' +
                               folder_name + '/' + src.split('/')[-1])
        finally:
            pass

        try:
            liked = b.find_element_by_xpath(
                '//article/div[2]/section[1]/a[1]/span[contains(text(), "Like")]')
            liked.click()
        except:
            pass

        '''
        TO COMMENT ON PICS. WORKING BUT INSTA BLOCKS COMMENTS AFTER 5 PICS
        @TODO:
            ---> Comment on pics only after some interval of time.
        '''
        if comment_counter == 5:
            text = b.find_element_by_xpath('//form/textarea')
            comment = random.choice(comment_list[0])
            for i in range(1,len(comment_list)):
                comment += ' ' + random.choice(comment_list[i])
            # REPLACE 'YOUR COMMENT' ON THE NEXT LINE WITH WHAT YOU WANT TO COMMENT
            # comment = input("Enter what do you want to comment: ")
            text.send_keys(comment + Keys.RETURN)
            comment_counter = 0

        comment_counter += 1

        '''
        TO CLOSE THE IMAGE
        '''
        cross = b.find_element_by_xpath('//body//div/button[contains(text(), "Close")]')
        cross.click()


do(b, all)
b.quit()
