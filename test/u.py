import urllib.parse

url = 'https://www.amazon.cn/s/ref=lp_658673051_nr_n_1/459-0177127-1939404?fst=as%3Aoff&rh=n%3A658390051%2Cn%3A%21658391051%2Cn%3A658673051%2Cn%3A1754894071&bbn=658673051&ie=UTF8&qid=1512529027&rnid=658673051'
s = urllib.parse.urlparse(url)
print(s)

g = s.path.split('/')
print(g)
print(len(g))
ds = '/'.join(g[0:-1])
query = s.query
print(query)
print('{}://{}/{}?{}'.format(s.scheme, s.netloc, ds, query))
# print('{}?{}'.format(ds, s['query']))