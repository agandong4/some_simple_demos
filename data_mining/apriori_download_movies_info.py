#!/usr/bin/env python
# encoding: utf-8
'''
@author: agandong4
@license: (C) Copyright 2013-2019, Node Supply Chain Manager Corporation Limited.
@contact: agandong4@gmail.com
@software: garner
@file: apriori_download_movies_info.py
@time: 2019-05-05 18:26
@desc:
'''

#下载某个导演的电影数据集

from efficient_apriori import apriori
from lxml import etree
from selenium import webdriver
import time
import csv
driver = webdriver.Chrome()

#设置想要下载的导演，数据集
director = u'成龙'
#写入CSV文件
filename = './'+director+'.csv'
base_url = 'https://movie.douban.com/subject_search?search_text='+director+'&cat=1002'
out = open(filename,'w',newline='',encoding='utf-8-sig')
csv_write = csv.writer(out,dialect='excel')
flags= []
#下载指定页面的数据
def download(request_url):
    driver.get(request_url)
    time.sleep(1)
    html = driver.find_element_by_xpath("//*").get_attribute("outerHTML")
    html = etree.HTML(html)
    #设置电影名称，导演演员的Xpath
    movies_lists = html.xpath('//*[@id="root"]/div/div[2]/div[1]//*[@class="title"]/text()')
    names_lists = html.xpath('//*[@id="root"]/div/div[2]/div[1]//*[@class="meta abstract_2"]/text()')
    nums = len(movies_lists)
    if nums > 15:#第一页有16条数据
        #默认第一个不是，所以需要去掉
        movies_lists = movies_lists[1:]
        names_lists = names_lists[1:]
    for (movie,name) in zip(movies_lists,names_lists):
        #会有数据为空的情况
        if name.text is None:
            print("name is null")
            continue
        #显示下演员名称
        print(name.text)
        names = name.text.split('/')
        #判断导演是否为指定的director
        if names[0].strip() == director and movie.text not in flags:
            #将第一额字段设置为电影名称
            names[0] = movie.text
            flags.append(movie.text)
            csv_write.writerow(names)
    print('ok')
    print(nums)
    if nums >= 14:#有可能一页会有14个电影
        #继续下一页
        return True
    else:
        #没有下一页
        return False

def main():
    start = 0
    while start < 1000:
        request_url = base_url + str(start)
        #下载数据，并返回是否有下一页
        flag = download(request_url)
        if flag:
            start = start + 15
        else:
            break
    out.close()
    print('finished!!!\n')

