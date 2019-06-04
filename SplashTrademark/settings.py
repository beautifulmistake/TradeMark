# -*- coding: utf-8 -*-

# Scrapy settings for SplashTrademark project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import os

BOT_NAME = 'SplashTrademark'

SPIDER_MODULES = ['SplashTrademark.spiders']
NEWSPIDER_MODULE = 'SplashTrademark.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'SplashTrademark (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'SplashTrademark.middlewares.SplashtrademarkSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
     # 'scrapy_splash.SplashCookiesMiddleware': 723,
     # 'scrapy_splash.SplashMiddleware': 725,
     # 'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
     'SplashTrademark.middlewares.ProxyMiddleware': 400,
     'SplashTrademark.middlewares.RetryOfWipoMiddleware': 220,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   # 'SplashTrademark.pipelines.SplashtrademarkPipeline': 300,
   'SplashTrademark.pipelines.JsonExportPipeline': 300,
   'SplashTrademark.pipelines.TrademarkSpiderPipeline': 1,
   'scrapy_redis.pipelines.RedisPipeline': 400,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# 使用splash时配置
# SPLASH_URL = 'http://40.73.1.39:8050'
# # 配置一个去重的类 DUPE FILTER LASS
# DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
# # Cache 存储 HTTPCACHE STORAGE
# HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'

# 分布式一些配置
# 分布式爬虫添加的配置信息
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"   # 使用scrapy_redis 里的去重组件，不使用scrapy默认的去重方式
SCHEDULER = "scrapy_redis.scheduler.Scheduler"  # 使用scrapy_redis 里的调度器组件，不使用默认的调度器
SCHEDULER_PERSIST = True    # 允许暂停，redis请求记录不丢失
SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderPriorityQueue"    # 默认使用scrapy_redis请求队列形式（优先级）
# 队列形式，请求先进先出
# SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderQueue"
# 栈形式，请求先进后出
# SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderStack"
LOG_LEVEL = 'DEBUG'     # 日志级别
REDIS_HOST = '127.0.0.1'    # 连接本机
REDIS_PORT = '6379'   # 端口
REDIS_PARAMS = {
    # 'password': 'your_password',
    'db': 0
}   # 密码一般不设置，使用数据0

# 一些文件的配置路径
# 一些相关文件的路径设置
JSON_PATH = os.path.join(os.path.dirname(__file__), "record")   # 用于记录搜索的结果（有这个公司还是没有）
KEYWORD_PATH = os.path.join(os.path.dirname(__file__), "list_urls")   # 用于存放列表页的链接的路径
RESULT_PATH = os.path.join(os.path.dirname(__file__), "result")     # 用于存放结果的路径，以上都是文件夹，与spider在同一级目录下

# 配置总页数
TOTAL_PAGE_NUM = 3

# 以下是在有图片下载的时候添加配置信息

IMAGES_STORE = 'E:\\SplashTrademark'    # 添加图片下载路径
IMAGES_URLS_FIELD = 'image_urls'    # 指定存放图片下载链接的字段
IMAGES_RESULT_FIELD = 'images'      # 文件结果所在的字段

