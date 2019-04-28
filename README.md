# some_simple_demos
个人写的一些爬虫,爬取ins之类,telegram_bot bing图片
Some_simple_demo

## bosszhipin: boss 直聘岗位分析实战

```
爬取boss直聘网站上数据分析岗位,累计有效数据116条,并用Excel teableau 等进行数据可视化,同时采用网络工具,对地址进行解析,生成了多个岗位的坐标图
```





## bingwallpaper_bot_code:

```python
写的一个爬虫兼tg机器人，每天定时爬取bing的壁纸和简介信息，发布到个人频道上,同时壁纸用hash值校验,防止重复存储
解决的bug有，
1.有时候爬取的是英文版，原先的统配规则无法使用，于是换成了通用的正则
2.LINUX 下CRONTAB命令很迷，原先在服务器上部署成功后，服务器被回收后也就没有再自动化，每天直接手动运行
PYTHON-TELEGRAM-BOT 模块是一个非常好用的三方库，也需要自己去telegram 官网上看看bot api文档

```

![image-20190427005412679](http://agandong4-bucket.oss-cn-shanghai.aliyuncs.com/2019-04-26-165415.png)

## ins: instgram 爬虫,自动抓取ins上明星的图片

```
主要的难点是设置代理,同时采用了selenium 模拟翻页,并将每次翻页所解析出的图片链接与现有的图片链接集合取差集,获得新的图片链接集合,同时将链接存储到mongodb 数据库上,避免重复下载
目前累计下载约3000+张图片
```

![image-20190427010922486](http://agandong4-bucket.oss-cn-shanghai.aliyuncs.com/2019-04-26-170924.png)

## new_year_zhufu: 自动向微信好友发送新年祝福

```
利用itchat 三方库,自动向微信好友发送新年祝福
```

## maoyaotop100: 猫眼电影top100 

```
爬取到猫眼电影上的top100 电影,一部电影一部人生
```

![image-20190427135029536](http://agandong4-bucket.oss-cn-shanghai.aliyuncs.com/2019-04-27-055031.png)

## qqHead_portrait_spider: qq 群头像爬虫

```
爬取了某二手群2000人的QQ头像,将这些头像集合拼接成了蒙太奇图片,并做了昵称的词云图
```

![image-20190427135232637](http://agandong4-bucket.oss-cn-shanghai.aliyuncs.com/2019-04-27-055251.png)

![image-20190427135308918](http://agandong4-bucket.oss-cn-shanghai.aliyuncs.com/2019-04-27-055312.png)
