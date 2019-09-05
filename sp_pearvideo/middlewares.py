# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import logging
import requests
import random
from w3lib.url import safe_url_string
from six.moves.urllib.parse import urljoin
from scrapy.exceptions import IgnoreRequest


class SpPearvideoSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class SpPearvideoDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


# 代理中间件
class ProxyMiddleware(object):
    logger = logging.getLogger(__name__)

    def process_request(self, request, spider):
        pro_addr = requests.get('http://127.0.0.1:5555/random').text
        request.meta['Proxy'] = 'http://' + pro_addr

    def process_exception(self, request, exception, spider):
        self.logger.debug('Try Exception time')
        self.logger.debug('Try second time')
        proxy_addr = requests.get('http://127.0.0.1:5555/random').text
        self.logger.debug(proxy_addr)
        request.meta['Proxy'] = 'http://{0}'.format(proxy_addr)


# 随机User-Agent中间件
class RandomUserAgentMiddleware():
    def __init__(self):
        self.user_agents = [
            'Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)',
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.2 (KHTML, like Gecko) Chrome/22.0.1216.0 Safari/537.2',
            'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:15.0) Gecko/20100101 Firefox/15.0.1',
            'Mozilla/5.0(Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, likeGecko) Chrome/14.0.835.163 Safari/535.1',
            'Mozilla/5.0(Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, likeGecko) Chrome/73.0.3683.103 Safari/537.36',
            'Mozilla/5.0(Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, likeGecko) Chrome/17.0.963.56 Safari/535.11',
            'Mozilla/5.0(Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0',
            'Mozilla/5.0(Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
            'Mozilla/5.0(Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, likeGecko) Version/5.1 Safari/534.50',
            'Mozilla/5.0(Windows; U; Windows NT 6.1; en - us) AppleWebKit/534.50 (KHTML, likeGecko) Version/5.1 Safari/534.50',
            'Opera/9.80(Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11',
            'Opera/9.80(Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
            'Mozilla/5.0(Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) likeGecko',
            'Mozilla/5.0(compatible; MSIE9.0; Windows NT 6.1; Trident/5.0)',
            'Mozilla/4.0(compatible; MSIE7.0; Windows NT 5.1; 360SE)',
            'Mozilla/4.0(compatible; MSIE7.0; Windows NT 5.1; TencentTraveler4.0)',

        ]

    def process_request(self, request, spider):
        request.headers['User-Agent'] = random.choice(self.user_agents)


# 用于重试的代理中间件
class AutoProxyDownloaderMiddleware(object):

    def __init__(self, settings):
        self.proxy_status = settings.get('PROXY_STATUS')
        # See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html?highlight=proxy#module-scrapy.downloadermiddlewares.httpproxy

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            settings=crawler.settings
        )

        # See /site-packages/scrapy/downloadermiddlewares/redirect.py

    def process_response(self, request, response, spider):
        if (request.meta.get('dont_redirect', False) or
                response.status in getattr(spider, 'handle_httpstatus_list', []) or
                response.status in request.meta.get('handle_httpstatus_list', []) or
                request.meta.get('handle_httpstatus_all', False)):
            return response

        if response.status in self.proxy_status:
            if 'Location' in response.headers:
                location = safe_url_string(response.headers['location'])
                redirected_url = urljoin(request.url, location)
            else:
                redirected_url = ''

            # AutoProxy for first time
            if not request.meta.get('auto_proxy'):
                pro_addr = requests.get('http://127.0.0.1:5555/random').text
                proxy_config = 'http://' + pro_addr
                request.meta.update({'auto_proxy': True, 'Proxy': proxy_config})
                new_request = request.replace(meta=request.meta, dont_filter=True)
                new_request.priority = request.priority + 2

                spider.log('Will AutoProxy for <{} {}> {}'.format(
                    response.status, request.url, redirected_url))
                return new_request

            # IgnoreRequest for second time
            else:
                spider.logger.warn('Ignoring response <{} {}>: HTTP status code still in {} after AutoProxy'.format(
                    response.status, request.url, self.proxy_status))
                raise IgnoreRequest

        return response
