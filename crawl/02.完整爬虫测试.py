# coding:utf-8

import urllib.request as request
import re
from debug.my_logging import create_logger
import csv

my_logger = create_logger(__name__)
csv_writer = csv.writer(open('job_name.csv', 'a', encoding='utf-8'))

# 页面抓取开始
start_url = 'https://search.51job.com/list/030200,000000,0000,00,9,99,python,2,1.html?lang=c&stype=&postchannel=0000' \
            '&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1' \
            '&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='

# 待抓取links
all_links = set()
# 在待爬取里links中添加起始url
all_links.add(start_url)
# 已爬取links,已经爬取过的link添加到已爬取，防止重复爬取
crawled_links = set()


# 抓取url远程页面
def getPage(url):
    global crawled_links
    try:
        page = request.urlopen(url).read().decode('gbk')
    except Exception as e:
        my_logger.error(e)
    crawled_links.add(url)
    return page


# 从页面提取链接，并过滤重复的链接
def extractLinks(page):
    global all_links
    links_reg = '<div class="el">.*?<a.*?href="(.*?)".*?>.*?</div>'
    try:
        links = re.findall(links_reg, page, flags=re.DOTALL)
    except Exception as e:
        my_logger.error(e)
    else:
        links = set(links) - crawled_links
        all_links = all_links.union(links)
    return all_links


# 从页面中提取有用信息
def extractInfo(page):
    job_name_reg = '<div\s*?class=\"el\">.*?<a.*?title=\"(.*?)\".*?>.*?</a>'
    try:
        job_names = re.findall(job_name_reg, page, flags=re.DOTALL)
    except Exception as e:
        my_logger.error(e)
    if job_names:
        saveInfo(job_names)


# 保存页面
def saveInfo(info_list):
    for info in info_list:
        try:
            csv_writer.writerow([info])
        except Exception as e:
            my_logger.error(e)


# 运行一个主循环
DEBUG = True

while True:
    try:
        link = all_links.pop()
        my_logger.log(10, '%(link)s', {"link": link})
    except Exception as e:
        my_logger.error(e)
        continue
    else:
        page = getPage(link)
        if page:
            extractLinks(page)
            extractInfo(page)

    if DEBUG:
        break
