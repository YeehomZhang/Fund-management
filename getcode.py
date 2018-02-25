from bs4 import BeautifulSoup
from config import *

import requests
import pymongo

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB][MONGO_TABLE_2]

def get_all_code():
    codes = []
    url = 'http://www.1234567.com.cn/allfund.html'
    response = requests.get(url)
    response.encoding = 'GBK'
    html = response.text
    html_bs = BeautifulSoup(html, 'lxml').find_all(id = 'code_content')[0].select('li')
    for i in range(len(html_bs)):
        try:
            codes.append(html_bs[i].select('a')[0].text[1:7])
            codes.append(html_bs[i].select('a')[0].text[8:])
        except:
            None
    data = {
        '_id':1,
        'codes':codes,
    }
    db.save(data)
get_all_code()


