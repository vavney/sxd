# sxd
on the way
# Todo
- BloomFilter
- change price link to pagination link in redis.
- mongodb data zip
- sub/pub
- cookie jar = aiohttp.DummyCookieJar() session = aiohttp.ClientSession(cookie_jar=jar)
        https://docs.aiohttp.org/en/stable/client.html?highlight=cookie
- 执行chrome,获取cookie  selenium框架 操作chrome，执行js获取
- htmlunit 也可以获取cookie

# DATA
- category:     6579
- redis:        57600


# book link
- 抓取价格10区间的图书,如果大于16*75,则细分抓取
```$xslt
>>> urllib.urlencode({'p': [1, 2, 3]}, doseq=True)
'p=1&p=2&p=3'
```


# STEP
1. zcn_link.py 获取分类下对应的所有价格区间链接
2. pricerange_pagination.py 获取价格区间链接下对应的所有分页链接

3. 获取分页链接下面对应的所有图书链接
4. 获取所有图书详情信息.

# add squid to local
- port 3128

