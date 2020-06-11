# -*- coding=utf-8 -*-

import requests

url = "https://p.3.cn/prices/mgets?type=1&skuIds=J_8748165,J_100008793532,J_100005578792," \
      "J_100009149836,J_100005855324,J_100004061926&callback=show&_=1587889274792"

headers = {'Host': 'p.3.cn', 'Referer': 'https://caidian.jd.com/'}

res = requests.get(url, headers=headers)


# 提取json部分
# 去掉函数名后就是json部分，将js中的true,false,null转为 True, False, None，得到json字典
def get_dicts(string, func_name):
    true = True
    false = False
    null = None
    return eval(string[len(func_name) + 1:-3])


dicts = get_dicts(res.text, "show")
print(dicts)
