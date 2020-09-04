from pymongo import MongoClient
from shared import constant as shareConstant


class Client:
    def __init__(self, dbInfo):
        uri_link = "mongodb://" + dbInfo['username'] + ":" + dbInfo['password'] \
                  + "@" + dbInfo['ip'] + ":" + dbInfo['port'] + "/" + dbInfo['db']
        self.client = MongoClient(uri_link)


    def disconnect(self):
        return self.client.close()

if (__name__ == '__main__'):
    dbConnect = Client(shareConstant.DBInfo['history'])
    print(dbConnect.client.database_names())
    dbConnect.disconnect()