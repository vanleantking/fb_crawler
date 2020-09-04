from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from Shared import constant as shared_constant

if __name__ == '__main__':
    options = Options()
    options.add_argument("--user-data-dir=../profile/default")
    driver = webdriver.Chrome(executable_path='../libs/chromedriver', options=options)

    driver.get(shared_constant.FBURL)
    # assert "Python" in driver.title
    username = shared_constant.UserNameFB
    password = shared_constant.PasswordFB
    elem = driver.find_element_by_id("email")
    elem.clear()
    elem.send_keys(username)
    sleep(5)

    passElem = driver.find_element_by_id("pass")
    passElem.clear()
    passElem.send_keys(password)
    passElem.send_keys(Keys.RETURN)
    sleep(60)
    # assert "No results found." not in driver.page_source
    driver.close()
