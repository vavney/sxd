import requests
from network.useragent import headers
import re
import math
import hashlib

from pymongo import MongoClient
client = MongoClient()
db = client["Library"]
collection = db["book_html"]

import urllib.parse

CATEGORY_URL = "https://www.amazon.cn/s?" \
               "fst=as%3Aoff&rh=n%3A658390051%2Cn%3A%21658391051%2Cn%3A2045366051%2Cn%3A1381749071%2Cn%3A1381810071%2Cn%3A1381863071%2Cn%3A1381869071%2Cn%3A1381870071&bbn=1381869071&ie=UTF8&qid=1512568288&rnid=1381869071&low-price=1&high-price=80"

# CATEGORY_URL2 = 'https://www.amazon.cn/s?fst=as%3Aoff&rh=n%3A658390051%2Cn%3A%21658391051%2Cn%3A658438051%2Cn%3A659213051&bbn=658438051&ie=UTF8&qid=1512543826&rnid=658438051&low-price=81&high-price=90'
CATEGORY_URL2 = 'https://www.amazon.cn/s/ref=sr_ex_n_1?rh=n%3A658390051%2Cp_36%3A8100-9000&bbn=658390051&ie=UTF8&qid=1512640886'
'''共 9 个结果'''
'''显示： 1-16条， 共255,359条 '''
# headers={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}

def parse_page():

    md5 = hashlib.md5(CATEGORY_URL2.encode('utf-8')).hexdigest()
    result = collection.find_one({"id": md5})
    if result:
        print(md5)
        print("{} is exists!!!".format(CATEGORY_URL2))
        return result['content']
    else:
        req = requests.get(CATEGORY_URL2, headers=headers)
        text = req.text
        book = {'id': md5, 'content': text}
        collection.insert_one(book)
        return text


def parse_paramer():
    rs = urllib.parse.urlparse(CATEGORY_URL2.strip())
    return dict(urllib.parse.parse_qsl(rs.query))


def books_total():
    t = parse_page()
    # print(t)
    ''' 此处是大坑'''
    # Todo 两处字符串匹配不到 FUCKING
    # pattern_book_total = '<div id="s-result-info-bar-content" class="a-row">.*?<h1 id="s-result-count" class="a-size-base a-spacing-small a-spacing-top-small a-text-normal">(.*?) <span>.*?</span></h1>'

    # pattern_book_total1 = '''共 (.*?) 个结果'''
    # pattern = '''<h1 id="s-result-count" class="a-size-base a-spacing-small a-spacing-top-small a-text-normal">.*?(\d+).*?<span>.*?</span></h1>'''
    pattern = '''((?<=显示： 1-16条， 共)[0-9,]+(?=条 )|(?<=共 )\d+(?= 个结果))'''
    re_result = re.findall(pattern, t, re.S|re.M)
    print(re_result)
    # if len(re_result) > 0:
    #     total = int(''.join(re_result[0].split(',')))
    #     print(total)
    #     return total
    # else:
    #     pass
    '''<h1 id="s-result-count" class="a-size-base a-spacing-small a-spacing-top-small a-text-normal">显示： 1-16条， 共255,359条 <span>'''
    '''<h2 class="resultCount" id="resultCount"><span>显示： 17-32条， 共255,359条</span></h2>'''
def split_g():
    l = 11
    h = 20
    s = int(10 / 2)
    for i in range(l, h, s):
        print(i, i+(s-1))


def parse_categroy():
    total = books_total()
    print(total)
    if total is not None:
        if total <= 16*75:
            pass
            # pagination = int(math.pattern = '''(显示： 1-16条， 共(.*?)条 | 共 (.*?) 个结果)'''
            # math.ceil(int(total) / 16))
            # print(pagination)
        else:
            paramers = parse_paramer()
            # print(paramers['low-price'])
            l = int(paramers['low-price'])
            h = int(paramers['high-price'])
            print(h - l)
            # s = int(h/2)
            for i in range(l, h, 1):
                print(i, i+1)
            # print("too big")
    else:
        print('wrong')
        # a = []
        # pattern_book_count = '''显示： 1-16条， 共(.*?)条'''
        # re_result = re.findall(pattern_book_count, parse_page())
        # if len(re_result) > 0:
        #     book_count = re_result[0]
        #     pagination = int(math.ceil(int(book_count) / 12))
        #     url = urllib.parse.urlparse(CATEGORY_URL)
        #     # print(url)
        #     for i in range(1, pagination + 1):
        #         str = "{}://{}{}/ref=sr_pg_{}?{}&page={}".format(url.scheme, url.netloc, url.path, i, url.query, i)
        #         a.append(str)
        #     print(a)


# def parse_book_list(text):
#     book_list_p = '''<ul class="zg_hrsr">(.*?)</ul>'''
#     book_list_html = re.findall(book_list_p, text, re.S | re.M)


'''分析出book链接'''
def parse_book_link():
    text = parse_page()
    print(text)
    # pattern = '''<a class="a-link-normal s-access-detail-page  s-color-twister-title-link a-text-normal" target="_blank" title=".*?" href="(.*?)">.*?</a>'''
    # pattern2 = '''<a class="a-link-normal s-access-detail-page  s-color-twister-title-link a-text-normal" target="_blank" title="(.*?)" href="(.*?)">.*?</a>'''
    pattern = '''(显示： 1-16条， 共[0-9,]+条 | 共 \d+ 个结果)'''

    books = re.findall(pattern, text, re.S|re.M)

    print(books)


def main():
    books_total()
    # parse_book_link()
    # split_g()
    # parse_categroy()
    # text = parse_page()
    # print(text)
    # t = parse_paramer()
    # print(t)
    # print(t['low-price'])
    # print(t['high-price'])


if __name__ == '__main__':
    main()
