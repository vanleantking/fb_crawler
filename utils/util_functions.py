from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

def get_driver(profile_path = '', execution_path = ''):
    options = Options()
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    if profile_path != '':
        options.add_argument("--user-data-dir=" + profile_path)
    
    driver = webdriver.Chrome(executable_path=execution_path, options=options)
    return driver