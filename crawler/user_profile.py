from selenium import webdriver
import time
import re
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from utils.util_functions import get_driver
from shared import constant as shareContants
from mongo_driver import mongo_db as con

''' crawl user info '''

class UserCrawler:

    _driver: None

    def __init__(self, driver):
        self._driver = driver

    # start from click on [about] tab
    def begin_crawl_user(self):
        try:
            userTab = shareContants.UserProfileTab.format(tab = "about")
            self._driver.implicitly_wait(10)
            element = WebDriverWait(self._driver, 10).until(
                EC.presence_of_element_located((By.XPATH, userTab))
            )
            print(element)
            element.click()
            time.sleep(5)
        except NoSuchElementException:
            pass

    # default section on click about is 'overview' tab
    def crawl_overview_tab(self):
        # data-overviewsection
        overview = {}
        user_sections = ["education", "places", "all_relationships", "contact_basic"]
        for user_section in user_sections:
            overview[user_section] = self.crawl_userinfo_section(user_section)
        return overview

    def check_in(self, url_profile):
        link_format = "{}/{}".format(
                url_profile, "places_recent")
        self._driver.get(link_format)
        self._driver.implicitly_wait(10)

        id_edu_elm = self._driver.find_element_by_xpath(
                shareContants.UserProfileSectionDetail.format(section_detail = "collection_wrapper"))

        checkin_details = id_edu_elm.find_elements_by_tag_name('li')
        return [checkin.text.strip().lower() for checkin in checkin_details]
        # for checkin in checkin_details:
        #     a_href = checkin.find_elements_by_tag_name('a')
        #     a_text = [a.get_attribute('href') for a in a_href]
        #     print('check in info, ', checkin.text, a_text)

    def crawl_other_tabs(self):
        sections_tab = [
            {
                'name': 'education',
                'tab': "/about?section=education",
                'id': ['eduwork'] #pagelet_edit_eduwork
            },
            {
                'name': 'living',
                'tab': "/about?section=living",
                'id': ['hometown']
            },
            {
                'name': 'contact_info',
                'tab': '/about?section=contact-info',
                'id': ['contact', 'basic']
            },
            {
                'name': 'relationship',
                'tab': '/about?section=relationship',
                'id': ['relationships']
            },
            {
                'name': 'bio',
                'tab': '/about?section=bio',
                'id': [
                    'bio',
                    'pronounce',
                    'nicknames',
                    'quotes',
                    'blood_donations']
            },
            {
                'name': 'year_overview',
                'tab': '/about?section=year-overviews',
                'id': ['timeline_app_collection']
            }
        ]
        sections = {}
        for section in sections_tab:
            sections[section['name']] = self.crawl_detail_tab(section)
        return sections


    def crawl_detail_tab(self, section):
        time.sleep(5)
        section_detail = {}
        section_tab = shareContants.UserProfileSectionTab.format(section_tab = section['tab'])
        print(section_tab)
        # element = self._driver.find_element_by_xpath(section_tab)
        self._driver.implicitly_wait(10)
        element = WebDriverWait(self._driver, 20).until(
            EC.presence_of_element_located((By.XPATH, section_tab)) #element_to_be_clickable
        )

        print(element)
        print("Element is visible? " + str(element.is_displayed()), section['tab'])

        # element.click()
        self._driver.execute_script("arguments[0].click();", element)

        time.sleep(20)

        for id_elm in section['id']:
            detail_id = {}
            id_edu_elm = self._driver.find_element_by_xpath(
                shareContants.UserProfileSectionDetail.format(section_detail = id_elm))
            roles_heading_declare = id_edu_elm.find_elements_by_xpath(
                shareContants.UserProfileSectionDeclares)
            fb_profile_experiences = id_edu_elm.find_elements_by_class_name(
                shareContants.UserProfileSectionFieldsDeclare)

            for idx, expr in enumerate(fb_profile_experiences):
                detail_id[roles_heading_declare[idx].text.lower()] = expr.text.lower()
            print('expr declare, ', expr.text)
            section_detail[id_elm] = detail_id
        print('education detail, ', section_detail)
        return section_detail

    def crawl_userinfo_section(self, user_section):
        eduHistory = []
        try:
            time.sleep(10)
            formatEdu = shareContants.UserProfileSection.format(section = user_section)
            print(formatEdu)
            ul_elms = self._driver.find_elements_by_xpath(formatEdu)
            eduHistory = [ul_elm.text.strip() for ul_elm in ul_elms]
            print("all education history, ", eduHistory)

        except NoSuchElementException:
            print("not found")
        return eduHistory





if __name__ == '__main__':
    driver = get_driver(profile_path='profile/default', execution_path='../libs/chromedriver')
    group_crawl = UserCrawler(driver)
    url_profile = "https://www.facebook.com/van.le.k3c1"

    group_crawl._driver.get(url_profile)
    time.sleep(20)

    group_crawl.begin_crawl_user()
    user_info = {}
    user_info["overview"] = group_crawl.crawl_overview_tab()
    other_tabs = group_crawl.crawl_other_tabs()
    for tab, info in other_tabs.items():
        user_info[tab] = info
    
    user_checkin = group_crawl.check_in(url_profile)
    print(user_checkin, user_info)
    # dbConnect = con.Client(shareContants.DBInfo['history'])
    # db = dbConnect.client['loghistory']
    # users_collection = db['facebook_users']

    # users_collection.update_one({_id: })

    time.sleep(2)

    driver.close()

