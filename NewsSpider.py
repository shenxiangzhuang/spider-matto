'''
新闻爬取程序
'''

import re
import os
import time
import chardet
import requests
import pandas as pd
from Mproxy import Mproxy

class MNewsSpider():
    def __init__(self):
        self.keywords = '赵丽颖'  # 爬取的关键词
        self.title_hrefs = {}  # 存放本次爬取的新闻数据{标题：链接}
        self.roi = {}  # 存放本次含有关键词的数据
        self.roi_latest = {}  # 存放最新的含有关键词的数据

    # 获取全部网址
    '''
    发现百度新闻娱乐新闻中的文章是动态加载的，分为下面几个地址：
    http://news.baidu.com/widget?id=Movie&channel=ent&t=1504867650168
    http://news.baidu.com/widget?id=TV&channel=ent&t=1504867650184
    http://news.baidu.com/widget?id=Music&channel=ent&t=1504867650200
    http://news.baidu.com/widget?id=Variety&channel=ent&t=1504867650217
    http://news.baidu.com/widget?id=Picture&channel=ent&t=1504867650248
    http://news.baidu.com/widget?id=LatestNews&channel=ent&t=1504867650266
    推测是根据请求时间（时间戳）来合成网址最后的后缀，不过差了三位，所以推测是小数点向后移动了三位
    '''

    def get_urls(self):
        urls = []
        time_plus = str(int(float(time.time()) * 1000))
        urls.append("http://news.baidu.com/widget?id=Star&channel=ent&t=" + time_plus)
        urls.append("http://news.baidu.com/widget?id=TV&channel=ent&t=" + time_plus)
        urls.append("http://news.baidu.com/widget?id=Music&channel=ent&t=" + time_plus)
        urls.append("http://news.baidu.com/widget?id=Variety&channel=ent&t=" + time_plus)
        urls.append("http://news.baidu.com/widget?id=Picture&channel=ent&t=" + time_plus)
        urls.append("http://news.baidu.com/widget?id=LatestNews&channel=ent&t=" + time_plus)
        urls.append("http://news.baidu.com/widget?id=Movie&channel=ent&t=" + time_plus)
        urls.append("http://ent.sina.com.cn/")


        return urls

    # 获取网页数据
    def get_web_data(self, url, use_proxies=False):
        headers = {
            'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) Gecko/20100101 Firefox/55.0"}

        # 测试的时候，请求频繁会返回500错误,按常理说是服务器端的错误，但是，
        # 浏览器可以正常访问的。。而且测试下，换了代理IP也是可以的
        # 推测是服务器检测到请求异常，暂时封了我的IP...
        # 加入异常处理

        if use_proxies:

            myproxies = Mproxy()
            myproxies.get_chinaips()
            proxies = myproxies.getRandomProxyList()
            try_times = 3  # 失败则重试三次
            while(try_times > 0):
                # 引入代理IP的class，开始换入
                print("正在换入代理IP: ", proxies)
                html = requests.get(url, headers=headers, proxies=proxies, verify=False, timeout=10)
                try_times -= 1
                statuscode = html.status_code
                if statuscode == 200:
                    break
        else:
            html = requests.get(url, headers=headers, verify=False, timeout=10)

        Encoding = chardet.detect(html.content)['encoding']
        html.encoding = Encoding
        web_data = html.text
        # print(web_data)

        return web_data

    # 获取标题
    def get_titles(self, web_data):
        # 抓取处于a 标签，带href属性的新闻（占了绝大多数）
        pa = '<a href="(http.*?)" .*?>(.*?)</a>'
        href_title_data = re.findall(pa, web_data)
        for href_title in href_title_data:
            # 　去除非新闻信息（根据标题长度）
            if ((len(href_title[1]) >= 10) & (len(href_title[1]) < 50)):
                self.title_hrefs[href_title[1]] = href_title[0]  # {标题：链接}

    # 筛选自己想了解的信息

    def getNewsRoiData(self):
        urls = self.get_urls()
        # 获取所有新闻信息到self.title_hrefs
        for url in urls:
            web_data = self.get_web_data(url)
            self.get_titles(web_data)
        # 获取含有关键词的新闻信息到self.roi
        for title in self.title_hrefs:
            if self.keywords in title:
                self.roi[title] = self.title_hrefs[title]



    # 存入CSV文件
    def saveDatatoCSV(self, mode='w'):
        NewsdataDf = pd.DataFrame()
        NewsdataDf['titles'] = self.roi_latest.keys()
        NewsdataDf['hrefs'] = self.roi_latest.values()
        NewsdataDf.drop_duplicates(subset='hrefs', inplace=True)  # 这里根据网址去重（防止之前正则写的规则重复抓取）
        self.roi_latest = NewsdataDf  # 去重后的ROI数据

        if mode == 'a':
            NewsdataDf.to_csv("NewsData.csv", index=None, header=None, mode=mode)
        else:
            NewsdataDf.to_csv("NewsData.csv", index=None, mode=mode)
        return NewsdataDf

    # 存入MySQL数据库
    def saveDatatoMySQL(self):
        pass

    # 存储前查看是否存在重复抓取（去重）
    '''
    暂时通过遍历文件,对比的方法来判断重复与否
    '''

    def saveLatestRoi(self):
        # 没有文件则创建
        if 'NewsData.csv' not in os.listdir():
            self.roi_latest = self.roi
            LatestRoi_df = self.saveDatatoCSV(mode='w')  # mdoe=write
            print("Latest: \n", LatestRoi_df)
            return LatestRoi_df

        HistoryNews = pd.read_csv("NewsData.csv")
        for title, href in self.roi.items():
            is_latest = True
            for h_title_index in range(len(HistoryNews['titles'])):
                if title[:10] == HistoryNews['titles'][h_title_index][:10]:
                    is_latest = False
                if href == HistoryNews['hrefs'][h_title_index]:
                    is_latest = False

            if is_latest:
                self.roi_latest[title] = href

        LatestRoi_df = self.saveDatatoCSV(mode='a')  # mode=add
        print("Latest: \n", LatestRoi_df)

        return LatestRoi_df

    # 生成本地日志记录
    def record(self):
        if 'NewsReportLog.txt' not in os.listdir():
            with open('NewsReportLog.txt', 'w') as f:  # 写入模式
                f.write(str(self.keywords) + '相关新闻抓取程序日志' + str(time.ctime()) + '\n')

        with open('NewsReportLog.txt', 'a') as f:  # 追加模式
            f.write('=' * 10 + str(time.ctime() + '=' * 10) + '\n')
            if len(self.roi_latest) != 0:
                for i in range(len(self.roi_latest)):
                    f.write(self.roi_latest['titles'][i])
                    f.write(", ")
                    f.write(self.roi_latest['hrefs'][i])
                f.write('\n')
            else:
                f.write("None\n")

if __name__ == '__main__':
    mynewsspider = MNewsSpider()
    mynewsspider.getNewsRoiData()
    latest_roi = mynewsspider.saveLatestRoi()
    mynewsspider.record()

