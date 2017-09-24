'''
手机通过坚果云，编辑PC文件，坚果云自动程序扫描
/home/shensir/Nutstore/MyLover/Lover.txt
'''
import re


def get_myword():
    with open("/home/shensir/Nutstore/MyLover/Lover.txt", 'r') as f:
        data = f.read()

    if len(data) == 0:
        my_word = '并没有写什么。。。搬砖ing。。。'
        print(my_word)
        return my_word

    all_words = re.findall(r'(\d+.\d+.\d+ \d+:\d+)\n(.*?)\n', data)
    my_word = all_words[0]  # 取出第一条数据

    # 将剩余的文件重新保存，覆盖原来的文件
    with open("/home/shensir/Nutstore/MyLover/Lover.txt", 'w') as f:
        for i in range(1, len(all_words)):
            f.write(all_words[i][0])
            f.write('\n')
            f.write(all_words[i][1])
            f.write('\n\n')

    print(my_word)
    return my_word

if __name__=='__main__':
    my_word = get_myword()