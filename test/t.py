# from network.useragent import headers
def main():
    pass

if __name__ == '__main__':
    # print(headers)
    # print(headers)

    # for i in range(0, 100, 10):
    #     print(i+1, i+10)
    print([(i+1, i+10) for i in range(0,100, 10)])
    req = "http://z.cn"
    print(["{}&low-price={}&high-price={}".format(req, i+1, i+10) for i in range(0, 100, 10)])