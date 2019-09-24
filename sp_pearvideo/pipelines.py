# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exporters import JsonLinesItemExporter
import pymongo
from scrapy.pipelines.files import FilesPipeline
import scrapy
from scrapy.exceptions import DropItem
import oss2
import requests


# 保存数据为json文件
class SpPearvideoPipeline(object):
    def __init__(self):
        self.fp = open("pear.json", 'wb')
        self.exporter = JsonLinesItemExporter(self.fp, ensure_ascii=False, encoding='utf-8')

    def open_spider(self, spider):
        print('爬虫开始了。。。')

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

    def close_spider(self, spider):
        self.fp.close()
        print('爬虫结束了。。。')


# 下载视频文件到本地
class VideoDownloadPipeline(FilesPipeline):

    def get_media_requests(self, item, info):
        yield scrapy.Request(url=item['video_link'])

    def item_completed(self, results, item, info):
        file_paths = [x['path'] for ok, x in results if ok]
        if not file_paths:
            raise DropItem("Item contains no files")
        # item['file_paths'] = file_paths
        return item

    def file_path(self, request, response=None, info=None):
        """自定义视频保存路径"""
        url = request.url
        file_name = url.split('/')[-1]
        return file_name


# 同步存储到Mongodb
class SaveMongodbPipeline(object):

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
            mongo_db=crawler.settings.get("MONGO_DB")
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        name = item.__class__.__name__
        self.db[name].insert_one(dict(item))
        return item

    def close_spider(self, spider):
        self.client.close()


# 下载视频文件到云OSS对象存储
class UploadtoAliOssPipeline(object):
    def __init__(self, accesskeyid, accesskeysecret):
        self.accesskeyid = accesskeyid
        self.accesskeysecret = accesskeysecret
        # 阿里云主账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM账号进行API访问或日常运维，请登录 https://ram.console.aliyun.com 创建RAM账号。
        self.auth = oss2.Auth(self.accesskeyid, self.accesskeysecret)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            accesskeyid=crawler.settings.get("ACCESS_KEY_ID"),
            accesskeysecret=crawler.settings.get("ACCESS_KEY_SECRET")
        )

    def open_spider(self, spider):
        print('开始上传到Oss对象存储。。。')

    def process_item(self, item, spider):
        # # Endpoint以杭州为例，其它Region请按实际情况填写。
        bucket = oss2.Bucket(self.auth, 'http://oss-cn-hangzhou.aliyuncs.com', 'pearvideoes')
        # requests.get返回的是一个可迭代对象（Iterable），此时Python SDK会通过Chunked Encoding方式上传。
        url = item['video_link']
        video_stream = requests.get(url)
        video_name = url.split('/')[-1]
        bucket.put_object(video_name, video_stream)
        return item

    def close_spider(self, spider):
        print('上传结束。。。')
