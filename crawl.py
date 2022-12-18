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


def crawl_group_info(browser_driver):
    description = ''
    total_member = ''
    group_name = ''
    group_id = ''
    regexp_id = re.compile(r'id=(\d+)')

    group_link = 'https://www.facebook.com/groups/yeunhadep/about/'

    driver.get(group_link)
    time.sleep(10)

    # description
    try:
        description_elm = browser_driver.find_element(By.XPATH,
                                                      "(//div[contains(@class,'x9f619 x1n2onr6 x1ja2u2z x78zum5 xdt5ytf x2lah0s x193iq5w x1gslohp x12nagc xzboxd6 x14l7nz5')])[2]")
        print(description_elm.text)
        description = description_elm.text
    except NoSuchElementException:
        print('no element group description found')
        pass

    # group_name
    try:
        group_name_elm = browser_driver.find_element(By.XPATH, "(//a[@href='https://www.facebook.com/groups/yeunhadep/'])[2]")
        group_name = group_name_elm.text
    except NoSuchElementException:
        print('no element group name found')

    # group_id
    try:
        priceValue = browser_driver.find_element(By.XPATH, "//meta[@property='al:ios:url']")
        print('content id group, ', priceValue.get_attribute('content'))
        content = priceValue.get_attribute("content")
        content_groups = regexp_id.search(content)
        group_id = content_groups.group(1)
    except NoSuchElementException:
        print('no element group name found')
    print((group_name, description, group_id))

    # crawl total_member:
    browser_driver.get('https://www.facebook.com/groups/yeunhadep/members/')
    time.sleep(10)

    try:
        total_elm = browser_driver.find_element(By.XPATH, "(//span[contains(@class,'x1lliihq x6ikm8r x10wlt62 x1n2onr6')])[6]")
        print('total elm, ', total_elm.find_element(By.NAME, 'span'))
        total_member = total_elm.find_element(By.NAME, 'span').text
    except NoSuchElementException:
        print('no element group description found')
        pass

    return {
        'group_name': group_name,
        'description': description,
        'group_id': group_id,
        'total_member': total_member
    }


if __name__ == '__main__':
    options = Options()
    options.add_argument("--user-data-dir=profile/default")
    driver = webdriver.Chrome(executable_path='libs/chromedriver', options=options)

    #
    # # crawl group page info
    group_instance = crawl_group_info(driver)
    print('group instance info, ', group_instance)
    # dbConnect = con.Client(shareContants.DBInfo['history'])
    # db = dbConnect.client['loghistory']
    # groups_collection = db['fb_groups']
    # result = groups_collection.insert_one(group_instance)
    # print(result.inserted_id)
    # crawl_members_link(driver, group_instance['group_id'], dbConnect)

    driver.close()
