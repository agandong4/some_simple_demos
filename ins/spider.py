#!/usr/bin/env python
# encoding: utf-8
'''
@author: agandong4
@license: (C) Copyright 2013-2019, Node Supply Chain Manager Corporation Limited.
@contact: agandong4@gmail.com
@software: garner
@file: spider.py
@time: 2019-03-15 19:40
@desc:爬取INSTGRAM 上面的个人主页上的图片，ins上面有两种图片展示方法，一种是根据标签，另外一种是个人主页
本爬虫采取的就是后者.通过短标签'v1Nh3'，我们可以定位到图片链接
多进程池还不太熟悉，有待下次添加
图片名字还是以md5值命令，避免重复
采用的selenium进行模拟浏览器，流程：模拟翻页几次-->解析图片链接-->保存下载图片链接-->下载图片-->再次模拟
-->直到条件满足
满足条件有两，
1.下载图片张数
2.试错次数
'''
import os
import re
import time
import random
import requests
from requests import codes, ConnectionError
from requests.exceptions import ConnectTimeout, ReadTimeout
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from hashlib import md5
import pymongo


#mongoDB 的设置
MONGO_URL = 'localhost'
MONGO_DB = 'ins'
MONGO_TABLE = 'ayasa'
SUPERSTAR = 'ayasa'
client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]
#配置信息
NUMS = 40     #想要的图片数量
base_url ='https://www.instagram.com/ayasa_doya/'       #下载链接
# base_url = 'https://www.instagram.com/irene.rvelvet/'
# base_url = 'https://www.instagram.com/tvxq.official/'


def selenium_get(brower,total_sets):

    try:
        urls_set = set([])  # 集合保证了链接的唯一性
        for x in range(4*4):
            time.sleep(random.random())
            ActionChains(brower).send_keys(Keys.PAGE_DOWN).perform()
        time.sleep(random.random()+2)
        #定位图片链接
        divs = brower.find_elements_by_class_name('v1Nh3')
        for d in divs:
            urls_set.add(d.find_element_by_tag_name('a').get_attribute('href'))

        #获得新的图片链接集合
        new_sets = (urls_set | total_sets) - total_sets
    except:
        new_sets = set([])
    finally:
        return new_sets




def save_to_mongo(result):
    """
    存到mongoDB数据库中，同时返回Ture 或者False
    :param result:save img_url to mongoDB
    :return: boole value
    """
    if not db[MONGO_TABLE].find_one({'url':result}):
        db[MONGO_TABLE].insert_one({'url':result})
        print('successful restore the url to mongo db!', result)
        return True
    else:
        print('already have this url ,no need to insert!')
        return False

def save_img(content):
    """
    保存图片到本地
    :param content:
    :return:
    """
    file_path = '{0}/{1}/{2}.{3}'.format(os.getcwd(), SUPERSTAR, md5(content).hexdigest(), 'jpg')
    if not os.path.exists(file_path):
        # print("当前目录下有{}张图片".format(1+len(os.listdir(os.getcwd() + os.path.sep + SUPERSTAR))))
        print("save to local disk successful")
        with open(file_path, 'wb') as f:
            f.write(content)
            f.close()
    else:
        # print("当前目录下有{}张图片".format(1 + len(os.listdir(os.getcwd() + os.path.sep + SUPERSTAR))))
        print('aleady downloaded! continue')


def get_img_content(IMG_set):
    for i, item in enumerate(IMG_set):
        print('{:.1%} ----{}----{}'.format((i+1)/len(IMG_set),i+1,len(IMG_set)))    #进度条
        pattern2 = re.compile('display_url":"(.*?)","display_resources":')  # no nedd re.S
        IMG_html_text = requests.get(item).text
        display_url = re.search(pattern2, IMG_html_text)
        longurl = display_url.group(1)
        try:
            resp = requests.get(longurl, timeout=4)
            if resp.status_code == codes.ok:
                if not os.path.exists(os.getcwd() + os.path.sep + SUPERSTAR):
                    os.mkdir(os.getcwd() + os.path.sep + SUPERSTAR)
                    print("mkdir successfully")
                if save_to_mongo(longurl):
                    save_img(resp.content)
        except ConnectionError:
            print("request long_url wrong !", longurl)
            print("status_code", resp.status_code)
            continue
        except ConnectTimeout:
            print("requests time out!!!", longurl)
            continue
        except ReadTimeout:
            print("read time out !!!", longurl)
            continue
        except Exception as e:
            print('wrong ! please debug',e)
            continue

def main():
    total_sets = set([])
    brower = webdriver.Chrome()
    brower.get(base_url)
    counter = 0 #试错计数器
    times = 40  #试错次数，错误达到后停止爬取
    for i in range(times):
        try:
            NEW_sets = selenium_get(brower,total_sets)
            if NEW_sets:
                get_img_content(NEW_sets)
            elif not NEW_sets:
                time.sleep(4)       #休眠时间，防止图片加载不出来
                NEW_sets = selenium_get(brower, total_sets)
                get_img_content(NEW_sets)
            else:
                counter += 1
            if counter >= times:
                break

            print('第{}次尝试，一共{}次,还剩{}次机会'.format(i+1,times,times-counter))
        except Exception as e:
            print('oh something wrong!!!',e)
        finally:
            tmpdir = os.getcwd() + os.path.sep + SUPERSTAR
            photo_nums = len(os.listdir(r'{}'.format(tmpdir)))
            print("In the current directory has {} photos".format(photo_nums))
            if photo_nums >= NUMS:
                break
            total_sets = total_sets | NEW_sets
    brower.close()
    print("*"*20+"  ",counter,"  "+"*"*20)


if __name__ == '__main__':
    start = time.time()
    main()
    print('Complete!!!!!!!!!!\n')
    end = time.time()
    spend = end - start
    hour = spend // 3600
    minu = (spend - 3600 * hour) // 60
    sec = round(spend - 3600 * hour - 60 * minu, 2)
    print(f'一共花费了{hour}小时{minu}分钟{sec}秒')
