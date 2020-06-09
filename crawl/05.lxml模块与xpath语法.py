# coding:utf-8

import requests
from lxml import html

# 页面抓取成功
url = "https://search.51job.com/list/070300,000000,0000,00,9,99,python,2,1.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare="

headers = {
    "Host": "search.51job.com",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36"
}

try:
    data = requests.get(url, headers=headers)
except Exception as e:
    print(e)
else:
    # page1 = data.content.decode(data.apparent_encoding)
    page = data.content.decode('gbk')

# 岗位链接提取
xhref = '//div[@class="el"]/p/span/a/@href'
xlink_text = '//div[@class="el"]/p/span/a/text()'
dom = html.document_fromstring(page)
links = dom.xpath(xhref)
texts = dom.xpath(xlink_text)

# 抓取详细页面
res = requests.get(links[0], headers=headers)
job_page_content = res.content
job_page = job_page_content.decode('gbk')

# 根据xpath提取岗位信息
xpath = "//p[@class=\"msg ltype\"]/@title"
dom = html.document_fromstring(job_page)
info = dom.xpath(xpath)[0]

print('done')

# lxml 还支持其他的元素选择方式
# ele为dom或者匹配的元素
# ele.text - dom转换为字符串,不包含子元素
# ele.text_content - dom的所有元素text（不包含子元素tag名）转换为string
# ele.items - 属性列表
# ele.find_class - 根据样式名查找元素
# ele.get_element_by_id - 根据id查找元素
# ele.getchildren - 查找子元素1
