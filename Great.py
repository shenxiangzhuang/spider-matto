# -*- coding: utf-8 -*-

from MEmail import send_ms
from NewsSpider import MNewsSpider
from WordSpider import GreateSentence
from Mword import get_myword


# 获取新闻[dataframe with ttles and hrefs as col-names]
def getRoiNews(record=True):
    mynewsspider = MNewsSpider()
    mynewsspider.getNewsRoiData()
    latest_roi = mynewsspider.saveLatestRoi()
    if record:
        mynewsspider.record()
    return latest_roi


# 发送邮件到邮箱提醒
def send_report_word(roi):
    # 新闻数据
    length = len(roi)
    if length > 0:
        s1 = '本次共探测到' + str(length) + '条相关新闻' + '\n'
        s2 = ''
        for title_href_index in range(length):
            s2 += roi['titles'][title_href_index]
            s2 += "->"
            s2 += roi['hrefs'][title_href_index]
            s2 += '\n'
        s_news_report = s1 + s2
    else:
        s_news_report = "啊哦~今天好像没有发现赵丽颖最新的信息~"

    # 句子迷数据
    greatesentence = GreateSentence()
    try:
        sentence_data = greatesentence.get_greatesent_data()
    except:
        sentence_data = greatesentence.get_myown_sentence()

    # 我的随笔
    s_my_word = get_myword()

    # 组织格式
    s = ''
    # 头部
    s += '=' * 8 + "小小白一号在此！" + '=' * 8 + '\n'
    # 　新闻
    s += '=' * 8 + '赵丽颖的新闻' + '=' * 8 + '\n'
    s += s_news_report
    s += '\n'

    # 句子迷
    s += '=' * 8 + '每天一口毒鸡汤' + '=' * 8 + '\n'
    if len(sentence_data) == 3:
        s += sentence_data[0] + '\n'
        s += '----' + sentence_data[1] + ', ' + sentence_data[2]
    else:
        s += sentence_data
    s += '\n'

    # 随笔
    s += '=' * 8 + '我的地球日记[绝密:-)]' + '=' * 8 + '\n'
    if len(s_my_word) == 2:
        s += '现在是' + s_my_word[0] + '\n'
        s += s_my_word[1]
    else:
        s += s_my_word
    s += '\n'

    # 尾部
    s += '=' * 8 + "小小白一号先去搬砖了！" + '=' * 8

    my_email = 'xxx'
    send_ms(s, my_email)
    her_email = 'xxx'
    send_ms(s, her_email)


def GreateGO():
    Latest_Roi = getRoiNews()
    send_report_word(Latest_Roi)
    print('OK!')


if __name__ == '__main__':
    GreateGO()
