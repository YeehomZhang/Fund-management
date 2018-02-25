from config import *

import matplotlib.animation as animation
from PIL import Image
import matplotlib.pyplot as plt
import pylab as pl
import pymongo
import datetime



client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB][MONGO_TABLE]


class get_information(object):

    def by_id(id):
        results = db.find_one({'_id':str(id)})
        return results

    def by_order(order):
        results = db.find_one({'order':int(order)})
        return results

    def by_name(name):
        results = db.find_one({'name': name})
        return results

class analysis(object):


    def by_one_value(day, id = None, order = None, name = None):
        if id:
            results = db.find_one({'_id':str(id)})
        elif order:
            results = db.find_one({'order':int(order)})
        elif name:
            results = db.find_one({'name': name})
        else:
            print('please check the id or order or name')
            return None
        try:
            order_day = results['content'].index(day)
            value = results['content'][order_day+3]
            print(value)
        except:
            print('please check the day')
            return None


    def analy_one(days_buy=7 ,days_sale=5,days_keep=90, buy_value_growth = None, sale_value_growth = None,id = None, order = None, name = None):
        if id:
            results = db.find_one({'_id':str(id)})
        elif order:
            results = db.find_one({'order':int(order)})
        elif name:
            results = db.find_one({'name': name})
        else:
            print('please check the id or order or name')
            return None
        data = results['content']
        count_i = 0
        count_j = 0
        count_k = 0
        for i in range(max(days_buy,days_sale)*4,len(data),4):
            try:
                # print('i=',i)
                date_buy = datetime.datetime.strptime(data[i],'%Y-%m-%d')
                value_buy = float(data[i+2])
                #print('now',value_now)
                value_before = float(data[i+2-4*days_buy])
                #print('before',value_before)
                value_growth_day0 = float(data[i+3].replace('%',''))
                #value_growth_day1 = float(data[i+3-4])
                #value_growth_day2 = float(data[i+3-8])
                growth = (value_buy - value_before)/value_before*100
                if growth<-11 and value_growth_day0>0 :
                    count_i = count_i + 1
                    print('buy', date_buy,',', growth,',\t', value_buy, ',\t',value_growth_day0, end='\t \t \t')
                    for j in range(i,len(data),4):
                        date_sale = datetime.datetime.strptime(data[j], '%Y-%m-%d')
                        value_sale = float(data[j+2])
                        growth_sale =(value_sale - value_buy)/value_buy*100
                        days = (date_sale - date_buy).days
                        if growth_sale>8:
                            count_j = count_j + 1
                            if days < days_keep:
                                count_k = count_k + 1
                            print('sale',date_sale,',',value_sale,',',growth_sale,days, end='\n')
                            break
            except:
                None
        print(count_i,count_j,count_j/count_i,int(count_k/count_i*100)/100)










# 有待完善，更加人性化
    def show_trend(x, y):
        pl.plot(x,y)
        pl.show()





