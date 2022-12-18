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

    # group_link = 'https://www.facebook.com/groups/yeunhadep/'
    group_link = 'https://www.facebook.com/tuyhoayoungofficial/'

    driver.get(group_link)
    time.sleep(30)
    # Get infinite scroll for get all post facebook feed height
    last_height = browser_driver.execute_script("return document.body.scrollHeight")

    idx = 0
    while True:
        idx += 1
        # Scroll down to bottom
        exe_result = browser_driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        print(exe_result)

        # Wait to load page
        time.sleep(10)

        # Calculate new scroll height and compare with last scroll height
        new_height = browser_driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        if idx == 5:
            break
    print('exit scroll, ')
    feed = browser_driver.find_element(By.XPATH, "(//div[contains(@class,'x6s0dn4 x78zum5 xdt5ytf x193iq5w x1t2pt76 xh8yej3')])")
    fb_posts = feed.find_elements(By.XPATH, "(//div[contains(@class, 'x1yztbdb x1n2onr6 xh8yej3 x1ja2u2z')])")
    print(len(fb_posts))
    if len(fb_posts) == 0:
        return
    single_post = fb_posts[0]
    # feed_content = single_post.find_element(By.ID, 'jsc_c_2b')
    # print('feed content by id, ', feed_content.length)
    # if feed_content.length > 0:
    #     print(feed_content)


    # inside_post_info
    # include[fb_info, fb_contents(fb_post_content, fb_post_images), fb_comments]
    inside_post_info = single_post.find_element(By.XPATH,
        "(//div[contains(@class, 'x9f619 x1n2onr6 x1ja2u2z x2bj2ny x1qpq9i9 xdney7k xu5ydu1 xt3gfkd xh8yej3 x6ikm8r x10wlt62 xquyuld')])")

    # get facebook name & & facebook post time
    fb_info = inside_post_info.find_elements(By.XPATH,
        "(//div[contains(@class, 'x1cy8zhl x78zum5 x1q0g3np xod5an3 x1pi30zi x1swvt13 xz9dl7a')])")
    for idx, elm in enumerate(fb_info):

        print('fb_info, ',idx, elm, elm.text)
    # fb_info_name = inside_post_info.find_element(By.XPATH,
    #     "(//div[contains(@class, 'x1cy8zhl x78zum5 x1q0g3np xod5an3 x1pi30zi x1swvt13 xz9dl7a')])[0]")
    # fb_info_post_time = inside_post_info.find_element(By.XPATH,
    #     "(//div[contains(@class, 'x1cy8zhl x78zum5 x1q0g3np xod5an3 x1pi30zi x1swvt13 xz9dl7a')])[1]")


        # print('fb_info_name ', fb_info_name.text)
        # print('fb_info_post_time ', fb_info_post_time.text)

    # fb_contents
    # fb_post_content
    fb_post_content = inside_post_info.find_element(By.XPATH,
        "(//div[contains(@class, 'x1iorvi4 x1pi30zi x1l90r2v x1swvt13')])")
    print('fb_post_content, ', fb_post_content, fb_post_content.text)
    inside_fb_content = fb_post_content.find_element(By.XPATH, "(//span[contains(@class, 'x193iq5w xeuugli x13faqbe x1vvkbs xlh3980 xvmahel x1n0sxbx x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x4zkp8e x3x7a5m x6prxxf xvq8zen xo1l8bm xzsf02u x1yc453h')])")
    print('inside_fb_content, ', inside_fb_content.text)

    # fb_post_images <= this elements fb change each load pages = > find new way to get this element
    # fb_post_image = inside_post_info.find_element(By.ID, 'jsc_c_2c')
    # if len(fb_post_image) > 0:
    #     ahref = fb_post_image[0].getElementsByClassName('img')[0]
    #     print('images, ', ahref)


    # get fb comments
    fb_post_comments = inside_post_info.find_element(By.XPATH,
        "(//div[contains(@class, 'x168nmei x13lgxp2 x30kzoy x9jhf4c x6ikm8r x10wlt62')])")
    reactions_comments_summaries = fb_post_comments.find_element(By.XPATH,
        "(//div[contains(@class, 'x6s0dn4 xi81zsa x78zum5 x6prxxf x13a6bvl xvq8zen xdj266r xktsk01 xat24cr x1d52u69 x889kno x4uap5 x1a8lsjc xkhd6sd xdppsyt')])")
    total_reactions = reactions_comments_summaries.find_element(By.XPATH,
        "(//div[contains(@class, 'x6s0dn4 x78zum5 x1iyjqo2 x6ikm8r x10wlt62')])")
    print('total_reactions, ', total_reactions)
    comment_summaries = reactions_comments_summaries.find_element(By.XPATH,
        "(//div[contains(@class, 'x6s0dn4 x78zum5 x2lah0s x17rw0jw')])")
    print('comment_summaries, ', comment_summaries)


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
