# -*- coding: utf-8 -*-

import time
import random
import requests
from lxml import html
from debug.my_logging import create_logger
import csv
from redis import StrictRedis
from threading import current_thread

my_logger = create_logger(__name__)

redis = StrictRedis(host="127.0.0.1", port=63796)

# start_url
start_url = "https://search.51job.com/list/000000,000000,0000,00,9,99,python,2,1.html" \
            "?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99" \
            "&ord_field=0&dibiaoid=0&line=&welfare="

# 已爬取url记录，防止反复爬取已爬取过的页面
# 测试的时候需要删除已爬取记录，防止爬虫无法启动
redis.delete("crawled_links")


def get_page(url, headers):
    print("get_Page", current_thread().getName())
    time.sleep(random.randint(1, 3))
    try:
        res = requests.get(url=url, headers=headers)
        page = res.content.decode("gbk")
    except Exception as e:
        my_logger.exception(e)
        return None
    else:
        # 已经爬取的链接加入到redis记录
        redis.sadd("crawled_links", url)
    try:
        dom = html.document_fromstring(page)
    except Exception as e:
        my_logger.exception(e)
        return None
    return dom


# 抓取列表提取链接，添加到队列
def extract_list_links(link):
    """
    从页面提取链接，并过滤重复的链接
    :param link:
    :return:
    """
    print("extractListLinks", current_thread().getName())
    job_link_xpath = '//div[@id="resultList"]/div[@class="el"]/p/span/a/@href'
    next_path = "//li[@class='bk']/a/@href"
    headers = {'Host': 'search.51job.com',
               'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/81.0.4044.122 Safari/537.36'}

    dom = get_page(link, headers)
    if dom is None:
        return False

    # 提取岗位链接
    try:
        job_links = dom.xpath(job_link_xpath)
    except Exception as e:
        my_logger.exception(e)
    else:
        # 爬取所有岗位信息
        for job_link in job_links:
            if not redis.sismember("crawled_links", job_link):
                # 调用岗位信息爬取函数
                extract_info(job_link)

    try:
        # 提取下一页
        bk_link = dom.xpath(next_path)
    except Exception as e:
        my_logger.exception(e)
    else:
        if bk_link:
            next_link = bk_link[0] if link == start_url else bk_link[1]
            print("next_link", next_link)
            if not redis.sismember("crawled_links", next_link):
                return next_link
            else:
                return None


def extract_info(job_link):
    """
    从页面中提取有用信息
    :param job_link:
    :return:
    """
    print("extract_info", current_thread().getName())
    try:
        # 随机提供一个refer url，防止被51job服务器禁止访问
        refer = redis.srandmember("crawled_links", 1)[0].decode()
    except Exception as e:
        print(e)
        refer = start_url

    headers = {"Host": "jobs.51job.com",
               "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) "
                             "Chrome/81.0.4044.122 Safari/537.36",
               "Referer": refer
               }

    job_name_xpath = "//h1/@title"
    job_money_xpath = "//div[@class='cn']/strong/text()"
    job_info_xpath = "//p[@class='msg ltype']"
    job_require_xpath = "//div[@class='bmsg job_msg inbox']"

    dom = get_page(job_link, headers)
    if dom is None:
        return False
    try:
        job_name = dom.xpath(job_name_xpath)[0]
        job_money = dom.xpath(job_money_xpath)[0]
        job_info = dom.xpath(job_info_xpath)[0].text_content()
        job_require = dom.xpath(job_require_xpath)[0].text_content()
    except Exception as e:
        my_logger.exception(e)
    else:
        save_info([job_name, job_money, job_info, job_require])


def save_info(job_info):
    """
    保存信息
    :param job_info:
    :return:
    """
    print("save_info", current_thread().getName())
    try:
        csv_writer = csv.writer(open("my_job.csv", "a", encoding="utf-8"))
        csv_writer.writerow(job_info)
    except Exception as e:
        my_logger.exception(e)


url = start_url
while True:
    next_link = extract_list_links(url)
    if next_link is None:
        break
    else:
        url = next_link
