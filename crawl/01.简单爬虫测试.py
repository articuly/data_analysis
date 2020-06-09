# coding:utf-8

from urllib.request import urlopen

# 开始url
start_url = 'https://search.51job.com/list/030200,000000,0000,00,9,99,python,2,1.html?lang=c&stype=&postchannel=0000' \
            '&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1' \
            '&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='

# 抓取网页
webpage_file = urlopen(start_url)

# 抓取网页数据，为字节对象
data = webpage_file.read()

# 解码，将字节对象解码为字符串
data = data.decode('gbk')

# 从页面提取信息，提取详情页的链接
# .匹配换行符
import re

links = re.findall('<div class="el">.*?<a.*?href="(.*?)"[\w\W]*?>.*?</div>', data, flags=re.DOTALL)

print('done')
