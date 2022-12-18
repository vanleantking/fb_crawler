from selenium import webdriver
import time
import re
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from mongo_driver import mongo_db as con
from shared import constant as shareContants

''' get user account from member in group, include {user_name, fb_url} '''
''' insert new record on relationship user_group: group_member(n-n) '''


def crawl_members_link(browser_driver, group_id, db_connect):
    sections_link = ['members', 'members_with_things_in_common', 'friends', 'local_members']
    for link_section in sections_link:
        link_format = "{}{}/{}".format(
            shareContants.FbGroupURL, group_id, link_section)
        print(link_format)

        time.sleep(10)
        browser_driver.get(link_format)
        time.sleep(20)
        log_history_db = db_connect.client['loghistory']
        fb_users = log_history_db['facebook_users']
        users_group = log_history_db['group_member']

        user_url_pattern = re.compile(r'https?:\/\/(www\.)?facebook\.com\/[a-zA-Z0-9.]+(?:\?id=[0-9]+)?')
        member_id_pattern = re.compile(r'[&?]member_id=(\d+)')
        limit_insert = 1000
        # Get scroll height
        last_height = browser_driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to bottom
            exe_result = browser_driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            print(exe_result)

            # Wait to load page
            time.sleep(20)

            # Calculate new scroll height and compare with last scroll height
            new_height = browser_driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        print('exit scroll, ')
        try:
            friend_list = browser_driver.find_elements_by_class_name("_gse")
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
                    member_id = member_id_pattern.search(member_id_link).group(1)
                    print("user info, ", title, href, url_link, member_id)
                    user = {
                        'user_name': title,
                        'facebook_url': url_link,
                        'facebook_id': member_id
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


def crawl_fb_page_feed(browser_driver):

    group_link = 'https://www.facebook.com/groups/yeunhadep/'

    driver.get(group_link)
    time.sleep(10)
    # Get infinite scroll for get all post facebook feed height
    last_height = browser_driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        exe_result = browser_driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        print(exe_result)

        # Wait to load page
        time.sleep(20)

        # Calculate new scroll height and compare with last scroll height
        new_height = browser_driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    print('exit scroll, ')


if __name__ == '__main__':
    options = Options()
    options.add_argument("--user-data-dir=profile/default")
    driver = webdriver.Chrome(executable_path='libs/chromedriver', options=options)

    #
    # # crawl group page info
    group_instance = crawl_fb_page_feed(driver)
    print('group instance info, ', group_instance)
    # dbConnect = con.Client(shareContants.DBInfo['history'])
    # db = dbConnect.client['loghistory']
    # groups_collection = db['fb_groups']
    # result = groups_collection.insert_one(group_instance)
    # print(result.inserted_id)
    # crawl_members_link(driver, group_instance['group_id'], dbConnect)

    driver.close()
