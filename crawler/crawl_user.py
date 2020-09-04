from crawler.user_profile import UserCrawler
import time
from utils.util_functions import get_driver
from shared import constant as shareContants
from mongo_driver import mongo_db as con

if __name__ == '__main__':
    driver = get_driver(profile_path='profile/default', execution_path='../libs/chromedriver')
    dbConnect = con.Client(shareContants.DBInfo['history'])
    db = dbConnect.client['loghistory']
    users_collection = db['facebook_users']
    user_process = users_collection.find(
        {
            "status": 0
        },
        {
            "facebook_url": 1,
            "_id": 1
        }).limit(10)
    for url_profile in user_process:        
        group_crawl = UserCrawler(driver)
        group_crawl._driver.get(url_profile["facebook_url"])
        time.sleep(20)

        group_crawl.begin_crawl_user()
        user_info = {}
        user_info["overview"] = group_crawl.crawl_overview_tab()
        other_tabs = group_crawl.crawl_other_tabs()
        for tab, info in other_tabs.items():
            user_info[tab] = info
        
        user_checkin = group_crawl.check_in(url_profile["facebook_url"])

        result = users_collection.update_one(
            {"_id": url_profile["_id"]},
            {"$set": {
                "status": 1,
                "overview": user_info["overview"],
                "education": user_info["education"],
                "living": user_info["living"],
                "contact_info": user_info["contact_info"],
                "relationship": user_info["relationship"],
                "bio": user_info["bio"],
                "year_overview": user_info["year_overview"]}})
        print(result)
        time.sleep(10)