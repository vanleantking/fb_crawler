from selenium import webdriver
import time
import re
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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
    feed = browser_driver.find_element(By.XPATH,
                                       "(//div[contains(@class,'x6s0dn4 x78zum5 xdt5ytf x193iq5w x1t2pt76 xh8yej3')])")
    fb_posts = feed.find_elements(By.XPATH, "(//div[contains(@class, 'x1yztbdb x1n2onr6 xh8yej3 x1ja2u2z')])")
    print(len(fb_posts))
    if len(fb_posts) == 0:
        return
    single_post = fb_posts[0]

    # inside_post_info
    # include[fb_info, fb_contents(fb_post_content, fb_post_images), fb_comments]
    inside_post_info = single_post.find_element(By.XPATH,
                                                "(//div[contains(@class, 'x9f619 x1n2onr6 x1ja2u2z x2bj2ny x1qpq9i9 xdney7k xu5ydu1 xt3gfkd xh8yej3 x6ikm8r x10wlt62 xquyuld')])")

    # get facebook name & & facebook post time
    fb_info = inside_post_info.find_elements(By.XPATH,
                                             "(//div[contains(@class, 'x1cy8zhl x78zum5 x1q0g3np xod5an3 x1pi30zi x1swvt13 xz9dl7a')])")
    for idx, elm in enumerate(fb_info):
        try:
            fb_post_content = elm.find_element(By.CLASS_NAME,
                                               "x1iorvi4 x1pi30zi x1l90r2v x1swvt13")
            print('fb_post_content', fb_post_content, fb_post_content.get_attribute("innerText"))
        except NoSuchElementException:
            pass
        print('fb_info, ', idx, elm, elm.get_attribute("innerText"))
    # fb_info_name = inside_post_info.find_element(By.XPATH,
    #     "(//div[contains(@class, 'x1cy8zhl x78zum5 x1q0g3np xod5an3 x1pi30zi x1swvt13 xz9dl7a')])[0]")
    # fb_info_post_time = inside_post_info.find_element(By.XPATH,
    #     "(//div[contains(@class, 'x1cy8zhl x78zum5 x1q0g3np xod5an3 x1pi30zi x1swvt13 xz9dl7a')])[1]")

    # print('fb_info_name ', fb_info_name.text)
    # print('fb_info_post_time ', fb_info_post_time.text)

    # fb_contents
    # fb_post_content
    # fb_post_content = fb_info.find_element(By.CLASS_NAME,
    #                                                 "x1iorvi4 x1pi30zi x1l90r2v x1swvt13")
    # print('fb_post_content, ', fb_post_content, fb_post_content.text)
    # inside_fb_content = fb_post_content.find_element(By.XPATH,
    #                                                  "(//span[contains(@class, 'x193iq5w xeuugli x13faqbe x1vvkbs xlh3980 xvmahel x1n0sxbx x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x4zkp8e x3x7a5m x6prxxf xvq8zen xo1l8bm xzsf02u x1yc453h')])")
    # print('inside_fb_content, ', inside_fb_content.text)

    # js_get_page_info = '''
    # // inside_post_info include [fb_info, fb_contents(fb_post_content, fb_post_images), fb_comments]
    #     var inside_post_info = single_post.getElementsByClassName('x9f619 x1n2onr6 x1ja2u2z x2bj2ny x1qpq9i9 xdney7k xu5ydu1 xt3gfkd xh8yej3 x6ikm8r x10wlt62 xquyuld')[0];
    #
    #
    #     // get facebook name && facebook post time
    #     var fb_info = inside_post_info.getElementsByClassName('x1cy8zhl x78zum5 x1q0g3np xod5an3 x1pi30zi x1swvt13 xz9dl7a')[0];
    #     var fb_info_name = fb_info.getElementsByClassName('xu06os2 x1ok221b')[0];
    #     var fb_info_post_time = fb_info.getElementsByClassName('xu06os2 x1ok221b')[1];
    # '''
    # fb_post_images = browser_driver.execute_script(js_get_page_info);
    # fb_post_images <= this elements fb change each load pages = > find new way to get this element
    # fb_post_image = inside_post_info.find_element(By.ID, 'jsc_c_2c')
    # if len(fb_post_image) > 0:
    #     ahref = fb_post_image[0].getElementsByClassName('img')[0]
    #     print('images, ', ahref)

    # get fb comments summary
    fb_post_comments = inside_post_info.find_element(By.XPATH,
                                                     "//div[contains(@class, 'x168nmei x13lgxp2 x30kzoy x9jhf4c x6ikm8r x10wlt62')]")
    reactions_comments_summaries = fb_post_comments.find_element(By.XPATH,
                                                                 "//div[contains(@class, 'x6s0dn4 xi81zsa x78zum5 x6prxxf x13a6bvl xvq8zen xdj266r xktsk01 xat24cr x1d52u69 x889kno x4uap5 x1a8lsjc xkhd6sd xdppsyt')]")
    total_reactions = reactions_comments_summaries.find_element(By.XPATH,
                                                                "//div[contains(@class, 'x6s0dn4 x78zum5 x1iyjqo2 x6ikm8r x10wlt62')]")
    print('total_reactions, ', total_reactions, total_reactions.get_attribute("innerText"))
    comment_summaries = reactions_comments_summaries.find_element(By.XPATH,
                                                                  "//div[contains(@class, 'x6s0dn4 x78zum5 x2lah0s x17rw0jw')]")
    print('comment_summaries, ', comment_summaries, comment_summaries.get_attribute("innerText"))

    # get fb comment content only
    fb_comments_only = fb_post_comments.find_element(By.XPATH,
                                                     "//div[contains(@class, 'x1jx94hy x12nagc')]")
    print('fb_comments_only, ', fb_comments_only, fb_comments_only.get_attribute("innerText"))

    # this call click for get the menu option on comments, include [the mnost relevant comments, the newest comments, all comments]
    try :
        click_option_view_cmt = fb_comments_only.find_element(By.XPATH,
                                                         "//div[contains(@class, 'x78zum5 x13a6bvl xexx8yu x1pi30zi x18d9i69 x1swvt13 x1n2onr6')]")
        span_click_option_view_cmt = click_option_view_cmt.find_element(By.XPATH,
                                                         "//span[contains(@class, 'x193iq5w xeuugli x13faqbe x1vvkbs xlh3980 xvmahel x1n0sxbx x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x4zkp8e x3x7a5m x6prxxf xvq8zen x1s688f xi81zsa')][contains(.,'Phù hợp nhất')]");
        print('click_option_view_cmt, ', click_option_view_cmt)
        print('span_click_option_view_cmt, ', span_click_option_view_cmt, span_click_option_view_cmt.is_displayed(), span_click_option_view_cmt.is_enabled())
        print(ActionChains(browser_driver).move_to_element(span_click_option_view_cmt))
        print(browser_driver.execute_script("console.log(arguments[0]);", span_click_option_view_cmt))
        print(browser_driver.execute_script("arguments[0].click();", span_click_option_view_cmt))
        time.sleep(20)

        menu_opt_choice_all = browser_driver.find_element(By.XPATH,
            "//span[contains(@class, 'x193iq5w xeuugli x13faqbe x1vvkbs xlh3980 xvmahel x1n0sxbx x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x4zkp8e x3x7a5m x6prxxf xvq8zen xk50ysn xzsf02u x1yc453h')][contains(.,'Tất cả bình luận')]")
        print('menu_opt_choice_all, ', menu_opt_choice_all)
        print(ActionChains(browser_driver).move_to_element(menu_opt_choice_all))
        print(browser_driver.execute_script("console.log(arguments[0]);", menu_opt_choice_all))
        print(browser_driver.execute_script("arguments[0].click();", menu_opt_choice_all))
        time.sleep(10)
        browser_driver.implicitly_wait(10)
        span_click = WebDriverWait(driver, 15).until(
            lambda wd: wd.find_element(By.XPATH,
                                                        "//span[contains(@class, 'x193iq5w xeuugli x13faqbe x1vvkbs xlh3980 xvmahel x1n0sxbx x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x4zkp8e x3x7a5m x6prxxf xvq8zen x1s688f xi81zsa')][contains(.,'bình luận')]"))

        # span_click = click_option_view_cmt.find_element(By.XPATH,
        #                                                 "//span[contains(@class, 'x193iq5w xeuugli x13faqbe x1vvkbs xlh3980 xvmahel x1n0sxbx x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x4zkp8e x3x7a5m x6prxxf xvq8zen x1s688f xi81zsa')][contains(.,'bình luận')]")
        print('span_click, ', span_click)
        print("Element is visible? " + str(span_click.is_displayed()))
        print(ActionChains(browser_driver).move_to_element(span_click))
        print(browser_driver.execute_script("console.log(arguments[0]);", span_click))
        print(browser_driver.execute_script("arguments[0].click();", span_click))

        browser_driver.implicitly_wait(15)
        #  click on the view all comments agains
        menu_opt_choice_all2 = browser_driver.find_element(By.XPATH,
                                                          "//span[@class='x193iq5w xeuugli x13faqbe x1vvkbs xlh3980 xvmahel x1n0sxbx x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x4zkp8e x3x7a5m x6prxxf xvq8zen xk50ysn xzsf02u x1yc453h'][contains(.,'Tất cả bình luận')]")
        print('menu_opt_choice_all, ', menu_opt_choice_all2)
        print(ActionChains(browser_driver).move_to_element(menu_opt_choice_all2))
        print(browser_driver.execute_script("console.log(arguments[0]);", menu_opt_choice_all2))
        print(browser_driver.execute_script("arguments[0].click();", menu_opt_choice_all2))

        time.sleep(20)

        # print(span_click.click())

        # print(span_click.click())
    except Exception as exp:
        print('ooop, something not as expected, ', exp)

    time.sleep(10)
    browser_driver.implicitly_wait(15)
    WebDriverWait(browser_driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'x1jx94hy x12nagc')]")))
    # fb_comments_only = fb_post_comments.find_element(By.XPATH,
    #                                                  "//div[contains(@class, 'x1jx94hy x12nagc')]")
    print('fb_comments_only, ', fb_comments_only, fb_comments_only.get_attribute("innerText"))
    time.sleep(300)


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
