# ScrapyProxy
scrapy代理中间件，可以自动获取代理，自动去重，自动检查可用代理个数，没有可用代理时会自动重新获取

# 如何使用
1. 将项目clone到本地
2. 在自己的scrapy爬虫下新建proxy文件夹，将所有文件复制到该文件夹下
3. 注意检查导入包的问题，如果路径不对，请修改导入路径
4. 将middlewares中的代码复制到你自己scrapy项目的middlewares中，同时也要注意路径问题
5. 修改setting如下：
``` Python
    DOWNLOADER_MIDDLEWARES = {
        #注意将SinaSpider修改为你自己的项目名称
       'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
       'SinaSpider.middlewares.UserAgentMiddleware': 100,
       'SinaSpider.middlewares.ProxyMiddleware':101,
       'SinaSpider.middlewares.ProcessException':102,
       'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': None,
       'scrapy.contrib.downloadermiddleware.retry.RetryMiddleware': None,
    }
```

