#!/usr/bin/env python
# encoding: utf-8
'''
@author: agandong4
@license: (C) Copyright 2013-2019, Node Supply Chain Manager Corporation Limited.
@contact: agandong4@gmail.com
@software: garner
@file: spider.py
@time: 2019-03-15 19:40
@desc:
'''
import os
import re
import json
import time
import random
import requests
from requests import codes, ConnectionError, RequestException
from requests.exceptions import ConnectTimeout, ReadTimeout
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from hashlib import md5
from pyquery import PyQuery as pq
from config import *
import pymongo

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/58.0.3029.110 Safari/537.36",
    "cookie": 'mid=XIvU4AAEAAFBy-RVWENGm4fPzNlm; rur=FTW; csrftoken=8csE583qo3YvzZYbQEoWSJP2kSJVpWwf; ds_user_id=6891606915; sessionid=6891606915%3AnrFkPOcuM5lFE7%3A14; urlgen="{\"112.120.244.82\": 4760}:1h4rvU:CRzyO1UVUIkivr5_YhvuNctyZ9c"'
}

# base_url = 'https://www.instagram.com/irene.rvelvet/'
# base_url = 'https://www.instagram.com/tvxq.official/'

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]


def selenium_get(brower,total_sets):

    try:
        urls_set = set([])  # 集合保证了链接的唯一性
        for x in range(4*4):
            time.sleep(random.random())
            ActionChains(brower).send_keys(Keys.PAGE_DOWN).perform()
        time.sleep(random.random()+2)
        divs = brower.find_elements_by_class_name('v1Nh3')
        for d in divs:
            urls_set.add(d.find_element_by_tag_name('a').get_attribute('href'))
        new_sets = (urls_set | total_sets) - total_sets
    except:
        new_sets = set([])
    finally:
        return new_sets


def download_img(img_pages):
    print("--------------\n", len(img_pages))
    for img in img_pages:
        img_html = requests.get(img)  # ,headers=None)
        # print(img_html.text)
        pattern = re.compile('"shortcode":"(.*?)"', re.S)
        # pattern = re.compile('<img alt="Image may contain:.*?class="FFVAD".*?src="(.*?)"',re.S)
        img_url = re.search(pattern, img_html.text)
        prefix_url = 'https://www.instagram.com/p/'
        print("获取到的 " + prefix_url + str(img_url.groups(1)).strip("(',)'"))


def get_img_content(IMG_set):
    # IMG = 'https://www.instagram.com/p/Bu0fjJnAewr/'
    for i, item in enumerate(IMG_set):
        print('{:.1%} ----{}----{}'.format((i+1)/len(IMG_set),i+1,len(IMG_set)))
        pattern2 = re.compile('display_url":"(.*?)","display_resources":')  # no nedd re.S
        IMG_html_text = requests.get(item).text
        display_url = re.search(pattern2, IMG_html_text)
        # print(display_url)
        longurl = display_url.group(1)

        try:
            resp = requests.get(longurl, timeout=4)
            if resp.status_code == codes.ok:
                if not os.path.exists(os.getcwd() + os.path.sep + SUPERSTAR):
                    os.mkdir(os.getcwd() + os.path.sep + SUPERSTAR)
                    print("mkdir successfully")
                if save_to_mongo(longurl):

                    save_img(resp.content)
            # time.sleep(random.random()+1)
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


def save_to_mongo(result):
    if not db[MONGO_TABLE].find_one({'url':result}):
        db[MONGO_TABLE].insert_one({'url':result})
        print('successful restore the url to mongo db!', result)
        return True
    else:
        print('already have this url ,no need to insert!')
        return False


def save_img(content):
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


def main():
    total_sets = set([])
    brower = webdriver.Chrome()
    brower.get(base_url)
    counter = 0 #计数器，方式爬取到最后没有和还继续爬
    times = 80
    for i in range(times):
        try:
            NEW_sets = selenium_get(brower,total_sets)
            if NEW_sets:
                get_img_content(NEW_sets)
            elif not NEW_sets:
                time.sleep(4)
                NEW_sets = selenium_get(brower, total_sets)
                get_img_content(NEW_sets)
            else:
                counter += 1
            if counter >= 20:
                break

            print('第{}次尝试，一共{}次,还剩{}次机会'.format(i+1,times,20-counter))
        except Exception as e:
            print('oh something wrong!!!')
            print(e)
        finally:
            photo_nums = len(os.listdir(os.getcwd() + os.path.sep + SUPERSTAR))
            print("In the current directory has {} photos".format(photo_nums))
            if photo_nums >=1024:
                break
            total_sets = total_sets | NEW_sets
    brower.close()
    print("*"*20,counter)


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
