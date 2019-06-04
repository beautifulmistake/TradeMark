#### 请求分析部分


https://www.wipo.int/branddb/jsp/data.jsp?  KEY=CHTM.052642019  &   IMG=20/19/052642019-th.jpg  &   TYPE=jpg    &   qi=0-bBTsf96ntvvc0qeVUZMmo89GQ5zdgFZCMm+9szGtm18=

https://www.wipo.int/branddb/jsp/data.jsp?  KEY=CHTM.052832019  &   IMG=20/19/052832019-th.jpg  &   TYPE=jpg    &   qi=0-bBTsf96ntvvc0qeVUZMmo89GQ5zdgFZCMm+9szGtm18=

https://www.wipo.int/branddb/jsp/data.jsp?  KEY=CHTM.052492019  &   IMG=20/19/052492019-th.jpg  &   TYPE=jpg    &   qi=0-bBTsf96ntvvc0qeVUZMmo89GQ5zdgFZCMm+9szGtm18=



#### 请求分析结果


* get请求

* 请求参数的构造以及来源：
   
  1、https://www.wipo.int/branddb/jsp/data.jsp?------>网页中查询分析
   
  2、KEY ------>ID  （从列表页的数据中获取，此值一定存在）
   
  3、IMG ------>IMG （从列表页的数据中获取，此值在没有图片的时候不存在）------>无此值的时候也要赋值为空，以便后续能判断出无图片
   
  4、TYPE=jpg       (固定值)
   
  5、qi---------->  从列表页的数据中获取）



#### 特别要解决的一个问题

image_urls 在没有的情况下也要进行赋空值的操作，不然在imagepipeline中间件时会报错，然后该条数据会丢失



#### 调试中发现的问题
item 定义的字段中：image_paths 和 image_urls 会被记录在最终的文件（数据库）之中



#### 在编码以及调试中遇见的问题

* 图片如何请求的问题
   
  第一种方案：从详情页里解析获取，首先尝试的是这种方式，有些无图片，需要做判断，有图片的请求URL也不是固定的格式，给后期图片的命名带来了一定的麻烦
   
  第二种方案：从列表页获取的json数据中解析出：ID（KEY）、IMG（IMG）、qi(qi)等信息构造出图片的URL，在图片的命名时使用ID（包含国家和申请后，可唯一定位一个商标）


* 解决图片命名的问题
   
  解决方案：参考上一条的第二中方案的思路


* 处理响应为403状态码的请求（在中间件中增加处理的逻辑，这个请求一般发生在请求详情页时，get请求）


* 解决图片下载失败的问题（测试时共采集三页数据，4/25的失败比例）
   
  暂时不只如何在发起图片请求的pipeline中使用errback方法捕获达到重试次数后抛出的TCP连接错误，然后重新加入队列
   
  故暂时采取的解决方案为，编写一个重试中间件来达到同样的效果（经测试，可以完整的获取25/25图片）


* 解决图片下载失败时该条item会被丢弃的问题（图片虽然下载失败，但该条item包含商标的详细信息，对我们而言是有用的数据，不能丢弃)
   
  解决方案：在item_complted()方法中添加即使image_path为空，赋予默认值，最后将item返回，保证数据不丢失


* 解决某条item中不包含图片时，会抛出 KeyValueError的异常，然后该条数据会被丢弃的问题
   
  解决方案：在get_media_requests()中增加对 image_url 是否为空的逻辑判断


* 增加errback的处理部分，处理多种异常，防止请求的遗漏而丢失数据



#### 运行方法

* 先运行prepare模块中的get_qi方法--------->会完成随机字符串qz的获取，加密参数qi的生成，以及cookies和详情页URL的生成

* 运行scrapy_redis，它会读取keyword文件下的包含URL请求的文件，发起请求，整个爬虫开始运行



#### 待优化的部分

* 破解加密的参数中“_”是变化的，目前还不知其变化的周期
*依照目前的方法，调试中发现cookies还是具有一定的有效性（还是会出现请求详情页失败，列表页没问题）

* 鉴于以上的情况，后期希望增加一个任务队列，按需生成
*采集的策略为：将总页数切分在不同的服务器上进行多级抓取（在生成详情页的URL时，这个可以控制）

* 最终要的就是网站的更新速率要大于我的采集速率，网站每日都在更新
