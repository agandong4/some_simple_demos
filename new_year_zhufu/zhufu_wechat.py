#!/usr/bin/env python
# encoding: utf-8

#coding=UTF-8
#基于python3.6
import itchat,time
import sys
import random
from itchat.content import *
itchat.auto_login()
wish_list = ['愿新的一年，仍有阳光满路温暖如初  (•‾̑⌣‾̑•)✧˖°']
SINCERE_WISH = wish_list[0]
total_friendList = itchat.get_friends(update=True)[1:]


myfriend = list()
with open('sended1.txt','r',encoding='utf-8') as files:
    for line in files.readlines():
        line = line.strip()
        # print(line)
        myfriend.append(line)

    files.close()

print("总共好友数： ",len(total_friendList))
print("已发送好友数： ",len(myfriend))

friendList = []
for i in range(len(total_friendList)):
    if total_friendList[i]['RemarkName'] not in myfriend:
        friendList.append(total_friendList[i])
print("未发送好友数： ",len(friendList))

with open('sended1.txt','a',encoding='utf-8') as files:
    for g in range(0,len(friendList)):
        itchat.send(SINCERE_WISH,friendList[g]['UserName'])
        print((friendList[g]['RemarkName'] or friendList[g]['NickName']),'已发送')
        sys.stdout.write(str(g+1)+"/"+str(len(friendList))+"\r")
        sys.stdout.flush()
        files.write(friendList[g]['RemarkName'],)
        files.write("\n")
        time.sleep(4 + random.random()*4)
    files.close()
    print('done')
