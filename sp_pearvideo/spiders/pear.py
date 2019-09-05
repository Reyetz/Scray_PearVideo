# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re
from sp_pearvideo.items import SpPearvideoItem


class PearSpider(CrawlSpider):
    name = 'pear'
    allowed_domains = ['pearvideo.com']
    start_urls = ['http://pearvideo.com/']

    rules = (
        Rule(LinkExtractor(allow=r'video_\d+'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'category_\d+'), follow=True),
        Rule(LinkExtractor(allow=r'tag_\d+'), follow=True),
        Rule(LinkExtractor(allow=r'popular'), follow=True),
        Rule(LinkExtractor(allow=r'popular_\d+'), follow=True),
    )

    def parse_item(self, response):
        item = SpPearvideoItem()
        try:
            video_link_js = response.xpath('.//script[@type="text/javascript"]/text()').getall()
            for js in video_link_js:
                video_link = re.search(r'.*?srcUrl="(.*?)".*?', js, re.S)
                if video_link:
                    video_link = video_link.group(1)
                    break
            box_info = response.xpath('.//div[@class="video-tt-box"]')
            box_detail = response.xpath('.//div[@class="details-content-describe"]')
            tags = response.xpath('.//div[@class="tags"]/a')
            title = box_info.xpath('.//h1[@class="video-tt"]/text()').get()
            date = box_info.xpath('.//div[@class="date"]/text()').get()
            fav = box_info.xpath('.//div[@class="fav"]/text()').get()
            # data_id1 = box_info.xpath('.//div[@class="fav"]/@data-id').get()
            author_id_link = box_detail.xpath('./div/a/@href').get()
            author_id = re.search(r'\d+', author_id_link).group(0)
            logo_link = box_detail.xpath('.//div[@class="col-name"]//img/@src').get()
            author_name = box_detail.xpath('.//div[@class="col-name"]/text()').get()
            sign = box_detail.xpath('./div/a/text()').get()
            content = box_detail.xpath('.//div[@class="summary"]/text()').get()
            comm_ul = response.xpath('.//ul[@class="main-comm-list"]/li')
            author = {
                'id': author_id,
                'name': author_name,
                'logo_link': logo_link,
                'sign': sign
            }
            tag_list = []
            comment_list = []
            if tags:
                for a in tags:
                    tag = a.xpath('./span/text()').get()
                    tag_list.append(tag)
            if comm_ul:
                for comm_li in comm_ul:
                    comm_name = comm_li.xpath('.//div[@class="comm-name"]/a/text()').get()
                    comm_content = comm_li.xpath('.//div[@class="comm-cont"]/text()').get()
                    comm_date = comm_li.xpath('.//span[@class="date"]/text()').get()
                    comm_zan = comm_li.xpath('.//span[@class="zan"]/text()').get()
                    comm_ping = comm_li.xpath('.//span[@class="ping"]/text()').get()
                    comment = {
                        'comm_name': comm_name,
                        'comm_content': comm_content,
                        'comm_date': comm_date,
                        'comm_zan': comm_zan,
                        'comm_ping': comm_ping,
                    }
                    comment_list.append(comment)
            item['video_link'] = video_link
            item['title'] = title
            item['date'] = date
            item['fav'] = fav
            item['author'] = author
            item['content'] = content
            item['tags'] = tag_list
            item['comments'] = comment_list
        except Exception as e:
            print(e)
        yield item
