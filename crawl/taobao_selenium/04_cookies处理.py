# coding:utf-8
# author: Articuly
# datetime: 2020/6/12 17:24
# software: PyCharm

import time, random
import pickle
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import Options, WebDriver

# 创建实例
options = Options()
options.add_experimental_option('excludeSwitches', ['enable-automation'])
browser = WebDriver(r'D:\Browser\Chromium\chromedriver.exe', options=options)

# 打开网页
browser.get('https://www.taobao.com')
# 将浏览器最大化显示
browser.maximize_window()
# 隐性等待页面加载完成，如果一个元素获取不到，会等待30s
browser.implicitly_wait(30)


class TaobaoSpider:
    def __init__(self, driver):
        self.driver = driver

    def search_action(self):
        input_ = input('please enter keyword:')
        # 登陆之前的cookies
        print('*' * 100)
        print(self.driver.get_cookies())
        print(len(self.driver.get_cookies()))
        print('*' * 100)
        try:
            q = self.driver.find_element_by_id('q')
        except Exception as e:
            print(e)
        else:
            q.send_keys(input_)

        try:
            search_btn = self.driver.find_element_by_class_name('btn-search')
        except Exception as e:
            print(e)
        else:
            search_btn.click()

    def login(self):
        try:
            login_btn = self.driver.find_element_by_class_name('icon-qrcode')
        except Exception as e:
            print(e)
        else:
            login_btn.click()
        # 页面登陆跳转需要时间，不能在点击之后立即记录cookie
        # 这里记录的未必是登陆之后的cookie
        print("-" * 100)
        print(browser.get_cookies())
        print(len(browser.get_cookies()))
        print("-" * 100)

    def click_next(self):
        """
        点击下一页
        """
        try:
            next = self.driver.find_element_by_css_selector('.next>a')
        except Exception as e:
            print(e)
        else:
            next.click()

    def get_info(self):
        """
        提取商品信息
        """
        try:
            goods_area = self.driver.find_element_by_id('mainsrp-itemlist')
        except Exception as e:
            print(e)
        else:
            title_eles = goods_area.find_elements_by_xpath(
                "//div[@class='row row-2 title']/a")
            price_eles = goods_area.find_elements_by_xpath(
                "//div[@class='row row-1 g-clearfix']/div/strong")
            seller_eles = goods_area.find_elements_by_xpath(
                "//div[@class='row row-3 g-clearfix']/div/a/span[2]")
            bougnt_eles = goods_area.find_elements_by_xpath(
                "//div[@class='row row-1 g-clearfix']/div[2]")
            location_eles = goods_area.find_elements_by_xpath(
                "//div[@class='row row-3 g-clearfix']/div[2]")

        for i, title_ele in enumerate(title_eles):
            print(
                title_ele.text.strip(),
                price_eles[i].text,
                seller_eles[i].text,
                bougnt_eles[i].text,
                location_eles[i].text,
            )

        cookies = self.driver.get_cookies()
        print('*' * 100)
        print(cookies)
        print(len(cookies))
        print('*' * 100)
        with open('cookie.txt', 'wb') as f:
            pickle.dump(cookies, f)

    def run_spider(self):
        self.search_action()
        if self.driver.current_url.find('login') != -1:
            self.login()
        self.get_info()


taobao_spider = TaobaoSpider(browser)
taobao_spider.run_spider()

# ###############################
# cookie使用方法
# 1：get_cookies() ,获取cookie信息
# 2：get_cookie(name),即获取key的信息
# 3：add_cookie(cookie_dict),添加cookie信息,cook_dict 指的是name 和 Value
# 4：delete_cookie(name):根据cookie name删除cookie
# 5：delete_all_cookies():删除cookie信息
