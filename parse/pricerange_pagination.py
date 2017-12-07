import asyncio
import aioredis, aiohttp
import urllib.parse
import re
import math
from network.useragent import headers
REDIS_CONNECT = 'redis://:foobared@127.0.0.1:6379/1'


class RDSSS:
    def __init__(self, loop=None):
        self.loop = loop or asyncio.get_event_loop()
        self.session = aiohttp.ClientSession(loop=self.loop)

    async def link_parse(self, text, url):
        print(url)
        pattern_book_total = '''((?<=显示： 1-16条， 共)[0-9,]+(?=条 )|(?<=共 )\d+(?= 个结果))'''
        re_result = re.findall(pattern_book_total, text.decode('utf-8'), re.S|re.M)
        print(re_result)
        if len(re_result) > 0:
            cu = urllib.parse.urlparse(url)
            total = int(''.join(re_result[0].split(',')))
            if total <= 16:
                '''only one page'''
                pagination_url = "{}://{}{}/ref=sr_pg_{}?{}&page={}".format(cu.scheme, cu.netloc, cu.path, 1, cu.query, 1)
                redis = await aioredis.create_redis_pool(
                    REDIS_CONNECT, minsize=5, maxsize=10, loop=self.loop)
                '''获取分页链接'''
                await redis.lpush('pagination_book_link_a', pagination_url)
                print("insert success")
            if 16 < total <= 16*75:
                '''multiply pages'''
                pagination = int(math.ceil(int(total) / 16))
                # for page in range(1, pagination + 1):
                ov = pagination + 1
                print("产出{}页数据".format(ov))
                pagination_url = ["{}://{}{}/ref=sr_pg_{}?{}&page={}".format(cu.scheme, cu.netloc, cu.path, page, cu.query, page) for page in range(1, ov)]
                print(pagination_url)
                redis = await aioredis.create_redis_pool(
                    REDIS_CONNECT, minsize=5, maxsize=10, loop=self.loop)
                await redis.lpush('pagination_book_link_a', *pagination_url)
                print("insert success")
                # print(pagination_url)
            if total > 16*75:
                redis = await aioredis.create_redis_pool(
                    REDIS_CONNECT, minsize=5, maxsize=10, loop=self.loop)
                await redis.lpush('more_pagination_book_link_a', url)
            print(total)
        else:
            print("no total")

    async def fetch(self, url):
        rep = await self.session.get(url, headers=headers)
        print(rep.status)
        if rep.status == 200:
            text = await rep.read()
            await self.link_parse(text, url)
        else:
            print('no 200')
            redis = await aioredis.create_redis_pool(
                REDIS_CONNECT, minsize=5, maxsize=10, loop=self.loop)
            await redis.rpush('more_pagination_book_link_no200_a', url)

    async def go(self):
        print('go func...')
        try:
            while True:
                redis = await aioredis.create_redis(
                    REDIS_CONNECT, encoding='utf-8')
                u = await redis.lpop('price_link_c')

                await self.fetch(u)

                redis.close()
                await redis.wait_closed()
        except Exception as e:
            print(e)

    def w(self):
        tasks = [self.go() for _ in range(2)]
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