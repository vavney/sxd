import asyncio, aiohttp
import re, cgi, urllib.parse, hashlib
from asyncio import Queue
from network.useragent import headers
import time
'''
client = motor.motor_asyncio.AsyncIOMotorClient('localhost', 27017)
db = client.test_database
db = client['test_database']
'''
from pymongo import MongoClient
client = MongoClient()
db = client["zcn_database1"]
collection = db["zcn_collection1"]

import redis
pool=redis.ConnectionPool(host='127.0.0.1',port=6379,db=0, password="foobared")
redis_server = redis.StrictRedis(connection_pool=pool)

MAX_TASK = 50
MAX_TRIES = 3
class ZCNLink:
    def __init__(self, roots, loop=None, mongo=None):
        self.roots = roots
        self.loop = loop or asyncio.get_event_loop()
        # self.mongo = mongo or motor.motor_asyncio.AsyncIOMotorClient('localhost', 27017)
        self.session = aiohttp.ClientSession(loop=self.loop)
        self.q = Queue(loop=self.loop)
        self.seen_urls = set()
        for root in roots:
            self.q.put_nowait(root)
            self.seen_urls.add(root)

    async def fetch(self, url):
        # print("top:" + url)
        tries = 0
        while tries < MAX_TRIES:
            try:
                md5 = hashlib.md5(url.encode('utf-8')).hexdigest()
                result = collection.find_one({"id": md5})
                if result:
                    text = result['content']
                    links = await self.parse_links(text, url)
                    print('解析出的links:')
                    print(links)
                    if links is not None:
                        for link in links.difference(self.seen_urls):
                            self.q.put_nowait(link)
                        self.seen_urls.update(links)
                else:
                    rep = await self.session.get(url, headers=headers)
                    print('go in network!!!!!' + url)
                    if rep.status == 200:
                        text = await rep.read()
                        collection_target = {'id': md5, 'content': text, 'req_link': url}
                        collection.insert_one(collection_target)
                        links = await self.parse_links(text, req_url=url)
                        if links is not None:
                            for link in links.difference(self.seen_urls):
                                self.q.put_nowait(link)
                            self.seen_urls.update(links)
                        else:
                            pass
                break
            except aiohttp.ClientError as client_error:
                tries += 1
                print(client_error)
            except Exception as e:
                print(e)

    def component_link(self, url):
        link = urllib.parse.urlparse(url)
        g = link.path.split('/')
        link_path = '/'.join(g[0:-1])
        return '{}://{}{}?{}'.format(link.scheme, link.netloc, link_path, link.query)

    async def parse_links(self, text, req_url):
        try:
            links = set()
            text = text.decode('utf-8')
            urls = set(re.findall('<li style="margin-left: [-\d]+px">.*?<a href="(/s/ref=lp_\d+_nr_n_[\d+].*?)">.*?<span class="refinementLink">(.*?)</span>.*?</a>.*?</li>',
                                  text, re.S|re.M))
            if urls:
                for url in urls:
                    u, title = url
                    next_url_c = urllib.parse.urljoin(req_url, u.replace('&amp;', '&'))
                    next_url = self.component_link(next_url_c)
                    print(title)
                    print(next_url)
                    if title == "General (科学通俗读物)":
                        pass
                    else:
                        links.add(next_url)
                return links
            else:
                price_links = ["{}&low-price={}&high-price={}".format(req_url, i+1, i+10) for i in range(0, 100, 10)]
                print(price_links)
                redis_server.lpush('prices_link', *price_links)
                print('redis insert success')
        except Exception as e:
            print(e)

    async def worker(self):
        try:
            while True:
                url = await self.q.get()
                assert url in self.seen_urls
                await self.fetch(url)
                self.q.task_done()
        except asyncio.CancelledError:
            pass

    async def crawler(self):
        workers = [asyncio.Task(self.worker(), loop=self.loop) for _ in range(MAX_TASK)]
        await self.q.join()
        for w in workers:
            w.cancel()

    def close(self):
        self.session.close()


if __name__ == '__main__':
    roots = [
        'https://www.amazon.cn/%E5%9B%BE%E4%B9%A6/b/ref=topnav_storetab_b?ie=UTF8&node=658390051'
        # 'https://www.amazon.cn/s/ref=lp_658390051_nr_n_8?fst=as%3Aoff&rh=n%3A658390051%2Cn%3A%21658391051%2Cn%3A118362071&bbn=658391051&ie=UTF8&qid=1512538170&rnid=658391051'
    ]
    t0 = time.time()
    loop = asyncio.get_event_loop()

    zcn = ZCNLink(roots)
    crawler = zcn.crawler()
    try:
        loop.run_until_complete(crawler)
        print('cost time: {}'.format(time.time()-t0))
    except KeyboardInterrupt:
        # sys.stderr.flush()
        print('\nInterrupted\n')
    finally:
        zcn.close()
        loop.close()
