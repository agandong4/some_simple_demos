#!/usr/bin/env python
# encoding: utf-8
'''
@author: agandong4
@license: (C) Copyright 2013-2019, Node Supply Chain Manager Corporation Limited.
@contact: agandong4@gmail.com
@software: garner
@file: main.py
@time: 2019-03-24 17:15
@desc:写的一个爬虫兼tg机器人，每天定时爬取bing的壁纸和简介信息，发布到个人频道上,同时壁纸命令用hash
解决的bug有，
1.有时候爬取的是英文版，原先的统配规则无法使用，于是换成了通用的正则
2.LINUX 下CRONTAB命令很迷，原先在服务器上部署成功后，服务器被回收后也就没有再自动化，每天直接手动运行
PYTHON-TELEGRAM-BOT 模块是一个非常好用的模块，也需要自己去看看bot api文档
'''
import pymongo
import requests
from config import *
import re
import datetime
from hashlib import md5
from requests import ConnectionError, codes, RequestException
import os
import telegram

MONGO_URL = 'localhost'
MONGO_DB = 'bing'
MONGO_TABLE = 'bingwallpaper'


header = {
  "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
}
proxies = {'http': 'http://localhost:1087', 'https': 'https://localhost:1087'}

MASTER = GROUP_ID

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]
bot_proxy = telegram.utils.request.Request(proxy_url='socks5://127.0.0.1:1086')
bot = telegram.Bot(token=TOKEN, request=bot_proxy)
dir = os.getcwd() + os.path.sep + 'bingwallpaper'


def parse_bing():
    base_url = 'https://cn.bing.com/'
    language_parameter = '?mtk=zh-CN'
    # base_url = 'https://www.bing.com/?mkt=zh-CN'
    try:
        resp = requests.get(base_url+language_parameter, headers=header).text
    except RequestException:
        send_text(MASTER, "connectionError")
    # print(resp)
    match_url = re.search('id="bgLink".*?href="(.*?)"', resp, re.S)
    info = re.search('class="sc_light" title="(.*?)".*?"主页图片信息"', resp, re.S)
    print(info)
    if not info:
        info = re.search('"copyright":"(.*?)","copyrightlink"', resp, re.S)
        print('-'*40)
        print(info)
    IMG_info = str(info.groups(1)).strip("(),'")
    IMG_url = base_url + str(match_url.groups(1)).strip("()',")
    print(IMG_info, "----", IMG_url)
    return IMG_info, IMG_url


def down_img(imgurl):
    try:
        img = requests.get(imgurl, timeout=4)
        if img.status_code == codes.ok:
            return img.content
    except ConnectionError:
        send_text(MASTER, 'ConnectionError')
    except RequestException:
        send_text(MASTER, "wo ye buzhi dao weisha chu chuole")


def save_img(img, IMG_info):
    if not os.path.exists(dir):
        os.mkdir(dir)
        print('mkdir successfully')
    md5num = md5(img).hexdigest()
    dirs_md5 = [x.split('_')[-1] for x in os.listdir(dir)]
    print(dirs_md5)
    if md5num not in dirs_md5:
        today = datetime.date.today()
        img_path = '{0}/{1}.{2}'.format(dir, str(today) + '_' + md5num, 'jpg')
        print(img_path)
        with open(img_path, 'wb')as f:
            f.write(img)
            f.close()

def send_wallpaper():
    today = datetime.date.today()
    if not os.path.exists(dir):
        os.mkdir(dir)
        print('mkdir successfully')
    if str(today) not in [x.split('_')[1] for x in os.listdir(dir)]:
        IMG_info, IMG_url = parse_bing()
        save_img(down_img(IMG_url), IMG_info)
    send_img = str([x  for x in os.listdir(dir) if str(today)in x][0]).strip("[']")
    print(dir+os.path.sep+send_img)
    try:
        bot.send_photo(chat_id=MASTER, photo=open(dir+os.path.sep+send_img, 'rb'))
        send_text(chat_id=MASTER,text=IMG_info)
    except:
        print(IMG_info)
        send_text(text="oh! something wrong")


def send_text(chat_id=GFW_ID, text="23333"):
    bot.send_message(chat_id=chat_id, text=text)


def main():
    send_wallpaper()



if __name__ == '__main__':
    main()
