from shared import constant as shareConstant
from mongo_driver import mongo_db as con

if (__name__ == '__main__'):
    dbConnect = con.Client(shareConstant.DBInfo['history'])
    print(dbConnect.client.list_database_names())
    dbConnect.disconnect()