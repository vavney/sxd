import asyncio
import aioredis, aiohttp
import urllib.parse
import re, hashlib
import math
from network.useragent import headers

REDIS_CONNECT = 'redis://@127.0.0.1:6379/1'

import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient('localhost', 27017)
db = client.zcn_pagination_a
db = client['zcn_pagination_a']

MAX_TASKS = 10
MAX_TRIES = 4
PROXY_PRI = "http://wayne4v:Minmin0412.@111.231.215.30:3999"
# PROXY_PRI = "http://127.0.0.1:3128"
QUEUQ_PRICE = 'price_link_a'
QUEUQ_PAGES = 'pages_a'
QUEUQ_MORE_PAGE = 'pages_more_pages'
QUEUE_NO200 = 'no_200'


class RDSSS:
    def __init__(self, loop=None):
        self.loop = loop or asyncio.get_event_loop()
        self.session = aiohttp.ClientSession(loop=self.loop)

    async def link_parse(self, text, url):
        print(url)
        pattern_book_total = '''((?<=显示： 1-16条， 共)[0-9,]+(?=条 )|(?<=共 )\d+(?= 个结果))'''
        re_result = re.findall(pattern_book_total, text, re.S | re.M)
        print(re_result)
        if len(re_result) > 0:
            cu = urllib.parse.urlparse(url)
            total = int(''.join(re_result[0].split(',')))
            if total <= 16:
                '''only one page'''
                pagination_url = "{}://{}{}/ref=sr_pg_{}?{}&page={}".format(cu.scheme, cu.netloc, cu.path, 1, cu.query,
                                                                            1)
                redis = await aioredis.create_redis_pool(
                    REDIS_CONNECT, minsize=5, maxsize=1000, loop=self.loop)
                '''获取分页链接'''
                await redis.lpush(QUEUQ_PAGES, pagination_url)
                redis.close()
                await redis.wait_closed()
                print("insert success")
            if 16 < total <= 16 * 75:
                '''multiply pages'''
                pagination = int(math.ceil(int(total) / 16))
                # for page in range(1, pagination + 1):
                ov = pagination + 1
                print("产出{}页数据".format(pagination))
                pagination_url = [
                    "{}://{}{}/ref=sr_pg_{}?{}&page={}".format(cu.scheme, cu.netloc, cu.path, page, cu.query, page) for
                    page in range(1, ov)]
                print(pagination_url)
                redis = await aioredis.create_redis_pool(
                    REDIS_CONNECT, minsize=5, maxsize=1000, loop=self.loop)
                await redis.lpush(QUEUQ_PAGES, *pagination_url)
                redis.close()
                await redis.wait_closed()
                print("insert success")
                # print(pagination_url)
            if total > 16 * 75:
                redis = await aioredis.create_redis_pool(
                    REDIS_CONNECT, minsize=5, maxsize=1000, loop=self.loop)
                await redis.lpush(QUEUQ_MORE_PAGE, url)
                redis.close()
                await redis.wait_closed()
            print(total)
        else:
            pattern_none = '''请输入您在下方看到的字符'''
            print(text)
            nototal = re.findall(pattern_none, text, re.S|re.M)
            # print(nototal)
            if nototal[0] == '请输入您在下方看到的字符':
                print('no total. please insert validate code')

    async def fetch(self, url):
        md5 = hashlib.md5(url.encode('utf-8')).hexdigest()
        result = await db.zcn_collection1.find_one({'id': {'$eq': md5}})
        if result:
            print('url has exists!!!' + url)
            text = result['content'].decode('utf-8')
            print(text)
            await self.link_parse(text, url)
        else:
            tries = 0
            try:
                rep = await self.session.get(url, headers=headers, proxy=PROXY_PRI)
                print(rep.status)
                if rep.status == 200:
                    text = await rep.read()
                    collection_target = {'id': md5, 'content': text, 'req_link': url}
                    await db.zcn_collection1.insert_one(collection_target)
                    await self.link_parse(text.decode('utf-8'), url)
                else:
                    print('no 200')
                    redis = await aioredis.create_redis_pool(
                        REDIS_CONNECT, minsize=5, maxsize=1000, loop=self.loop)
                    await redis.rpush(QUEUQ_PRICE, url)
                    redis.close()
                    await redis.wait_closed()
            except aiohttp.ClientError as client_error:
                tries += 1
                print(client_error)
            except Exception as e:
                print(e)

    async def go(self):
        print('go func...')
        try:
            while True:
                redis = await aioredis.create_redis(
                    REDIS_CONNECT, encoding='utf-8')
                u = await redis.lpop(QUEUQ_PRICE)

                await self.fetch(u)

                redis.close()
                await redis.wait_closed()
        except Exception as e:
            print(e)

    def w(self):
        tasks = [self.go() for _ in range(MAX_TASKS)]
        self.loop.run_until_complete(asyncio.wait(tasks))

    def close(self):
        self.session.close()


if __name__ == '__main__':
    rds = RDSSS()
    try:
        rds.w()
    except Exception as e:
        print(e)
    finally:
        rds.close()
