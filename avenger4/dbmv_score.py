#!/usr/bin/env python
# encoding: utf-8
'''
@author: agandong4
@license: (C) Copyright 2013-2019, Node Supply Chain Manager Corporation Limited.
@contact: agandong4@gmail.com
@software: garner
@file: dbmv_score.py
@time: 2019-04-24 13:27
@desc:爬取《复仇者联盟4》豆瓣评分，使用简单的爬虫，写入txt文件，以便日后进行分析
对于 远程ssh linux平台，直接可以使用"nohup python dbmv_score.py & "命令进行执行，避免hup信号挂断python进程
还是将
'''

import requests
import os
import time
from lxml import etree
import telegram
from config import TOKEN,MY_ID
import platform

baseurl = 'https://movie.douban.com/subject/26100958/'

def get_score(url):
    resp = requests.get(baseurl).text
    s = etree.HTML(resp)
    title = s.xpath('//*[@id="content"]/h1/span[1]/text()')[0]
    score = s.xpath('//*[@id="interest_sectl"]/div[1]/div[2]/strong/text()')[0]
    rating_people = s.xpath('//*[@id="interest_sectl"]/div[1]/div[2]/div/div[2]/a/span/text()')[0]
    stars5 = s.xpath('//*[@id="interest_sectl"]/div[1]/div[3]/div[1]/span[2]/text()')[0]
    stars4 = s.xpath('//*[@id="interest_sectl"]/div[1]/div[3]/div[2]/span[2]/text()')[0]
    stars3 = s.xpath('//*[@id="interest_sectl"]/div[1]/div[3]/div[3]/span[2]/text()')[0]
    stars2 = s.xpath('//*[@id="interest_sectl"]/div[1]/div[3]/div[4]/span[2]/text()')[0]
    stars1 = s.xpath('//*[@id="interest_sectl"]/div[1]/div[3]/div[5]/span[2]/text()')[0]
    TIME = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    if title == '复仇者联盟4：终局之战 Avengers: Endgame':
        return (TIME,score,rating_people,stars5,stars4,stars3,stars2,stars1)

def restore_scores(results):
    if not os.path.exists('./scores.txt'):
        os.system('touch scores.txt')
    try:
        results = get_score(baseurl)
        print(results)
        #['复仇者联盟4：终局之战 Avengers: Endgame'] ['9.2'] ['59818'] ['71.8%'] ['20.1%'] ['6.3%'] ['0.9%'] ['0.9%']
        with open('./scores.txt','a') as f:
            f.write(str(results)+'\n')
            f.close()
    except Exception as e:
        send_text(str(e) + "restore_scores fun has something wrong!")

def send_text(text):
    try:
        bot_proxy = telegram.utils.request.Request(proxy_url='socks5://127.0.0.1:1086')
        bot = telegram.Bot(token=TOKEN, request=bot_proxy)
        bot.send_message(chat_id=MY_ID,text=text)
    except Exception as e:
        bot = telegram.Bot(token=TOKEN)
        bot.send_message(chat_id=MY_ID, text=text+str(e))
    finally:
        bot.send_message(chat_id=MY_ID,text=str(platform.platform()))

def main():
    try:
        results = get_score(baseurl)
    except Exception as e:
        send_text(str(e) + "get_score fun has something wrong!")

    restore_scores(results)

if __name__ == '__main__':
    while True:
        try:
            main()
        except UnboundLocalError as ue:
            send_text(str(ue))
        time.sleep(2*60)