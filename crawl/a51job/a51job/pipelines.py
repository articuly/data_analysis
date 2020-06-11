# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv
from datetime import datetime


class A51JobPipeline(object):
    def open_spider(self, spider):
        self.csvwriter = csv.writer(open('myjobs.csv', 'a', encoding='utf-8'))

    def process_item(self, item, spider):
        self.csvwriter.writerow(item.values())
        return item

    def close_spider(self, item, spider):
        pass


class TimePipeline(object):
    def process_item(self, item, spider):
        print(spider)
        item['update'] = datetime.now()
        print(item)
        return item
