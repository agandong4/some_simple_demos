# some_simple_demos
#### 个人利用自己的技能写的一些小东西,主要有:

* **爬取boss直聘数据分析岗位**	对爬取的结果进行数据分析,通过navicat 导入到myslq当中
  * 涉及到Excel可视化,透视表,切片器,tableau,mysql,xpath解析,python 语法
* **bing壁纸爬虫** 每天爬取壁纸,并通过代理,投送到个人频道上
  * 涉及到正则表达式,request库,python -telegram-bot等三方库,hash校验
* **Instrgram 爬虫** 自动抓取ins上明星的图片
  * 涉及到selenium 自动模拟,request 库,异常的捕获,mongodb的存储
* **Titan kaggle 生存预测**  参加的经典比赛,采用基于Gini系数的决策树对乘客进行生存预测
  * 涉及到python的matplotlib.pyplot  pandas sklearn seaborn
  * 数据清洗有去处空值,填充平均值,回归预测

## bosszhipin: boss 直聘岗位分析实战

```
爬取boss直聘网站上数据分析岗位,累计有效数据116条,并用Excel teableau 等进行数据可视化,同时采用网络工具,对地址进行解析,生成了多个岗位的坐标图
```

![数据透视表](http://agandong4-bucket.oss-cn-shanghai.aliyuncs.com/2019-04-28-050518.png)

#### 经验不限,一年以内的起薪一目了然,从中可以看出哥哥工作年限的平均薪资

![各区域岗位统计](http://agandong4-bucket.oss-cn-shanghai.aliyuncs.com/2019-04-28-050521.png)

#### 从上图可以看出,长宁,浦东新区和闵行区三个区的数据岗位需求最多,机会最大

![tableau](http://agandong4-bucket.oss-cn-shanghai.aliyuncs.com/2019-04-28-050539.png)

#### 从上图可以看出,数据分析的岗位要求最多的是本科,即本科是一般要求,而对博士生的要求最低,而对本科生而言,一年以内的工作经验可以拿到一万出头,而应届生则较差

![image-20190428130733225](http://agandong4-bucket.oss-cn-shanghai.aliyuncs.com/2019-04-28-050734.png)

#### 通过谷歌地图的api对公司的地址解析,得到了近-热力图,可以清楚看到数据分析岗位的地理位置分布

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

## Titan kaggle 生存预测

~~~
对泰坦尼克号进行生存预测
~~~

![pies](http://agandong4-bucket.oss-cn-shanghai.aliyuncs.com/2019-04-28-054945.png)

![image-20190428142712225](http://agandong4-bucket.oss-cn-shanghai.aliyuncs.com/2019-04-28-062715.png)



#### 图表中可以看出,船舱为一等舱的女士获救率高到95%以上,而男士普遍的生存率不高;男士的平均生存率为19%,女士为74%

![image-20190428141903373](http://agandong4-bucket.oss-cn-shanghai.aliyuncs.com/2019-04-28-062223.png)

#### 提交结果,预测准确率为72%

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

![2019-04-28-050045 copy](http://agandong4-bucket.oss-cn-shanghai.aliyuncs.com/2019-04-28-050416.jpg)

#### 学校校徽蒙太奇

## 个人摄影作品

![318单张大片-63 copy](http://agandong4-bucket.oss-cn-shanghai.aliyuncs.com/2019-04-28-103838.jpg)

![318拼接大片-9 copy](http://agandong4-bucket.oss-cn-shanghai.aliyuncs.com/2019-04-28-103848.jpg)

![dapanA01 copy](http://agandong4-bucket.oss-cn-shanghai.aliyuncs.com/2019-04-28-103857.jpg)

![milkway copy](http://agandong4-bucket.oss-cn-shanghai.aliyuncs.com/2019-04-28-103906.jpg)