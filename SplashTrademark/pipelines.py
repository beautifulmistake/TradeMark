# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os

import scrapy
from scrapy.exceptions import DropItem
from scrapy.exporters import JsonLinesItemExporter
from scrapy.pipelines.images import ImagesPipeline


class SplashtrademarkPipeline(object):
    def process_item(self, item, spider):
        return item


class JsonExportPipeline(object):
    def __init__(self, settings):
        self.save_file = open(os.path.join(settings.get("RESULT_PATH"), "trademark.json"), "ab")
        self.exporter = JsonLinesItemExporter(self.save_file, encoding="utf-8", ensure_ascii=False)
        self.exporter.start_exporting()

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(settings)

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.save_file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class TrademarkSpiderPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        """
        这是首先调用的方法，处理请求对象，每一组item中图片的链接, 传递item对象，以便下一环节能使用
        :param item:
        :param info:
        :return:
        """
        for image_url in item['image_urls']:
            # 此处增加判断是避免在取不到值的时候，报KeyValue的错，而丢失此item,null 是我设置的全局默认值
            if image_url != "null":
                # 请求下载图片
                yield scrapy.Request(image_url, meta={'item': item})

    def file_path(self, request, response=None, info=None):
        """
        这是第二个调用的方法，主要用来处理文件的分类保存/文件命名等一系列问题
        自定义方法修改图片的命名方法：图片下载下来之后实现以图片的原名称保存
        因为此时请求的图片URL是 ID，IMG，qi 三个参数共同构造的，IMG 虽然能代表此图片，但不方便后期的图片与商标信息的一一对应，放弃使用
        故此处采用ID来命名，一来这是国别加id号组成的唯一识别码，这样携带国别信息，页方便后期的图片与商标的一一对应
        :param request:
        :param response:
        :param info:
        :return:
        """
        image_name = request.url.split('&')[0][46:]  # 取原url的图片命名
        return 'full/%s.jpg' % image_name

    def item_completed(self, results, item, info):
        """
        这是在一个item中所有的图片下载完毕后才调用的方法，
        处理对象：每一组中的item中的图片
        :param results:
        :param item:
        :param info:
        :return:
        """
        # 下载成功图片的路径
        image_path = [x['path'] for ok, x in results if ok]
        # 此处还缺一个图片下载失败后的处理部分

        if not image_path:
            # 如果不包含图片，尝试将 image_paths 设置为默认值
            item['image_paths'] = "null"
            # raise DropItem("Item 中 不包含图片")
            return item
        item['image_paths'] = image_path
        return item
