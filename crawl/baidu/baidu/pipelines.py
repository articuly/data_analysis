# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
import scrapy


class BaiduPipeline(object):
    def process_item(self, item, spider):
        print(item)
        return item


class DownloadImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for image_url in item['urls']:
            yield scrapy.Request(image_url)
