import requests
from network.useragent import headers
import re
import math

import urllib.parse

CATEGORY_URL = "https://www.amazon.cn/s?fst=as%3Aoff&rh=n%3A658390051%2Cn%3A%21658391051%2Cn%3A2045366051%2Cn%3A1381749071%2Cn%3A1381810071%2Cn%3A1381863071%2Cn%3A1381869071%2Cn%3A1381870071&bbn=1381869071&ie=UTF8&qid=1512568288&rnid=1381869071&low-price=1&high-price=80"
# TMP = "https://www.amazon.cn/s/ref=sr_pg_2?fst=as%3Aoff&rh=n%3A658390051%2Cn%3A%21658391051%2Cn%3A2045366051%2Cn%3A1381749071%2Cn%3A1381810071%2Cn%3A1381863071%2Cn%3A1381869071%2Cn%3A1381870071%2Cp_36%3A100-8000&page=2&bbn=1381869071&ie=UTF8&qid=1512569898"
# URL = "https://www.amazon.cn/s/ref=sr_pg_1?fst=as%3Aoff&rh=n%3A658390051%2Cn%3A%21658391051%2Cn%3A2045366051%2Cn%3A1381749071%2Cn%3A1381810071%2Cn%3A1381863071%2Cn%3A1381869071%2Cn%3A1381870071&bbn=1381869071&ie=UTF8&qid=1512568288&rnid=1381869071&low-price=1&high-price=80&page=1"
# URL = urllib.parse.urlparse(CATEGORY_URL)
# pagination = 1
# A = "{}ref=sr_pg_{}?{}".format(URL.path, pagination, URL.query, pagination)

def parse_page():
    req = requests.get(CATEGORY_URL, headers=headers)
    text = req.text
    return text
def parse_categroy():
    a = []
    pattern_book_count = '''显示： 1-16条， 共(.*?)条'''
    re_result = re.findall(pattern_book_count,parse_page())
    if len(re_result) > 0:
        book_count = re_result[0]
        pagination = int(math.ceil(int(book_count) / 12))
        url = urllib.parse.urlparse(CATEGORY_URL)
        print(url)
        for i in range(1, pagination+1):
            str = "{}://{}{}/ref=sr_pg_{}?{}&page={}".format(url.scheme, url.netloc, url.path, i, url.query, i)
            a.append(str)
        print(a)
        print(book_count)
        print(pagination)
    #TODO

def main():
    parse_categroy()

if __name__ == '__main__':
    main()