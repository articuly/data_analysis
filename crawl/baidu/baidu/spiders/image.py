# -*- coding: utf-8 -*-
import scrapy
import re
from ..items import BaiduItem


class ImageSpider(scrapy.Spider):
    name = 'image'
    allowed_domains = ['baidu.com']
    start_urls = [
        'https://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=result&fr=&sf=1&fmq=1591890321094_R&pv=&ic=0&nc=1&z=&hd=&latest=&copyright=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&sid=&word=%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD']

    def parse(self, response):
        img_url_reg = "\"middleURL\":\"(.*?)\","
        img_urls = re.findall(img_url_reg, response.text)
        baidu_imgs = BaiduItem()
        baidu_imgs['urls'] = img_urls
        yield baidu_imgs
