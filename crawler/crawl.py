from selenium import webdriver
import time
import re
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from mongo_driver import mongo_db as con
from shared import constant as shareContants
from utils.util_functions import get_driver

''' function on crawl group info '''
''' get user account from member in group, include {user_name, fb_url} '''
''' insert new record on relationship user_group: group_member(n-n) '''

class GroupCrawler:
    _driver: None

    def __init__(self, driver):
        self._driver = driver

    def crawl_members_link(self, group_id, db_connect):
        sections_link = [
            # 'members',
            # 'members_with_things_in_common',
            'friends',
            'local_members']
        for link_section in sections_link:
            link_format = shareContants.FBFormatLink.format(
                shareContants.FbGroupURL, group_id, link_section)
            print(link_format)

            time.sleep(2)
            self._driver.get(link_format)
            time.sleep(40)
            log_history_db = db_connect.client['loghistory']
            fb_users = log_history_db['facebook_users']
            users_group = log_history_db['group_member']

            user_url_pattern = re.compile(r'https?:\/\/(www\.)?facebook\.com\/[a-zA-Z0-9.]+(?:\?id=[0-9]+)?')
            member_id_pattern = re.compile(r'[&?]member_id=(\d+)')
            limit_insert = 1000
            # Get scroll height
            last_height = self._driver.execute_script("return document.body.scrollHeight")

            while True:
                # Scroll down to bottom
                exe_result = self._driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                print(exe_result)

                # Wait to load page
                time.sleep(30)

                # Calculate new scroll height and compare with last scroll height
                new_height = self._driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height
            print('exit scroll, ')
            try:
                friend_list = self._driver.find_elements_by_class_name("_gse")
                print('len friend list, ', len(friend_list))
                insert_user_bulks = []
                insert_gr_user_bulks = []
                for friend in friend_list:
                    # facebook_url user
                    try:
                        aElem = friend.find_elements_by_tag_name('a')
                        href = aElem[0].get_attribute('href')
                        title = aElem[0].get_attribute('title')
                        url_link = user_url_pattern.search(href).group()

                        # member_id
                        member_id_link = aElem[0].get_attribute('ajaxify')
                        print('user id text, ', member_id_link, member_id_pattern.search(member_id_link))
                        print(' user id parse, ', member_id_pattern.search(member_id_link).group(1))
                        member_id = member_id_pattern.search(member_id_link).group(1)
                        print("user info, ", title, href, url_link, member_id)
                        user = {
                            'user_name': title,
                            'facebook_url': url_link,
                            'facebook_id': member_id,
                            'status': 0
                        }
                        insert_user_bulks.append(user)
                        user_group = {
                            'group_id': group_id,
                            'member_id': member_id
                        }
                        insert_gr_user_bulks.append(user_group)
                        if len(insert_user_bulks) == limit_insert:
                            fb_users.insert_many(insert_user_bulks)
                            users_group.insert_many(insert_gr_user_bulks)
                            insert_gr_user_bulks = []
                            insert_user_bulks = []

                    except NoSuchElementException:
                        print('error')
                        pass

                if len(insert_user_bulks) > 0:
                    fb_users.insert_many(insert_user_bulks)
                    users_group.insert_many(insert_gr_user_bulks)

            except NoSuchElementException:
                print('error')


    def crawl_about_section(self, group_id):
        # regexp_id = re.compile(r'id=(\d+)')
        seo_name = re.compile(r'groups\/(.+)\/')
        link_format = shareContants.FBFormatLink.format(
            shareContants.FbGroupURL, group_id, 'about')

        self._driver.get(link_format)
        time.sleep(10)

        # seo_name
        try:
            seo_name_elm = self._driver.find_element_by_id('seo_h1_tag')
            content = seo_name_elm.find_element_by_tag_name('a').get_attribute('href')
            content_seo_name = seo_name.search(content).group(1)
        except NoSuchElementException:
            print('no element group name found')

        # description
        try:
            description_elm = self._driver.find_element_by_xpath("(//div[@role='heading'])[4]")
            print(description_elm.text)
            description = description_elm.text
        except NoSuchElementException:
            print('no element group description found')
            pass

        # group_name
        try:
            group_name_elm = self._driver.find_element_by_xpath(
                "//a[@href='/groups/" + content_seo_name + "/?ref=group_header']")
            group_name = group_name_elm.text
        except NoSuchElementException:
            print('no element group name found')

        # group_id
        # try:
        #     id_elm = browser_driver.find_element_by_xpath("//meta[@property='al:ios:url']")
        #     print('content id group, ', id_elm.get_attribute('content'))
        #     content = id_elm.get_attribute("content")
        #     content_groups = regexp_id.search(content)
        #     group_id = content_groups.group(1)
        # except NoSuchElementException:
        #     print('no element group name found')

        return group_name, description, content_seo_name


    def crawl_total_section(self, group_id):
        link_format = shareContants.FBFormatLink.format(
            shareContants.FbGroupURL, group_id, 'members')

        self._driver.get(link_format)
        time.sleep(10)
        total_member = ''

        try:
            total_elm = self._driver.find_element_by_xpath("(//div[@role='heading'])[2]")
            print('total elm, ', total_elm.find_element_by_tag_name('span'))
            total_member = total_elm.find_element_by_tag_name('span').text
        except NoSuchElementException:
            print('no element group description found')
            pass

        return total_member


    def crawl_group_info(self, group_id):

        (description, group_name, seo_name_content) = self.crawl_about_section(group_id)
        total_member = self.crawl_total_section(group_id)

        return {
            'group_name': group_name,
            'description': description,
            'group_id': group_id,
            'total_member': total_member,
            'seo_name_content': seo_name_content,
            'link_groups': shareContants.FbGroupURL + group_id,
            'status': 1
        }


if __name__ == '__main__':

    driver = get_driver(profile_path='/home/vanle/.config/google-chrome/Profile 4', execution_path='../libs/chromedriver')
    group_crawl = GroupCrawler(driver)

    #
    # # crawl group page info
    group_instance = group_crawl.crawl_group_info('134754313279963')
    print('group instance info, ', group_instance)
    # dbConnect = con.Client(shareContants.DBInfo['history'])
    # db = dbConnect.client['loghistory']
    # groups_collection = db['fb_groups']
    # result = groups_collection.insert_one(group_instance)
    # print(result.inserted_id)
    # crawl_members_link(driver, '134754313279963', dbConnect)

    driver.close()
