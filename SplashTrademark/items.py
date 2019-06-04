# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SplashtrademarkItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 商标信息
    info = scrapy.Field()
    # 商标图片
    images = scrapy.Field()  # 必要，不可自定义
    image_urls = scrapy.Field()  # 必要，不可自定义，存放图片下载的路径，必须为一个列表（可迭代对象）
    image_paths = scrapy.Field()  # 存放图片的保存路径
