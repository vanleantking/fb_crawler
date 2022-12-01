from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from shared import constant as shared_constant

if __name__ == '__main__':
    options = Options()
    options.add_argument('--no-sandbox')  # Bypass OS security model
    options.add_argument('--user-data-dir=/home/vanle/.config/google-chrome/Profile 4')
    driver = webdriver.Chrome(executable_path='../libs/chromedriver', options=options)

    driver.get(shared_constant.FBURL)
    # assert "Python" in driver.title
    username = shared_constant.UserNameFB
    password = shared_constant.PasswordFB
    elem = driver.find_element_by_id("email")
    elem.clear()
    elem.send_keys(username)
    sleep(50)

    passElem = driver.find_element_by_id("pass")
    passElem.clear()
    passElem.send_keys(password)
    passElem.send_keys(Keys.RETURN)
    sleep(60)
    # assert "No results found." not in driver.page_source
    driver.quit()
    driver.close()
