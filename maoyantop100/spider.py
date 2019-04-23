#!/usr/bin/env python
# encoding: utf-8
'''
@author: agandong4
@license: (C) Copyright 2013-2019, Node Supply Chain Manager Corporation Limited.
@contact: agandong4@gmail.com
@software: garner
@file: spider.py
@time: 2019-03-12 21:39
@desc:
'''

import requests
from requests.exceptions import RequestException
import re
import json
from multiprocessing import Pool

def get_one_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
    except RequestException:
        return None
def parse_one_page(html):
    # pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a\
    #                      .*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>\
    #                     .*?integer">(.*?)</i>.*?fraction>(.*?)</i>.*?</dd>',re.S)
    pattern = re.compile('<dd>.*?board-index.*?">(.*?)</i>.*?data-src="(.*?)".*?name"><a'
                         '.*?">(.*?)</a></p>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>'
                         '.*?integer">(.*?)</i>.*?fraction">(.*?)</i></p>.*?</dd>',re.S)

    items = re.findall(pattern,html)
    for item in items:
        yield{
            'index':item[0],
            'image':item[1],
            'title':item[2],
            'actor':item[3].strip()[3:],
            'time' :item[4].strip()[5:],
            'score':item[5]+item[6]
        }
def write_to_file(content):
    with open("maoyantop100movie.txt",'a',encoding='utf-8') as f:
        f.write(json.dumps(content,ensure_ascii = False)+ "\n")
        f.close()



def main(offset):
    url = 'https://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)




if __name__ == '__main__':
    pool = Pool()
    pool.map(main,[i*10 for i in range(10)])