import urllib.parse

url = "https://www.amazon.cn/s/ref=lp_659981051_nr_n_0?fst=as%3Aoff&rh=n%3A658390051%2Cn%3A%21658391051%2Cn%3A658400051%2Cn%3A658622051%2Cn%3A659981051%2Cn%3A663542051&bbn=659981051&ie=UTF8&qid=1512543902&rnid=659981051&low-price=11&high-price=20"
cu = urllib.parse.urlparse(url.strip())
print(cu)
ov = 10
pagination_url = ["{}://{}{}/ref=sr_pg_{}?{}&page={}".format(cu.scheme, cu.netloc, cu.path, page, cu.query, page) for page in range(1, ov)]
print(pagination_url)

# l = ["{}&low-price={}&high-price={}".format(url.strip(), i+1, i+10) for i in range(0, 100, 10)]
# print(l)