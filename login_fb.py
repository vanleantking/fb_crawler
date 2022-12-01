from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.chrome.options import Options
from shared import constant as shared_constant

if __name__ == '__main__':
    options = Options()
    options.add_argument("--user-data-dir=profile/default")
    driver = webdriver.Chrome(executable_path='libs/chromedriver', options=options)

    driver.get(shared_constant.FBURL)
    # assert "Python" in driver.title
    username = shared_constant.UserNameFB
    password = shared_constant.PasswordFB
    sleep(5)
    elem = driver.find_element(By.ID, "email")
    elem.clear()
    elem.send_keys(username)
    sleep(5)

    passElem = driver.find_element(By.ID, "pass")
    passElem.clear()
    passElem.send_keys(password)
    passElem.send_keys(Keys.RETURN)
    sleep(60)
    # assert "No results found." not in driver.page_source
    driver.close()
