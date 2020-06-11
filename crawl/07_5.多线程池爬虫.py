# coding:utf-8

import time
import random
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
import requests
from lxml import html
from debug.my_logging import create_logger
import csv
from redis import StrictRedis

my_logger = create_logger(__name__)
csv_writer = csv.writer(open('my_jobs.csv', 'a', encoding='utf-8'))
redis = StrictRedis(host='127.0.0.1', port=63796)

# 抓取页面
start_url = 'https://search.51job.com/list/030200,000000,0000,00,9,99,python,2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='
# 待爬取links队列
# 1岗位搜索列表页面链接队列
list_links_queue = Queue()
list_links_queue.put(start_url)
# 2岗位详情列表页面链接队列
job_links_queue = Queue()
# 3待保存数据队列
job_info_queue = Queue()
# 每次开始抓取清空缓存
redis.delete('crawled_links')


# 获取页面对象
def get_page(url, headers):
    time.sleep(random.randint(1, 3))
    try:
        res = requests.get(url=url, headers=headers)
        page = res.content.decode('gbk')
    except Exception as e:
        my_logger.debug(e)
        return None
    else:
        # 已经爬取的链接加入到redis记录
        redis.sadd('crawed_links', url)
    try:
        dom = html.document_fromstring(page)
    except Exception as e:
        my_logger.debug(e)
        return None
    return dom


# 抓取列表提取链接，添加到队列，并过滤重复的链接
def extract_list_links():
    headers = {'Host': 'search.51job.com',
               'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36'}
    job_link_xpath = '//div[@id="resultList"]/div[@class="el"]/p/span/a/@href'
    next_xpath = '//li[@class="bk"]/a/@href'
    # 建立内部循环，当队列有数据时可执行任务
    while True:
        try:
            link = list_links_queue.get()
        except Exception as e:
            print(e)

        dom = get_page(link, headers)
        if dom is None:
            return False
        try:
            job_links = dom.xpath(job_link_xpath)
        except Exception as e:
            my_logger.debug(e)
        else:
            # 将岗位信息链接添加到工作链接队列
            for job_link in job_links:
                if not redis.sismember('crawed_links', job_link):
                    job_links_queue.put(job_link)
            print('job_links_len:', job_links_queue.qsize())

        try:
            # 将下一页添加队列
            bk_link = dom.xpath(next_xpath)
        except Exception as e:
            my_logger.debug(e)
        else:
            # 将结果添加到redis数据库
            if bk_link:
                next_link = bk_link[0] if link == start_url else bk_link[1]
                print('next_link:', next_link)
                if not redis.sismember('crawled_links', next_link):
                    list_links_queue.put(next_link)
                    print('list_links_len:', list_links_queue.qsize())


# 从页面提取有用信息
def extract_info():
    while True:
        try:
            refer = redis.srandmember('crawed_links', 1)[0].decode()
        except Exception as e:
            my_logger.debug(e)
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

        try:
            job_link = job_links_queue.get()
            print('job_link:', job_link)
        except Exception as e:
            print(e)
        else:
            dom = get_page(job_link, headers=headers)
        if dom is None:
            return False
        try:
            job_name = dom.xpath(job_name_xpath)[0]
            job_money = dom.xpath(job_money_xpath)[0]
            job_info = dom.xpath(job_info_xpath)[0].text_content()
            job_require = dom.xpath(job_require_xpath)[0].text_content()
        except Exception as e:
            my_logger.debug(e)
        else:
            print([job_name, job_money, job_info, job_require])
            job_info_queue.put([job_name, job_money, job_info, job_require])


# 保存职位信息
def save_info():
    while True:
        try:
            job_info = job_info_queue.get()
        except Exception as e:
            my_logger.debug(e)
        else:
            csv_writer.writerow(job_info)


# 最多20个线程，根据任务不同，分配不同的数量
pool = ThreadPoolExecutor(max_workers=20)

pool.submit(extract_list_links)

for i in range(10):
    pool.submit(extract_info)

for i in range(3):
    pool.submit(save_info)
