from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


options = Options()
options.add_argument('--no-sandbox')  # Bypass OS security model
options.add_argument('--user-data-dir=/home/vanle/.config/google-chrome/Profile 4')
driver = webdriver.Chrome(executable_path='../libs/chromedriver', options=options)


link_format = "https://www.facebook.com/phanboncamau/posts/2908192912830269"
# driver.get(shared_constant.FBURL)

driver.get(link_format)
sleep(5)
# between scrolls
# Scroll down to bottom
# driver.execute_script(
#     "window.scrollTo(0, document.body.scrollHeight);")
#
# # Wait to load page
# sleep(2)

script_execute = """const id = 'bp9cbjyn j83agx80 buofh1pr ni8dbmo4 stjgntxs';
const yOffset = -250;
const element = document.getElementsByClassName(id)[0];
const y = element.getBoundingClientRect().top + window.pageYOffset + yOffset;

window.scrollTo({top: y, behavior: 'smooth'});"""
driver.execute_script(script_execute)
sleep(2)
html = driver.find_element_by_xpath("(//span[@class='d2edcug0 hpfvmrgz qv66sw1b c1et5uql b0tq1wua a8c37x1j keod5gw0 nxhoafnm aigsh9s9 d9wwppkn fe6kdd0r mau55g9w c8b282yb hrzyx87i jq4qci2q a3bd9o3v knj5qynh m9osqain'])[1]")
html.click()
html.click()
print('clicked---')

sleep(10)
share = driver.find_element_by_xpath("(//span[contains(@class,'d2edcug0 hpfvmrgz qv66sw1b c1et5uql b0tq1wua a8c37x1j keod5gw0 nxhoafnm aigsh9s9 d9wwppkn fe6kdd0r mau55g9w c8b282yb hrzyx87i jq4qci2q a3bd9o3v knj5qynh m9osqain')])[3]")
print(share.text)
share.click()
