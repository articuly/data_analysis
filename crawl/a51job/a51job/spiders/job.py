# -*- coding: utf-8 -*-
import scrapy
from ..items import A51JobItem


class JobSpider(scrapy.Spider):
    name = 'job'
    allowed_domains = ['51job.com']

    def start_requests(self):
        for i in range(1, 74):
            url1 = 'https://search.51job.com/list/030200,000000,0000,00,9,99,python,2,'
            url2 = '.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='
            url = url1 + str(i) + url2
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        job_link_xpath = '//div[@id="resultList"]/div[@class="el"]/p/span/a/@href'
        # next_xpath = "//li[@class='bk']/a/@href"

        job_links = response.xpath(job_link_xpath).getall()
        # next_path=response.xpath(next_xpath).get()
        for job_link in job_links:
            print(job_link)
            yield scrapy.Request(job_link, callback=self.job_parse)

    def job_parse(self, response):
        job_name_xpath = "//h1/@title"
        job_money_xpath = "//div[@class='cn']/strong/text()"
        job_info_xpath = "//p[@class='msg ltype']/text()"
        job_require_xpath = "//div[@class='bmsg job_msg inbox']/p/text()"
        job_require_div_xpath = "//div[@class='bmsg job_msg inbox']/div/text()"

        # 因为51job页面有的职位信息xpath不相同，所以使用两个xpath来获取职位要求信息
        job_require = response.xpath(job_require_xpath).extract()
        job_require_div = response.xpath(job_require_div_xpath).extract()
        if job_require_div is not None:
            job_require = job_require_div + job_require
        content = ""
        for require in job_require:
            content += require
        content = ' '.join(content.split())

        job_info = A51JobItem()
        try:
            job_info['job_name'] = response.xpath(job_name_xpath).get().strip()
            job_info['job_money'] = response.xpath(job_money_xpath).get().strip()
            job_info['job_info'] = response.xpath(job_info_xpath).get().strip()
            job_info['job_require'] = content
        except Exception as e:
            print(e)
        yield job_info
