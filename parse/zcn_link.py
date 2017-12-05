import asyncio
import aiohttp
import re, cgi, urllib
from asyncio import Queue

MAX_TASK = 5
class ZCNLink:
    def __init__(self, roots, loop=None):
        self.roots = roots
        self.loop = loop or asyncio.get_event_loop()
        self.session = aiohttp.ClientSession(loop=self.loop)
        self.q = Queue(loop=self.loop)
        self.seen_urls = set()
        for root in roots:
            self.q.put_nowait(root)
            self.seen_urls.add(root)


    async def fetch(self, url):
        print(url)
        rep = await self.session.get(url)
        if rep.status == 200:
            text = await rep.read()
            # print(text.decode('utf-8'))
            links = self.parse_links(text)
            # print(links)

    def parse_links(self, text):
        text = text.decode('utf-8')
        urls = set(re.findall(r'''(?i)href=["']([^\s"'<>]+)''', text))
        print(urls)
        # return urls
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
        'http://httpbin.org/',
        'https://news.baidu.com'
    ]
    loop = asyncio.get_event_loop()

    zcn = ZCNLink(roots)
    crawler = zcn.crawler()
    try:
        loop.run_until_complete(crawler)
    except KeyboardInterrupt:
        # sys.stderr.flush()
        print('\nInterrupted\n')
    finally:
        zcn.close()
        loop.close()
