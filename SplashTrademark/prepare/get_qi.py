"""
使用requests实现首次请求，然后获取页面script脚本生成得 qz 参数 和 获取 响应的 cookies
"""
import json
import re
import requests
from requests.cookies import RequestsCookieJar

from SplashTrademark.encryption.generate_parameter import GenerateParameter


# 请求的URL
base_url = "https://www.wipo.int/branddb/en/"
# 首先登录进去的url
first_url = 'https://www.wipo.int/tools/en/gsearch.html?cx=016458537594905406506%3Ahmturfwvzzq&cof=FORID%3A11&q='
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
}
MAX_PAGE_NUM = 3
FILE_PATH = r'E:\SplashTrademark\SplashTrademark\list_urls\urs.json'
# 创建session对象
s = requests.Session()
# jar = RequestsCookieJar


def login():
    """
    首次登录进去主要为获取它的登录Cookies
    :return:
    """

    result = s.get(first_url, headers=headers)
    cookies = requests.utils.dict_from_cookiejar(result.cookies)
    # print(cookies)
    # for cookie in cookies:
    #     # print(cookie)
    #     jar.set(cookie, cookies[cookie])
    return cookies


def get_qi():
    """
    使用requests请求页面
    :return:
    """
    # 请求页面
    result = s.get(base_url, headers=headers)
    # 转换成HTML
    html = parse_response(result)
    # print(html)
    # 正则匹配 qz 参数
    qz = re.findall(r'zk = "(.*?)";', html)[0]
    # print(qz)
    # 获取cookies
    cookies = requests.utils.dict_from_cookiejar(result.cookies)
    # print(cookies)
    return {
        'qi': '0-{}'.format(qz),
        'cookies': cookies
    }


def parse_response(res):
    """
    将获取的响应转换为HTML
    :param res: 响应（text）
    :return: HTML
    """
    try:
        if res.status_code == 200:
            # 测试时使用
            # print("查看获取的响应<login-parse_response>：", res.text)
            # res.encoding = res.apparent_encoding
            # return etree.HTML(res.text, etree.HTMLParser())
            return res.text
        else:
            print("响应的状态码不是200")
            return False
    except Exception as e:
        print(e)


# 测试代码
if __name__ == "__main__":
    # 首次登录
    cookies = login()
    print(cookies)
    qi_cookies = get_qi()
    qi = qi_cookies['qi']
    cookies_ = qi_cookies['cookies']
    cookies.update(cookies_)
    print(cookies)
    g = GenerateParameter()
    with open(FILE_PATH, 'a+', encoding='utf-8') as f:
        for num in range(MAX_PAGE_NUM):
            t = g.parameter_encrypt(qi, num * 30)
            res = {
                'cookies': cookies,
                'qz': t
            }
            if isinstance(res, dict):
                data = json.dumps(res, ensure_ascii=False)
                print(data)
                f.write(data)
                f.write('\n')
