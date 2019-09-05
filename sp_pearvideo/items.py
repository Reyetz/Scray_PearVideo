# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SpPearvideoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    video_link = scrapy.Field()
    title = scrapy.Field()
    date = scrapy.Field()
    fav = scrapy.Field()
    author = scrapy.Field()
    content = scrapy.Field()
    tags = scrapy.Field()
    comments = scrapy.Field()
