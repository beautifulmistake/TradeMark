"""
此版代码是在破解了列表页的加密参数之后对第一版的改版：
1、首先请求：https://www.wipo.int/branddb/en/ 获取页面加载的随机字符串（zk，也就是qk),这个字符串用于后续生成qi的0-----用于后续的图片和详情页的请i求
2、将获取的cookies保存，后续的请求可能需要会话的保持
3、根据获取的qi参数和页号，调用解密函数，得到请求列表页的加密参数，真正的请求从此处发起（列表页的数据）
4、解析列表页数据（列表页数据为json,对我们也有用，将其写入文件中，保存），从列表页的响应中获取两个参数用于构造详情页的请求
"""
import json
import os
import re
import scrapy
from scrapy.exceptions import CloseSpider
from scrapy.signals import spider_closed
from scrapy.spidermiddlewares.httperror import HttpError
from scrapy_redis.spiders import RedisSpider
from twisted.internet.error import TCPTimedOutError, DNSLookupError
from SplashTrademark.items import SplashtrademarkItem


class TradeMarkSpider(RedisSpider):
    name = 'trademark'
    redis_key = "TradeMarkSpider:start_urls"

    def __init__(self, settings):
        super(TradeMarkSpider, self).__init__()
        # 记录列表页的json数据
        self.record_file = open(os.path.join(settings.get("JSON_PATH"), 'record.json'), 'a+', encoding='utf-8')
        self.record_file.write('[')
        self.keyword_file_list = os.listdir(settings.get("KEYWORD_PATH"))
        # 列表页的URL, ajax----> post:参数为qz<-------- page_num 和 qi 共同生成
        self.list_url = 'https://www.wipo.int/branddb/jsp/select.jsp'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
            'Referer': 'https://www.wipo.int/branddb/en/',
            'Host': 'www.wipo.int',
            'Origin': 'https://www.wipo.int',
            'X-Requested-With': 'XMLHttpRequest'
        }
        # 详情页URL--->不包含图片
        self.detail_url = "https://www.wipo.int/branddb/jsp/getData.jsp?qi={}&ID={}&LANG=en&XML={}&NO={}&TOT={}"
        # 详情页的请求--->包含图片
        self.detail_img = "https://www.wipo.int/branddb/jsp/getData.jsp?qi={}&ID={}&LANG=en&XML={}&NO={}&TOT={}&IMG={}"
        # 图片的请求URL 参数说明：KEY=ID，IMG=IMG，qi=qi
        self.image_url = "https://www.wipo.int/branddb/jsp/data.jsp?KEY={}&IMG={}&TYPE=jpg&qi={}"
        # 全局的默认值，此处值修正过
        self.default_value = ["null"]

    def parse_err(self, failure):
        """
        处理各种异常，将请求失败的Request自定义处理方式
        :param failure:
        :return:
        """
        if failure.check(TimeoutError, TCPTimedOutError, DNSLookupError):
            request = failure.request
            self.server.rpush(self.redis_key, request)
        if failure.check(HttpError):
            response = failure.value.response
            self.server.rpush(self.redis_key, response.url)
        return

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        # 获取配置信息
        settings = crawler.settings
        # 爬虫信息
        spider = super(TradeMarkSpider, cls).from_crawler(crawler, settings, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=spider_closed)
        return spider

    def spider_closed(self, spider):
        # 输出日志关闭爬虫
        self.logger.info('Spider closed：%s', spider.name)
        spider.record_file.write("]")
        spider.record_file.close()

    def start_requests(self):
        """
        生成初始请求
        :return:
        """
        # 判断关键字文件是否存在
        if not self.keyword_file_list:
            # 抛出异常，关闭爬虫
            raise CloseSpider("需要关键字文件")
        # 遍历关键字文件
        for keyword_file in self.keyword_file_list:
            # 获取关键字文件路径
            file_path = os.path.join(self.settings.get("KEYWORD_PATH"), keyword_file)
            # 读取关键字文件
            with open(file_path, 'r', encoding='utf-8') as f:
                for keyword in f.readlines():
                    # 消除末尾的空格
                    data = json.loads(keyword.strip(), encoding='utf-8')
                    # print("查看获取的关键字：", data)
                    # 发起请求
                    yield scrapy.FormRequest(url=self.list_url, formdata={
                        'qz': data['qz']
                    }, headers=self.headers, cookies=data['cookies'], meta={
                        'qz': data['qz'], 'cookies': data['cookies']
                    }, callback=self.parse, errback=self.parse_err, dont_filter=True)

    def parse(self, response):
        """
        解析列表页, 获取的为Json数据，此次只采集部分信息：
        1、lastUpdated、
        2、response--->{ docs --->[30条数据]，numFound，start， maxScore}
        3、qi
        :param response:
        :return:
        """
        if response.status == 200:
            try:
                print(response.text)
                res = json.loads(response.text, encoding='utf-8')
                # 获取最近的更新时间----代表着我采集的日期
                # lastUpdated = res.get('lastUpdated')
                # 获取响应主题
                response_ = res.get("response")
                # 获取列表页展示的商标信息
                docs = response_.get('docs')
                # 获取此时的总数据量------TOT参数
                numFound = response_.get('numFound')
                # 获取当前的页号起始的条数-----NO参数
                start = response_.get('start')
                # 获取随机的字符串------qi参数
                qi = res.get("qi")
                # 遍历docs
                for doc in docs:
                    # 每一项都是一条商标信息----dict
                    # 获取每一条商标信息的ID，DOC
                    id = doc.get("ID")
                    xml = doc.get("DOC")
                    img = doc.get("IMG")
                    print("查看获取的img：", img)
                    doc = json.dumps(doc, ensure_ascii=False)
                    self.record_file.write(doc)
                    self.record_file.write(",\n")
                    self.record_file.flush()
                    if img:
                        # 发起详情页的请求，不管有无图片 通过Meta 属性传递的参数是固定的：id,image,qi,无值得赋值为空
                        yield scrapy.Request(url=self.detail_img.format(qi, id, xml, start, numFound, img),
                                             callback=self.parse_detail, headers=self.headers,
                                             meta={'KEY': id, 'IMG': img, 'qi': qi}, errback=self.parse_err,
                                             dont_filter=True)
                    else:
                        yield scrapy.Request(url=self.detail_url.format(qi, id, xml, start, numFound),
                                             callback=self.parse_detail, headers=self.headers, dont_filter=True,
                                             meta={'KEY': id, 'IMG': img, 'qi': qi}, errback=self.parse_err)
            except AttributeError:
                print("请求失败，重新发起请求")
                qz = response.meta['qz']
                cookies = response.meta['cookies']
                # 发起请求
                yield scrapy.FormRequest(url=self.list_url, formdata={
                    'qz': qz
                }, headers=self.headers, cookies=cookies, meta={
                    'qz': qz, 'cookies': cookies
                }, callback=self.parse, errback=self.parse_err, dont_filter=True)

    def parse_detail(self, response):
        """
        解析详情页的数据，将获取的数据全部解析保存
        :param response:
        :return:
        """
        if response.status == 200:
            print("查看获取的响应：", response.text)
            # 获取Meta中传递的参数
            id = response.meta['KEY']
            img = response.meta['IMG']
            qi = response.meta['qi']
            # item 对象
            item = SplashtrademarkItem()
            # 创建存放title的列表
            title = list()
            # 创建存放标题内容的列表
            title_text = list()
            inid_num = len(response.xpath('//div[@id="documentContent"]/div[@class="inid"]').extract())
#######################################################################################################################
            # # 获取总的inid的数量
            # inid_num = len(response.xpath('//div[@id="documentContent"]/div[@class="inid"]').extract())
            # ###############################################################
            # # 增加商标隶属国别字段,获取的是列表形式
            # mark_country = response.xpath('//div[@id="topHeader"]/h4/text()').extract()
            # # 在title中设置 country 键
            # title.append("country")
            # # 在title_text 中增加国家名称
            # title_text.append(re.sub('\W', ' ', " ".join(mark_country)))
            # ################################################################
            # # 获取mark的标题，第一个是固定的
            # mark_title = response.xpath('//div[@id="documentContent"]/h2/text()|'
            #                             '//div[@id="documentContent"]/h2/span/text()|'
            #                             '//div[@id="documentContent"]/h2/div[child::text()]').extract()
            # title.append(re.sub('\W', ' ', " ".join(mark_title)).strip())
            # mark_text = response.xpath('//div[@id="documentContent"]/div[1]/text()').extract()
            # title_text.append(" ".join(mark_text).strip())
            # # 设置一个初始变量
            # start = 1
            # while start < inid_num:
            #     title_info = response.xpath('//div[@id="documentContent"]/div[@class="inid"][{}]/'
            #                                 'child::*/text()'.format(start)).extract()
            #     title.append(re.sub('\W', ' ', " ".join(title_info)).strip())
            #     title_info_text = response.xpath('//div[@id="documentContent"]/'
            #                                      'div[@class="text"][{}]/text()|'
            #                                      '//div[@id="documentContent"]/'
            #                                      'div[@class="text"][{}]/img/@src'.format(start + 1, start + 1)
            #                                      ).extract()
            #     title_text.append(" ".join(re.sub('\s', ' ', title) for title in title_info_text).strip())
            #
            #     start += 1
            # # 获取最后一个标签的数据
            # title_class = response.xpath('//div[@id="documentContent"]/div[@class="inid"][{}]/'
            #                              'div[@class="inidText"]/text()'.format(start)).extract()
            # title.append(re.sub('\W', ' ', " ".join(title_class)).strip())
            # # 获取最后一个标签的内容，一般是 dd -- dl 的结构,这获取的是一个Element对象，使用re将文本提取出来
            # title_class_text = response.xpath('//div[@id="documentContent"]/'
            #                                   'div[@class="text"][last()]/dl/child::*/text()|'
            #                                   '//div[@id="documentContent"]/div[@class="text"][last()]/text()').extract()
            # title_text.append(" ".join(title_class_text).strip())
            # # 将最后的结果进行打包生成字典
            # print("查看获取的title列表项：===========", title)
            # print("查看获取的title_text列表项：===========", title_text)
#######################################################################################################################
            # 以下代码为解决测试中发现数据依然会有错位的现象
            # 第一个字段为国别字段，依然不变，单独取值，然后添加到 title---text 列表中
            mark_country = response.xpath('//div[@id="topHeader"]/h4/text()').extract()
            # 在title中设置 country 键
            title.append("country")
            # 在title_text 中增加国家名称
            title_text.append(" ".join(mark_country).strip())
            # 获取商标名称以及状态信息，有时候会没有状态信息，这也是此次需要修正的部分
            mark_title = response.xpath('//div[@id="documentContent"]/h2/descendant-or-self::text()|'
                                        '//div[@id="documentContent"]/h2/span/text()|'
                                        '//div[@id="documentContent"]/h2/div[child::text()]').extract()
            title.append(re.sub(r'\n|\t|\r', ' ', " ".join(mark_title)).strip())
            # 获取商标的状态，可能不存在，必要的逻辑判断
            # 获取 mark_title 之后的所有同级标签的第一个标签，可能是 text 也可能不是
            next_fir = response.xpath('//div[@id="documentContent"]/h2/following-sibling::div[1]/@class').extract_first()
            # print("查看第一个标签：", next_fir)
            # 获取 mark_title 之后所有有 class 属相的div
            # all_text = response.xpath('//div[@id="documentContent"]/h2/'
            #                           'following-sibling::div/@class').extract()
            # print("查看所有的 text 属相标签：", all_text)
            # 判断是否包含在 text 属性中
            if next_fir == 'text':
                mark_text = response.xpath('//div[@id="documentContent"]/h2/following-sibling::div[1]/text()').extract()
                title_text.append(re.sub(r'\n|\r|\t', ' ', " ".join(mark_text).strip()))
            else:
                mark_text = self.default_value
                title_text.append(re.sub(r'\n|\r|\t', ' ', " ".join(mark_text).strip()))
            # 设置一个初始变量
            start = 1
            while start <= inid_num:
                title_info = response.xpath('//div[@id="documentContent"]/div[@class="inid"][{}]/'
                                            'child::*/text()'.format(start)).extract()
                title.append(re.sub(r'\r|\n|\t', ' ', " ".join(title_info).strip()))
                # 获取该标签的紧邻标签
                next_close = response.xpath('//div[@id="documentContent"]/div[@class="inid"][{}]/'
                                            'following-sibling::div[1]/@class'.format(start)).extract_first()
                # print("查看近邻标签的属性值：", next_close)
                # # 获取所有的 text 标签
                # all_texts = response.xpath('//div[@id="documentContent"]/div[@class="inid"][{}]/'
                #                            'following-sibling::div[starts-with(@class, "text")]/@class'
                #                            .format(start)).extract()
                if next_close == "text":
                    title_info_text = response.xpath('//div[@id="documentContent"]/div[@class="inid"][{}]/'
                                                     'following-sibling::div[1]/descendant-or-self::text()|'
                                                     '//div[@id="documentContent"]/div[@class="inid"][{}]/'
                                                     'following-sibling::div[1]/img/@src|'
                                                     '//div[@id="documentContent"]/div[@class="inid"][{}]/'
                                                     'following-sibling::div[1]/dl/child::*/text()'
                                                     .format(start, start, start)).extract()
                    # print("查看获取的 title_info_text：", title_info_text)
                    title_text.append(re.sub(r'\n|\r|\t', ' ', " ".join(title_info_text).strip()))
                else:
                    title_info_text = self.default_value
                    title_text.append(re.sub(r'\n|\r|\t', ' ', " ".join(title_info_text).strip()))
                start += 1
#######################################################################################################################
            print("查看获取的title列表项：===========", title)
            print("查看获取的title_text列表项：===========", title_text)
            # 将字段打包成字典格式
            dict_ = dict(zip(title, title_text))
            # 此处写构造image_urls的逻辑,特别需要注意的是这里必须返回的是一个 [ image_urls ] 的列表
            image_url = list()
            # 此处的取值也修正过 [0]---->去掉
            url = self.image_url.format(id, img, qi) if img else self.default_value[0]
            image_url.append(url)
            item['image_urls'] = image_url
            item['info'] = dict_
            yield item
