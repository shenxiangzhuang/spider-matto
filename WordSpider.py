import re
import requests
from bs4 import BeautifulSoup
from Mproxy import Mproxy
from fake_useragent import UserAgent

class GreateSentence():
    def __init__(self):
        self.index_url = 'http://www.juzimi.com/'
        self.sentence = []
        self.s = requests.session()
        self.proxy = Mproxy().getRandomProxyList()

    # 获取url网页数据
    def get_webdata(self, url):
        headers = {
            'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) Gecko/20100101 Firefox/55.0"}

        data = self.s.get(url, headers=headers, proxies=self.proxy, timeout=10)
        # print(data.text)
        return data.text

    # 获取句子迷首页数据，获取偶遇佳句url-->greatesent_data_wholeurl
    def get_randomsentUrl_from_index(self):
        index_data = self.get_webdata(self.index_url)
        # print(index_data)
        soup = BeautifulSoup(index_data, 'lxml')
        greatesent_data_parturl = soup.find('a', {'class': 'homethreebu1 homethreebulink'}).get('href')
        greatesent_data_wholeurl = "http://www.juzimi.com" + greatesent_data_parturl
        # print(greatesent_data_wholeurl)
        return greatesent_data_wholeurl

    def get_greatesent_data(self):
        greatesent_data_wholeurl = self.get_randomsentUrl_from_index()
        greatesent_html = self.get_webdata(greatesent_data_wholeurl)
        # print(greatesent_html)
        '''
        三种不同的格式...略麻烦，之后换BS试下
        '''
        try:
            sentence_data = re.findall(r'<meta name="description" content="句子欣赏评论: “(.*?)” 原作者：(.*?) 出处：出自(.*?)" />', greatesent_html)
        except:
            sentence_data = re.findall(r'<meta name="description" content="句子欣赏评论: “(.*?)” 出处：出自(.*?)" />', greatesent_html)
        if len(sentence_data) == 0:
            sentence_data = re.findall(r'<title>佳句赏析_"(.*?)" 原作者 出处 出自 | 句子迷</title>', greatesent_html)
        print(sentence_data[0])

        return sentence_data[0]

    def get_myown_sentence(self):
        with open("/home/shensir/Nutstore/MyLover/MySentence.txt", 'r') as f:
            data = f.read()

        if len(data) == 0:
            my_word = '毒鸡汤卖完了...'
            print(my_word)
            return my_word

        all_words = re.findall(r'@(.*?)\n', data)
        my_word = all_words[0]  # 取出第一条数据

        # 将剩余的文件重新保存，覆盖原来的文件
        with open("/home/shensir/Nutstore/MyLover/MySentence.txt", 'w') as f:
            for i in range(1, len(all_words)):
                f.write('@')
                f.write(all_words[i])
                f.write('\n\n')

        print(my_word)
        return my_word


if __name__ == '__main__':
    greatesentence = GreateSentence()
    sentence_data = greatesentence.get_greatesent_data()
