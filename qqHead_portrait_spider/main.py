#!/usr/bin/env python
# encoding: utf-8
'''
@author: agandong4
@license: (C) Copyright 2013-2019, Node Supply Chain Manager Corporation Limited.
@contact: agandong4@gmail.com
@software: garner
@file: main.py
@time: 2019-03-17 18:59
@desc:
'''

import requests
import random
import os,re
from os import listdir
from PIL import Image
import math
from wordcloud import WordCloud
from hashlib import md5
import urllib3
urllib3.disable_warnings()


class Genqqmen:
    group_url = 'https://qun.qq.com/cgi-bin/qun_mgr/search_group_members'

    def __init__(self,qq_number,group_name='',mem_count=200):
        self.qq_num = qq_number
        self.begin = mem_count
        self.end = mem_count + 20
        self.dir_name = os.getcwd() + os.path.sep +  qq_number + '_' + group_name
    def get_memes(self,):

        all_nick = []
        data = 'gc=%s&st=%s&end=%s&sort=0&bkn=1527834478'%(self.qq_num,self.begin,self.end)
        print(data)
        cookies = {
        'cookie':'pgv_pvi=460754944; pgv_si=s9801076736; uin=o1357964502; ptisp=cm; RK=1hz4iw3IXa; ptcz=a56bc07ed3cc2906c669b30f794068c07bc47e9b43e40918a47330fd88c8e277; p_uin=o1357964502; skey=@fdS2NMHaV; pt4_token=mMUnYBKr2i8kGIZFnGI5WgkIr5qDrt1O5f-f0SDGsd4_; p_skey=epnJ7icKWeGaE3FLIi7gb7fbLwXygVh*8vp3JGg0Ecg_'
        }
        response = requests.post(self.group_url,data=data,headers=cookies,verify=False)
        print(response.text)
        resp = response.json()
        print('resp\n',resp)
        mems = resp.get('mems')
        if not os.path.exists(self.dir_name):
            os.mkdir(self.dir_name)

        for m in mems:
            try:
                url = 'https://q4.qlogo.cn/g?b=qq&nk={}&s=140'.format(m.get('uin'))
                abs_path = os.path.join(self.dir_name,'%s.jpg'%m.get('uin'))
                # os.mknod(abs_path)
                if not os.path.exists(abs_path):
                    with open(abs_path,'wb') as f:
                        f.write(requests.get(url,verify=False).content)
                        f.close()

                nick_name = m.get('nick')
                print("download complete!!!",nick_name)
                all_nick.append(nick_name)
            except TypeError as e:
                print(e)
                continue
        return all_nick

    def clear_nicks(self,nicks):
        return [re.sub('&.*?;','',nick) for nick in nicks]

    def gen_wrodcloud(self,words):
        words = ' '.join(words)
        wordcloud = WordCloud(width=1000,
                              height=860,
                              margin=2,
                              background_color='black',
                              font_path='SimSun.ttf')

        wordcloud.generate(words)
        wordcloud.to_file(self.dir_name + '_' + 'wordcloud' + '.jpg')

    def get_pic(self):
        # 拼接图片的函数，这个在拼接图片那个博客里写有
        user = self.dir_name
        pics = listdir(user)
        random.shuffle(pics)
        numPic = len(pics)
        size = 760
        eachsize = int(math.sqrt(float(size * size) / numPic))
        numline = int(size / eachsize)
        toImage = Image.new('RGBA', (size, size))
        x = 0
        y = 0
        for i in pics:
            try:
                # 打开图片
                img = Image.open(user + "/" + i)
            except IOError:
                print("Error: 没有找到文件或读取文件失败")
            else:
                # 缩小图片
                img = img.resize((eachsize, eachsize), Image.ANTIALIAS)
                # 拼接图片
                toImage.paste(img, (x * eachsize, y * eachsize))
                x += 1
                if x == numline:
                    x = 0
                    y += 1
        toImage.save(user + str(size) + ".png")

def main():
    total_nicks = []
    for i in range(0,1980,20):
        q = Genqqmen('383342665', '盘锦校区二手物品交易', i)
        nicks = q.get_memes()
        nicks = q.clear_nicks(nicks)
        total_nicks.extend(nicks)

    q.gen_wrodcloud(total_nicks)
    # self.get_pic()

if __name__ == '__main__':
    main()