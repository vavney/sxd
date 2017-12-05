import asyncio
import aiohttp
import uvloop
from contextlib import closing

from network.useragent import headers

def fetch(urls):
    tasks = []
    with closing(asyncio.get_event_loop()) as loop:
        with aiohttp.ClientSession(loop=loop) as session:
            for url in urls:
                tasks.append(fetch_page(session, url))
            pages = loop.run_until_complete(asyncio.gather(*tasks))
    return pages

async def fetch_page(session, url):
    with aiohttp.Timeout(10):
        async with session.get(url) as response:
            assert response.status == 200
            return await response.text()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    urls = ['https://www.baidu.com/s?ie=utf-8&f=3&rsv_bp=0&rsv_idx=1&tn=baidu&wd=1&rsv_pq=bd2b784f000a4c4f&rsv_t=c45e5fWrku34WxMyzQc3bO81aiEMmwR1JZjXe5Mpt%2FULelD%2B9%2BkDOg%2Bvwl4&rqlang=cn&rsv_enter=1&rsv_sug3=1&rsv_sug1=1&rsv_sug7=100&rsv_sug2=0&prefixsug=1&rsp=2&inputT=272&rsv_sug4=272']
    # tasks = [fetch(url) for url in urls]
    # with aiohttp.ClientSession() as session:
    #     loop.run_until_complete(fetch(session, urls))
    # loop.close()
    p = fetch(urls)
    for page in p:
        print(page)