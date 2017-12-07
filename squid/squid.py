# -*- coding: utf-8 -*-
import os
import time
import requests

PEER_CONF = "cache_peer %s parent %s 0 no-query weighted-round-robin weight=1 connect-fail-limit=2 allow-miss max-conn=100\n"
def update_conf(proxies):
    with open('/etc/squid/squid.conf.original', 'r') as F:
        squid_conf = F.readlines()
    squid_conf.append('\n# Cache peer config\n')
    for proxy in proxies:
        squid_conf.append(PEER_CONF % (proxy[0], proxy[1]))
    with open('/etc/squid/squid.conf', 'w') as F:
        F.writelines(squid_conf)
def get_proxy():
    #api_url = "http://svip.kuaidaili.com/api/getproxy/?orderid=951066632340445&num=10&b_pcchrome=1&b_pcie=1&b_pcff=1&protocol=2&method=2&an_an=1&an_ha=1&quality=2&sort=1&format=json&sep=1"
    # api_url = "http://svip.kuaidaili.com/api/getproxy/?orderid=951066632340445&num=20&b_pcchrome=1&b_pcie=1&b_pcff=1&protocol=2&method=2&an_an=1&an_ha=1&sp2=1&format=json&sep=1"
    # api_url = 'http://svip.kuaidaili.com/api/getproxy/?orderid=951066632340445&num=100&b_pcchrome=1&b_pcie=1&b_pcff=1&carrier=1&protocol=1&method=2&an_an=1&an_ha=1&format=json&sep=1'
    # api_url = 'http://svip.kuaidaili.com/api/getproxy/?orderid=951066632340445&num=30&b_pcchrome=1&b_pcie=1&b_pcff=1&protocol=1&method=2&an_an=1&an_ha=1&sp1=1&quality=2&format=json&sep=1'
    # api_url = 'http://svip.kuaidaili.com/api/getproxy/?orderid=951066632340445&num=30&b_pcchrome=1&b_pcie=1&b_pcff=1&protocol=2&method=2&an_an=1&an_ha=1&sp1=1&quality=1&format=json&sep=1'
    api_url = 'http://svip.kuaidaili.com/api/getproxy/?orderid=951066632340445&num=20&b_pcchrome=1&b_pcie=1&b_pcff=1&protocol=1&method=2&an_an=1&an_ha=1&sp1=1&quality=2&format=json&sep=1'
    r = requests.get(api_url)
    json = r.json()

    proxy_list = json["data"]["proxy_list"]
    # print proxy_list
    # print(proxy_list[1])
    proxies = []
    for p in proxy_list:
        proxies.append(p.strip().split(":"))
    # print proxies
    update_conf(proxies)
    os.system('sudo squid -k reconfigure')
    print(time.asctime( time.localtime(time.time()) )+': done')

def timer(n):
    while True:
        get_proxy()
        time.sleep(n)

def main():

    timer(60)
if __name__ == '__main__':
    main()

    #nohup python -u squid.py > get_squid2.log 2>&1 &
    # 13072