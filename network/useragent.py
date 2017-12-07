import random
first_num = random.randint(55, 62)
third_num = random.randint(0, 3200)
fourth_num = random.randint(0, 140)


class FakeChromeUA:
    os_type = [
        '(Windows NT 6.1; WOW64)', '(Windows NT 10.0; WOW64)', '(X11; Linux x86_64)',
        '(Macintosh; Intel Mac OS X 10_12_6)'
    ]

    chrome_version = 'Chrome/{}.0.{}.{}'.format(first_num, third_num, fourth_num)

    @classmethod
    def get_ua(cls):
        return ' '.join(['Mozilla/5.0', random.choice(cls.os_type), 'AppleWebKit/537.36',
                         '(KHTML, like Gecko)', cls.chrome_version, 'Safari/537.36']
                        )


headers = {
    'User-Agent': FakeChromeUA.get_ua(),
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Connection': 'keep-alive',
    'Cookie': "x-wl-uid=12ydJzGKmC9qVailIZJn3IVohgHiaDe2SNzIj71D7J1pyZIZWAw+Jb7pTtm9d5EBHuiPxY1eqgKo=; x-amz-captcha-1=1512665553867321; x-amz-captcha-2=F1poZkajakLurHRLneX9PA==; session-id=459-7578562-2397502; session-id-time=2082787201l; ubid-acbcn=457-2910120-0583448; session-token=\"7OOdANw9uxt6SvO0JvTywt3N5nG3j/Vn54Iq3xo0puuRPWqjIR2JFpUIC5uHWvW19scmlq6TZ8Hm/jCGTCkhGOUKrKfPU0Q+AiD6YR+J9ebVWhHRV36w/8JOi6Xi4VFO1w5rh2sDIpm8wrLex2TIjV9+PKzYBG+DjvivBREk1m3ocHWa3iWOwM0PWV2o2M+Rsh3eB0kIl+iaHrHQ/z3wd0Co0fCs1BxWJJQxUiVBBlaQiK+4eFsnOA==\"; csm-hit=EJAC8WYKJBA6ZPYXN6F2+s-EJAC8WYKJBA6ZPYXN6F2|1512659541062"
}