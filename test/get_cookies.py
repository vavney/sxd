# import requests
# import browsercookie
# cj = browsercookie.chrome()
# # print(cj)
# r = requests.get('http://z.com', cookies=cj)
# print(r)
import browser_cookie3
# import requests
cj = browser_cookie3.chrome(domain_name='www.amazon.cn')
print(list(cj))
# r = requests.get(url, cookies=cj)
# get_title(r.content)