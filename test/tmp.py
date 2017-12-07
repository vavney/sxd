import asyncio
import aioredis, aiohttp
import urllib.parse
import re
import math

REDIS_C = 'redis://:foobared@127.0.0.1:6379/1'


class RDSSS:
    def __init__(self, loop=None):
        self.loop = loop or asyncio.get_event_loop()
        self.session = aiohttp.ClientSession(loop=self.loop)

    async def fetch(self, url):
        # print(url)
        rep = await self.session.get(url)
        print(rep.status)
        text = await rep.read()

        pattern_book_total = '''显示： 1-16条， 共(.*?)条'''
        re_result = re.findall(pattern_book_total, text.decode('utf-8'))
        print(re_result)
        if len(re_result) > 0:
            cu = urllib.parse.urlparse(url)
            total = int(''.join(re_result[0].split(',')))
            if total <= 16:
                '''only one page'''
                str_one = "{}://{}{}/ref=sr_pg_{}?{}&page={}".format(cu.scheme, cu.netloc, cu.path, 1, cu.query, 1)
                print(str_one)
            if 16 < total <= 16*75:
                    '''multiply pages'''
                    pagination = int(math.ceil(int(total) / 16))
                    for page in range(1, pagination + 1):
                        str_two = "{}://{}{}/ref=sr_pg_{}?{}&page={}".format(cu.scheme, cu.netloc, cu.path, page, cu.query, page)
                        print(str_two)
            print(total)
        else:
            print("no total")

    async def go(self):
        print('go func...')
        try:
            while True:
                redis = await aioredis.create_redis(
                    REDIS_C, encoding='utf-8')
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