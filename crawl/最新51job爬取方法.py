#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
网易微专业 - python高级工程师特训班
"""

import requests
import json


url = "https://search.51job.com/list/030200,000000,0000,00,9,99,python,2,2.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare="
cookie = 'guid=a07ece7b2525a88b80265c4041ebc65c; nsearch=jobarea%3D%26%7C%26ord_field%3D%26%7C%26recentSearch0%3D%26%7C%26recentSearch1%3D%26%7C%26recentSearch2%3D%26%7C%26recentSearch3%3D%26%7C%26recentSearch4%3D%26%7C%26collapse_expansion%3D; search=jobarea%7E%60030200%7C%21ord_field%7E%600%7C%21'
headers = {'Host': 'search.51job.com',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
           'Accept': 'application/json, text/javascript, */*; q=0.01',
           'Referer': 'https://search.51job.com/list/030200,000000,0000,00,9,99,python,2,3.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare=',
           'Cookie': cookie,
           'X-Requested-With': 'XMLHttpRequest'}

try:
    req = requests.get(url, timeout=5, headers=headers)
    data = req.content.decode('gbk')
    print('success')
except requests.exceptions.RequestException as e:
    print(e)

jobs = json.loads(data)
