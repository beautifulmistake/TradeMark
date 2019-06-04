"""
此类用来模拟 wipo网站 请求参数的加密过程：
接收一个JSON形式的数据，然后调用 compressToBase64 获取加密后的 请求参数

现在转换思路逻辑判断由 js 部分实现，用Python实现时出错的几率比较大，一个空格的失误都可能造成结果的不一致
"""
import os

from SplashTrademark.encryption.setting import JS_FILE_PATH


class GenerateParameter(object):

    # def order_parameter(self, page_num=None):
    #     """
    #     传入页号，构造出有序的字典
    #     :param page_num:
    #     :return:
    #     """
    #     dict_ = OrderedDict()
    #     if not page_num:
    #         # page_num 参数未传入
    #         # dict_['s'] = {"dis": "flow"}
    #         dict_['type'] = 'brand'
    #         dict_['la'] = 'en'
    #         dict_['qi'] = '0-mdhkn9QsimOjEgZep0FpgccKoYnhw4M5RUuIkb+GCFI='
    #         dict_['queue'] = 1
    #         dict_['_'] = '8742'
    #     else:
    #         dict_['p'] = {'start': page_num}
    #         dict_['s'] = {'dis': 'flow'}
    #         dict_['type'] = 'brand'
    #         dict_['la'] = 'en'
    #         dict_['qi'] = '0-mdhkn9QsimOjEgZep0FpgccKoYnhw4M5RUuIkb+GCFI='
    #         dict_['queue'] = 1
    #         dict_['_'] = '8742'
    #     return dict_
    #
    # def parameter_to_json(self):
    #     """
    #     将参数转换成JSON类型数据
    #     :return:
    #     """
    #     return json.dumps(self.order_parameter(120), ensure_ascii=False)

    def parameter_encrypt(self, qi, page_num=0):
        """
        传递两个参数一个是首次进入页面以后生成的随机字符串，一个是下一页的起始页数
        第一页时默认传递页号为0，每一列表页的数据显示为30条
        下一页的起始(page_num-1)*30
        :return:
        """
        return os.popen(r'node {0} {1} {2}'.format(JS_FILE_PATH, page_num, qi)).read().strip()


# 测试代码
if __name__ == "__main__":
    # 创建对象
    g = GenerateParameter()
    # 调用加密方法
    t = g.parameter_encrypt('0-ugITGfMJmABXcb/+NMDN+RPtiLW4HKYnGL7EH2HMgWs=', 0)
    print("查看加密后的参数：", t)
