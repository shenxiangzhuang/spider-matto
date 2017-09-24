'''
鉴于刚才的测试,IP出了写些问题
这里尝试从http://cn-proxy.com/获取中国的代理IP
不过,这个网站是要翻墙的,这里使用ss,配合requests使用
用于新闻网页的再次请求
'''

import requests
import random
import pandas as pd
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


class Mproxy():
    def __init__(self):
        self.ss_proxy = {
            "http": "http://localhost:1080",
            "https": "https://localhost:1080"
        }
        self.headers = {'User-Agent': UserAgent().random}

    def get_chinaips(self):
        # 获取网页

        data = requests.get("http://cn-proxy.com/", headers=self.headers, proxies=self.ss_proxy)
        # print(data.text)

        # 解析网页
        soup = BeautifulSoup(data.text, 'lxml')

        ips_data = soup.find_all('tbody')[-1].find_all('tr')
        # print(ips_data)
        ips = []
        ports = []
        addrs = []
        date_times = []
        for ip_data in ips_data:
            ip = ip_data.find_all('td')[0].get_text()
            ips.append(ip)
            port = ip_data.find_all('td')[1].get_text()
            ports.append(port)
            addr = ip_data.find_all('td')[2].get_text()
            addrs.append(addr)
            date_time = ip_data.find_all('td')[4].get_text()
            date_times.append(date_time)
        # 转化为dataframe
        ips_df = pd.DataFrame()

        ips_df['ip'] = ips
        ips_df['port'] = ports
        ips_df['addr'] = addrs
        ips_df['date_time'] = date_times
        # print(ips_df)
        ips_df.to_csv("china_ips.csv", index=None)

    # 从文件里面随机获取2个代理IP
    def getRandomProxyList(self):
        ipdatas_df = pd.read_csv("china_ips.csv")
        # 　靠前的ＩＰ速度比较快，我们选出速度较快的5个ip
        ipdatas_df = ipdatas_df.head(5)
        ips = ipdatas_df['ip'].tolist()
        ports = ipdatas_df['port'].tolist()

        # proxies_dict = {
        #     "http": "http://113.128.91.174:48888",
        #     "https": "http://113.128.90.54:48888"}
        ip_ports_pool = ["http://" + str(ip) + ":" + str(port) for ip, port in zip(ips, ports)]
        proxies_dict = {}
        proxies_dict['http'] = random.choice(ip_ports_pool)
        return proxies_dict


if __name__ == '__main__':
    myproxy = Mproxy()
    myproxy.get_chinaips()
    print(myproxy.getRandomProxyList())
