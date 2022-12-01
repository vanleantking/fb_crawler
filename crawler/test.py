from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--no-sandbox')  # Bypass OS security model
options.add_argument('--user-data-dir=/home/vanle/.config/google-chrome/Profile 4')
# options.add_argument('--profile-directory=/home/vanle/.config/google-chrome/Profile 4')
driver = webdriver.Chrome(executable_path='../libs/chromedriver', options=options)
driver.get('http://www.python.org')
print(driver.title)
driver.quit()