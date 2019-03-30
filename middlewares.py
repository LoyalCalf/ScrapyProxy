# -*- coding: utf-8 -*-
# @Time    : 2019/3/30 14:20
# @Author  : 陈强
# @FileName: middlewares.py
# @Software: PyCharm

"""
scrapy 中间件的编写方法
"""
import logging
import random

from config import user_agents
from proxy_check import ProxyCheck
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from twisted.internet.error import TimeoutError, ConnectionRefusedError, TCPTimedOutError
from twisted.web._newclient import ResponseNeverReceived


class ProxyMiddleware(object):
    # overwrite process request
    def process_request(self, request, spider):
        # Set the location of the proxy
        proxy = ProxyCheck().get_random_proxy()
        request.meta['proxy'] = proxy


class ProcessException(RetryMiddleware):
    EXCEPTION_LIST = (TimeoutError, ConnectionRefusedError, TCPTimedOutError, ResponseNeverReceived)

    def process_exception(self, request, exception, spider):
        if isinstance(exception, self.EXCEPTION_LIST):
            try:
                proxy = request.meta['proxy']
                if 'http://' in proxy:
                    proxy = proxy.replace('http://', '')
                else:
                    proxy = proxy.replace('https://', '')
                # print('-------timeout------')
                ProxyCheck().update_proxy(proxy.split(':')[0])
            except Exception as e:
                logging.debug("===  访问页面: " + request.url + " 出现异常。\n %s", e)

    def process_response(self, request, response, spider):
        if response.status < 200 or response.status >= 400:
            try:
                proxy = request.meta['proxy']
                if 'http://' in proxy:
                    proxy = proxy.replace('http://', '')
                else:
                    proxy = proxy.replace('https://', '')
                # print('-------timeout------')
                ProxyCheck().update_proxy(proxy.split(':')[0])
            except Exception as e:
                logging.debug("===  访问页面: " + request.url + " 出现异常。\n %s", e)

class UserAgentMiddleware(object):
    """ 换User-Agent """

    def process_request(self, request, spider):
        agent = random.choice(user_agents)
        request.headers["User-Agent"] = agent
