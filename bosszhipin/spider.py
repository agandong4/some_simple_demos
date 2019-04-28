#!/usr/bin/env python
# encoding: utf-8
'''
@author: agandong4
@license: (C) Copyright 2013-2019, Node Supply Chain Manager Corporation Limited.
@contact: agandong4@gmail.com
@software: garner
@file: spider.py
@time: 2019-04-16 17:28
@desc:
'''

import requests
import json
import re
import os
import time
import random
import pandas as pd
from lxml import etree
from urllib.parse import quote #url编码

# 正则表达式：去掉标签中的<br/> 和 <em></em>标签，便于使用xpath解析提取文本
regx_obj = re.compile(r'<br/>|<(em).*?>.*?</\1>')
baseurl = 'https://www.zhipin.com'
headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/73.0.3683.103 Safari/537.36'}
columns = ['positionID','position_url','position','salary','publisherName',
           'responsibility','requirement','job_tags','company','company_info','address']
pages = 2



def send_request(url_path, param = None):
    '''
    发送请求，获取html响应(这里是get请求)
    '''
    response = regx_obj.sub('',requests.get(url=url_path, params=param, headers=headers).text)
    return response

def get_pages(page,work="数据分析",city_code = '101020100'):
    """
    构造URL 链接 解析网页，获得工作详细页链接
    :return:jobs_url
    """
    if page == 1:
        url = 'https://www.zhipin.com/c{}/?query={}'.format(city_code,quote(work))
    else:
        url = 'https://www.zhipin.com/c{}/?query={}&page={}&ka=page-next'.format(city_code,quote(work),pages)
    print('-'*40+'\n')
    print(f"正在爬取第{page}页，一共{pages}页")
    resp = regx_obj.sub('',requests.get(url,headers=headers).text)
    html = etree.HTML(resp)
    urls = html.xpath(".//div[@class='info-primary']//a/@href")
    return urls

def get_jobs_url(url):
    jobs_resp = regx_obj.sub('',requests.get(baseurl+url,headers=headers).text)
    html = etree.HTML(jobs_resp)
    try:
        parse_results = parse_html(html,url)
        return parse_results
    except Exception as e:
        print(e)


def parse_html(html_obj,url):
    item = {}
    #职位id
    positionID = re.search('/job_detail/(.*?).html', url).group(1)
    item['positionID'] = positionID
    #posittion_url
    item['position_url'] = baseurl+url
    # 职位名
    item['position'] = html_obj.xpath("//div[@class='job-primary detail-box']/div[@class='info-primary']/div[@class='name']/h1/text()")[0].strip()
    #薪水
    item['salary'] = html_obj.xpath('.//div[@class="info-primary"]//span[@class="salary"]/text()')[0].strip()
    # print(item["position"] + '\t' + item["salary"] + '\t' + item["position_url"])
    # 发布者姓名
    try:
        item['publisherName'] = html_obj.xpath("//div[@class='job-detail']//h2/text()")[0].strip()
    except:
        item['publisherName'] = 'no_name'
    # 发布者职位
    item['publisherPosition'] = html_obj.xpath("//div[@class='detail-op']//p/text()")[0].strip()
    # 工作职责
    item['responsibility'] = html_obj.xpath("//div[@class='job-sec']//div[@class='text']/text()")[0].strip()
    # 招聘要求
    item['requirement'] = html_obj.xpath("//div[@class='job-primary detail-box']/div[@class='info-primary']/p/text()")[
        0].strip()
    #工作标签  有些就是没有job_tags
    item['job_tags'] = str(html_obj.xpath('//*[@id="main"]/div[1]/div/div/div[2]/div[3]/div[@class="job-tags"]/span/text()'))
    # 招聘企业
    item['company'] = html_obj.xpath("//div[@class='sider-company']/div[@class='company-info']/a/@title")[0].strip()
    # 招聘企业信息
    item['company_info'] = str(html_obj.xpath('//*[@id="main"]/div[3]/div/div[2]/div[2]//div[@class="job-sec"]//div[@class="level-list"]/li/text()')).strip()
    # 地址
    item['address'] = html_obj.xpath('//*[@id="main"]/div[3]/div/div[2]/div[2]//div[@class="location-address"]/text()')[0].strip()

    return item

def query_city():
    '''
    查询城市编号并保存
    '''
    url = 'https://www.zhipin.com/common/data/city.json'
    data = json.loads(send_request(url))
    city = {}
    for item in data['data']['cityList']:
        for it in item['subLevelModelList']:
            city.update({it['name'] : it['code']})

    with open('./boss_city.json', 'w', encoding='utf-8') as f:
        try:
            json_str = json.dumps(city, indent=4, ensure_ascii=False)
            f.write(json_str)
        except Exception as e:
            print('-----')
            print(e)

def get_city_json():
    '''
    获取查询编号
    '''
    if not os.path.exists('./boss_city.json'):
        query_city()
    with open('./boss_city.json', 'r',encoding='utf-8') as f:
        return json.loads(f.read())

def input_f():
    city_list = get_city_json()
    city_name = input('请输入需要爬取的城市:')

    city_code = city_list[city_name]

    city_region = input('请输入需要爬取的城市行政区:')

    work = input('请输入需要爬取的职业信息:')
    pages = int(input('请输入需要爬取的页面数:'))
    return city_code,city_region,work,pages

def main():
    global city_code
    city_code = None
    #输入参数
    # input_f()
    print('*'*20)

    job_df = pd.DataFrame(columns=columns)
    print('~'*20)
    num = 0

    try:
        for page in range(1,pages):
            try:
                urlsets = get_pages(page)
                # tmp_urls = pd.read_csv('./jobs_list.csv',header=None)
                # urlsets = list('/job_detail/'+ tmp_urls.loc[:,0] + '.html')
            except:
                print('parsing page {} failed ! Continue....'.format(page))
                continue
            for u,url in enumerate(urlsets):
                job = get_jobs_url(url)
                print("{:<30}{:<20}{:<30}".format(job['position'],job['salary'],job['requirement']))
                #dict to dataframe
                job_df.loc[num,columns] = job
                #计数器
                num += 1
            time.sleep(4 + random.random())
    except Exception as e:
        print(repr(e))
    finally:
        # if not os.path.exists('./job.csv'):
        #     os.system('touch job.csv')
        print('一共下载了{}条数据，导入到csv文件中'.format(num))
        with open('./job.csv','a') as f:
            job_df.to_csv(f,encoding='utf-8',header=False)


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