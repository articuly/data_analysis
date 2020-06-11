# -*- coding: utf-8 -*-

import time
import random
from threading import Thread, active_count
from queue import Queue
import requests
from lxml import html
from debug.my_logging import create_logger
import csv
from redis import StrictRedis

my_logger = create_logger(__name__)
csv_writer = csv.writer(open("my_job.csv", "a", encoding="utf-8"))
redis = StrictRedis(host="127.0.0.1")

# 页面抓取成功
start_url = "https://search.51job.com/list/000000,000000,0000,00,9,99,python,2,1.html" \
            "?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99" \
            "&ord_field=0&dibiaoid=0&line=&welfare="
# 待爬取links队列
# 岗位搜索列表页面链接队列
list_links_queue = Queue()
list_links_queue.put(start_url)
# 岗位详情列表页面链接队列
job_links_queue = Queue()
# 待保存数据队列
job_info_queue = Queue()

redis.delete("crawled_links")


def get_page(url, headers):
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
def extract_list_links():
    """
    从页面提取链接，并过滤重复的链接
    :param page:
    :return:
    """
    job_link_xpath = '//div[@id="resultList"]/div[@class="el"]/p/span/a/@href'
    next_path = "//li[@class='bk']/a/@href"
    headers = {'Host': 'search.51job.com',
               'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko)'
                             ' Chrome/81.0.4044.122 Safari/537.36'}

    while True:
        try:
            link = list_links_queue.get()
        except Exception as e:
            print(e)
            continue

        dom = get_page(link, headers)
        if dom is None:
            return False
        try:
            job_links = dom.xpath(job_link_xpath)
        except Exception as e:
            my_logger.exception(e)
        else:
            # 将岗位信息链接添加到队列
            for job_link in job_links:
                if not redis.sismember("crawled_links", job_link):
                    job_links_queue.put(job_link)
            print(job_links_queue.qsize())

        try:
            # 将下一页添加队列
            bk_link = dom.xpath(next_path)

        except Exception as e:
            my_logger.exception(e)
        else:
            # 将结果添加到redis数据库
            if bk_link:
                next_link = bk_link[0] if link == start_url else bk_link[1]
                print("next_link", next_link)
                if not redis.sismember("crawled_links", next_link):
                    list_links_queue.put(next_link)


def extract_info():
    """
    从页面中提取有用信息
    :return:
    """
    while True:
        try:
            refer = redis.srandmember("crawled_links", 1)[0].decode()
        except Exception as e:
            refer = start_url

        headers = {"Host": "jobs.51job.com",
                   "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 "
                                 "(KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36",
                   "Referer": refer
                   }
        job_name_xpath = "//h1/@title"
        job_money_xpath = "//div[@class='cn']/strong/text()"
        job_info_xpath = "//p[@class='msg ltype']"
        job_require_xpath = "//div[@class='bmsg job_msg inbox']"

        try:
            job_link = job_links_queue.get()
            print("job_link", job_link)
        except Exception as e:
            print(e)
        else:
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
            job_info_queue.put([job_name, job_money, job_info, job_require])


def save_info():
    """
    保存信息
    :return:
    """
    while True:
        try:
            job_info = job_info_queue.get()
        except Exception as e:
            my_logger.exception(e)
        else:
            csv_writer.writerow(job_info)


# 运行1个爬取链接的线程
t = Thread(target=extract_list_links)
t.start()

# 运行5个爬取信息的线程
for i in range(5):
    t = Thread(target=extract_info)
    t.start()

t = Thread(target=save_info)
t.start()
