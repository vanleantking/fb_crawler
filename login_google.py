from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.chrome.options import Options
# from shared import constant as shared_constant

if __name__ == '__main__':
    options = Options()
    options.add_argument("--user-data-dir=profile")
    # options.add_argument("--user-data-dir=/Users/vanlecs/Library/Application Support/Google/Chrome")
    options.add_argument("--profile-directory=Default")
    options.add_argument('--no-sandbox')
    # options.add_argument('--headless')
    # options.add_argument('--no-sandbox')
    options.add_argument("--disable-blink-features=AutomationControllered")
    options.add_experimental_option('useAutomationExtension', False)
    prefs = {"profile.default_content_setting_values.notifications": 2}
    options.add_experimental_option("prefs", prefs)
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument("--start-maximized")  # open Browser in maximized mode
    options.add_argument("--disable-dev-shm-usage")  # overcome limited resource problems
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument('disable-infobars')
    # options.exclude_switches('enable-automation')
    # options.add_experimental_option('excludeSwitches', ['load-extension', 'enable-automation'])
    driver = webdriver.Chrome(executable_path='libs/chromedriver-mac-arm64/chromedriver', options=options)

    driver.get("https://accounts.google.com/v3/signin/identifier?continue=https%3A%2F%2Fwww.google.com%2Fsearch%3Fq%3DThis%2Bbrowser%2Bor%2Bapp%2Bmay%2Bnot%2Bbe%2Bsecure.%2BLearn%2Bmore%2BTry%2Busing%2Ba%2Bdifferent%2Bbrowser.%2BIf%2Byou%25E2%2580%2599re%2Balready%2Busing%2Ba%2Bsupported%2Bbrowser%252C%2Byou%2Bcan%2Btry%2Bagain%2Bto%2Bsign%2Bin.%26sourceid%3Dchrome%26ie%3DUTF-8&ec=GAZAAQ&hl=vi&ifkv=ASKXGp2fVx9ATx7yITSFSAJYiUnigYukNjiM6s7k-hWWW_enF-_Wl2xJXU8DRrysmJqMM6BOtlePPQ&passive=true&flowName=GlifWebSignIn&flowEntry=ServiceLogin&dsh=S-1526665121%3A1703748761882266&theme=glif")

    # assert "Python" in driver.title
    # username = shared_constant.UserNameFB
    # password = shared_constant.PasswordFB
    sleep(5)
    elem = driver.find_element(By.ID, "identifierId")
    # elem.clear()
    elem.send_keys("kimtuyen.nguyen@brancherx.com")
    sleep(5)

    # passElem = driver.find_element(By.ID, "pass")
    # passElem.clear()
    # passElem.send_keys(password)
    # passElem.send_keys(Keys.RETURN)
    # sleep(60)
    # # assert "No results found." not in driver.page_source
    # driver.close()
