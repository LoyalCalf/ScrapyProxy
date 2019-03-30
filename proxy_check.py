# -*- coding: utf-8 -*-
# @Time    : 2019/3/30 13:33
# @Author  : 陈强
# @FileName: proxy_check.py
# @Software: PyCharm

"""
主要是检测已经加入到可用代理列表中的代理，如果出现多次失效，则将其从列表中删除
"""
from config import available_proxy, MAX_FAILED_NUM
from proxy_spiders import ProxySpiders
from multiprocessing import Process, Lock
import random


class ProxyCheck(object):
    """
    function:更新available_proxy，主要是更新失效次数
    :param ip为需要更新的ip
    """

    def update_proxy(self, ip):
        for proxy in available_proxy:
            if ip == proxy.get_ip():
                proxy.set_failed_count(proxy.get_failed_count() + 1)

                if proxy.get_failed_count() > MAX_FAILED_NUM:
                    available_proxy.remove(proxy)
                break

        if not available_proxy:
            self.reget_proxy()

    """
    function:如果可用代理为空，则重新获取代理ip
    """

    def reget_proxy(self):
        print('---正在重新获取代理---')
        proxy_spider = ProxySpiders()
        proxy_spider.start()

    """
    随机获取一个可用代理
    """

    def get_random_proxy(self):
        if available_proxy:
            proxy_model = random.choice(available_proxy)
            http_type = proxy_model.get_http_type()
            ip = proxy_model.get_ip()
            port = proxy_model.get_port()
            return http_type.lower() + "://" + ip + ":" + str(port)
        else:
            self.reget_proxy()
            return None
