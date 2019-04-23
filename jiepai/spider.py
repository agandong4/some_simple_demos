#!/usr/bin/env python
# encoding: utf-8
'''
@author: agandong4
@license: (C) Copyright 2013-2019, Node Supply Chain Manager Corporation Limited.
@contact: agandong4@gmail.com
@software: garner
@file: spider.py
@time: 2019-03-15 16:57
@desc:
'''
from urllib.parse import urlencode
from requests.exceptions import RequestException
import requests
from requests import codes
import os
from hashlib import md5
from multiprocessing.pool import Pool

def get_page_index(offset,keyword):
    params = {
        'offset': offset,
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': '20',
        'cur_tab': '1',
        'from':'search_tab'
    }
    url = 'https://www.toutiao.com/search/?' + urlencode(params)

    try:
        response = requests.get(url)
        if response.status_code == codes.ok:
            return response.json()
        return None
    except requests.ConnectionError:
        print("请求索引页失败")
        return None

def get_image(json):
    if json.get('data'):
        data = json.get('data')
        for item in data:
            if item.get('cell_type') is not None:
                continue
            title = item.get('title')
            images = item.get('image_list')
            for image in images:
                yield {
                    'image':'https:'+image.get('url'),
                    'title':title
                }

def save_image(item):
    img_path = 'toutiao'+os.path.sep+item.get('title')
    if not os.path.exists(img_path):
        os.mkdirs(img_path)
    try:
        resp = requests.get(item.get('image'))
        if codes.ok == resp.status_code:
            file_path = img_path + os.path.sep + '{file_name}.{file_suffix}'\
            .format(file_name=md5(resp.content).hexdigest(),file_suffix='jpg')
        if not os.path.exists(file_path):
            with open(file_path,'wb') as f:
                f.write(resp.content)
            print('Successful downloaded image: %s'%file_path)
        else:
            print('Aleady Downloaded!',file_path)
    except requests.ConnectionError:
        print('Failed to Save Image, item %s' %item)




def main(offset):
    json = get_page_index(offset,'街拍')
    print(json)
    for item in get_image(json):
        print(item)
        save_image(item)

GROUP_START = 0
GROUP_END = 4

if __name__ == '__main__':
    pool = Pool()
    groups = ([x*20 for x in range(GROUP_START,GROUP_END+1)])
    pool.map(main,groups)
    pool.close()
    pool.join()


