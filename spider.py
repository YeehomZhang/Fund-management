# 一个月运行一次，不要经常运行
from config import *
from bs4 import BeautifulSoup
from multiprocessing import Pool

import requests
import pymongo

codes_again = []

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB][MONGO_TABLE]


def get_codes():
    db2 = client[MONGO_DB][MONGO_TABLE_2]
    codes = db2.find_one({'_id':1})
    return codes['codes']

codes = get_codes()

def get_code_info(code, name, order):
    content = []
    url = 'http://fund.eastmoney.com/f10/F10DataApi.aspx?type=lsjz&code=' + str(code) + \
          '&per=3000&sdate=&edate=&rt=0.7823397557719116'
    response = requests.get(url)
    html = response.text
    html_bs = BeautifulSoup(html, 'lxml')
    items = html_bs.select('td')
    for i in range(0, len(items)+7, 7):
        content.append(items[-i]. text)
        content.append(items[-i+1]. text)
        content.append(items[-i+2]. text)
        content.append(items[-i+3]. text)
    data = {
        '_id': code,
        'order':int(order/2),
        'name': name,
        'content': content[4:],
    }
    save_to_mongodb(code, data, name)


def save_to_mongodb(code, data, name):
    if db.save(data):
        print(code, name, 'successful')
    else:
        None



def main(order):
    global codes_again
    try:
        get_code_info(codes[order], codes[order+1], order)
    except:
        try:
            get_code_info(codes[order], codes[order + 1], order)
        except:
            print('---失败', codes[order], codes[order + 1])


if __name__ == '__main__':
    pool = Pool(5)
    pool.map(main, [order for order in range(0, len(codes), 2)])
