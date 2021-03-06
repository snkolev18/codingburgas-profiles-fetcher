from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import sys
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import pyfiglet
import argparse
import git

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--log-level=3')

parser = argparse.ArgumentParser(description='A python script to fetch codingburgas students\' profiles')
parser.add_argument("-u", "--github_username", help="That is your github username", default=git.get_uname())
parser.add_argument("-p", "--github_password", help="That is your github password", required=True)
parser.add_argument("-me", "--microsoft_email", help="Your Microsoft email", default=git.get_uemail())
parser.add_argument("-mp", "--microsoft_password", help="Password for your microsoft account", required=True)
args = parser.parse_args()

print(pyfiglet.figlet_format("Welcome to codingburgas profiles extractor"))

driver = webdriver.Chrome(ChromeDriverManager().install())

driver.get("https://github.com/login")

def getStudentsInPage(page_num, students_class):
    print("Students from class {} at page {}:".format(students_class, page_num))
    driver.get("https://github.com/orgs/codingburgas/people?page={}".format(page_num))
    links = driver.find_elements_by_xpath("//a[@href]")
    for link in links:
        current_profile = str(link.get_attribute("href"))
        if students_class in current_profile:
            print(current_profile)

print(driver.title)

userBox = driver.find_element_by_id("login_field")
#userBox.send_keys(input("Enter your username: "))
userBox.send_keys(args.github_username)
passwdBox = driver.find_element_by_id("password")
#passwdBox.send_keys(input("Enter your password: "))
passwdBox.send_keys(args.github_password)

try:
    login = driver.find_element_by_xpath("//input[@type='submit' and @value='Sign in']")
    login.click()
finally:
    time.sleep(2)
    print(driver.current_url)

driver.get("https://github.com/codingburgas")

try:
    button_element = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.TAG_NAME, "button")))
    button_element.click()
finally:
    time.sleep(3.5)

email = driver.find_element_by_id("i0116")
email.send_keys(args.microsoft_email)

try:
    next = driver.find_element_by_xpath("//input[@type='submit' and @value='Next']")
    next.click()
finally:
    time.sleep(3.5)

passwd = driver.find_element_by_id("i0118")
passwd.send_keys(args.microsoft_password)

try:
    next = driver.find_element_by_xpath("//input[@type='submit' and @value='Sign in']")
    next.click()
finally:
    time.sleep(3.5)

try:
    next = driver.find_element_by_xpath("//input[@type='button' and @value='No']")
    next.click()
finally:
    time.sleep(3.5)

driver.get("https://github.com/orgs/codingburgas/people")

max_page_num = 8
current_page_num = 1

student_class = input("Enter the class of the students that you want to fetch: ")

while current_page_num <= max_page_num:
    getStudentsInPage(current_page_num, student_class)
    current_page_num += 1
driver.quit()
