# -*- coding: utf-8 -*-

# Scrapy settings for sp_pearvideo project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'sp_pearvideo'

SPIDER_MODULES = ['sp_pearvideo.spiders']
NEWSPIDER_MODULE = 'sp_pearvideo.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'sp_pearvideo (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# 延迟下载（/秒）
# DOWNLOAD_DELAY = 1.5
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# 禁用Cookies
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
    Chrome/76.0.3809.100 Safari/537.36',
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'sp_pearvideo.middlewares.SpPearvideoSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'sp_pearvideo.middlewares.SpPearvideoDownloaderMiddleware': 543,
    # 'sp_pearvideo.middlewares.ProxyMiddleware': 500,
    # 'sp_pearvideo.middlewares.RandomUserAgentMiddleware': 520,
    # 设置不参与scrapy的自动重试的动作
    # 'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
    # 'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': 600,
    # 'sp_pearvideo.middlewares.AutoProxyDownloaderMiddleware': 601,
    # 'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 750,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    # 'sp_pearvideo.pipelines.SpPearvideoPipeline': 300,
    'sp_pearvideo.pipelines.SaveMongodbPipeline': 400,
    # 'sp_pearvideo.pipelines.UploadtoAliOssPipeline': 200,
    # 'sp_pearvideo.pipelines.VideoDownloadPipeline': 1,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
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
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# The params of connecting the mongodb
MONGO_URI = 'mongodb://127.0.0.1:27017'
MONGO_DB = 'PearVideoDB'

# 视频下载保存路径(重写了FilesPipeline默认输出路径：file_dir)
FILES_STORE = r'E:\PearVideo'
