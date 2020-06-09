# coding:utf-8

import requests
import re

# html页面抓取
url = 'https://www.baidu.com'
page = requests.get(url)

# 获得响应头
headers = page.headers
# 获得cookies
cookies = page.cookies
cookies_dict = cookies.get_dict()
# 网页内容
page_text = page.text
print(page_text)

#########################################################
# 媒体文件抓取
url = 'https://n.sinaimg.cn/news/1_img/upload/953904eb/106/w1024h682/20200425/3dca-isuiksm8683599.jpg'
data = requests.get(url)
# 图片、视频都是二进制字节数据，以字节形式保存
with open('web_img.jpg', 'wb') as f:
    f.write(data.content)

# # cookie，使用post登陆
# # 需要发送username, password, csrf_token, cookie
# url = "http://test.python-xp.com/login"
# # 打开登陆页面
# login_page = requests.get(url)
# # 获得session
# session = login_page.cookies['session']
# token = re.findall('<input id=\"csrf_token\".*?value=\"(.*?)\">', login_page.text)[0]
# print(token)
# data = {'username': 'luxp', 'password': '123356', 'csrf_token': token}
# cookies = {}
# cookies = {'session': session}
# res = requests.post(url, data=data, cookies=cookies)

# 抓取json数据
url = "https://fe-api.zhaopin.com/c/i/city-page/user-city?ipCity=%E8%8B%8F%E5%B7%9E&ipProvince=%E6%B1%9F%E8%8B%8F&userDesiredCity=&_v=0.05823934&x-zp-page-request-id=1d939dd0a33045618a8a998494752c7a-1587889705134-637459&x-zp-client-id=4812e4fa-1955-4993-b664-2df9e54b98cb&MmEwMD=5mfeA2OpscznACKEWo1mn8HcuqVI7KgRD_CkL_g.CVoH8h8Zwiku6DLMuvIollwEUinBX_t8NYt78iP5tt1rQq0s8oJs1MWmDwuvCbgpYNEPpxN6C95h2YzEewd0nQ_Jl_TqoizZXtlOFBfaHRa8dpf9ic36jUX14qZ4WenQ31koRF8dZoMKzRkUr5T2h12yamFAghtLtBluoe0OzIpkPF4KlCrnoRrj3ObiUVVy5XHid3.C5Lc4qP3xZFi6RZPeyY26fcadMtGBWMQABmxAB69BKbpJa8P5P38K3KtdkI0Cooo3bUcDRbkdvMlrG9Mwuf6psYWCCwScdfcdFzmZ37Qf7Ef.BmejjCrELKbifbED5TtX9nHD65R0trCZe82478T_ohpI8UzX3QFU4iyvShnU9"
data = requests.get(url)
# 直接获得json数据
data = data.json()
print(data)

# 代理
proxy_servers = {
    'http': '127.0.0.1:49567',
    'https': '127.0.0.1:49567'
}

url = "http://www.google.com"
data = requests.get(url, proxies=proxy_servers)
