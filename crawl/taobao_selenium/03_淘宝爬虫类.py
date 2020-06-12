# coding:utf-8
# author: Articuly
# datetime: 2020/6/12 15:08
# software: PyCharm

import time, random
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import Options, WebDriver
from selenium.webdriver import ActionChains

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
        """
        初始化驱动
        """
        self.driver = driver
        self.action = ActionChains(self.driver)
        self.count = 10

    def search_action(self):
        """
        等待搜索关键字输入，并填充关键字进行搜索
        """
        input_ = input('请输入抓取关键字：')
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

    def login_qr(self):
        """
        二维码登陆页面
        """
        try:
            login_btn = self.driver.find_element_by_class_name('icon-qrcode')
        except Exception as e:
            print(e)
        else:
            login_btn.click()

    def login(self):
        """
        登陆页面
        """
        try:
            user_input = self.driver.find_element_by_id('nocaptcha-password')
        except Exception as e:
            print('can not access the area', e)
        else:
            try:
                block_btn = self.driver.find_element_by_id('nc_1_n1z')
            except Exception as e:
                block_btn = self.driver.find_element_by_id('nc_2_n1z')
            else:
                # 滑块初始化需要一定的时间，与页面加载等待不同
                time.sleep(3)
                try:
                    self.action.drag_and_drop_by_offset(block_btn, 300, 0).perform()
                except Exception as e:
                    print('can not drag and drop, please retry', e)

            try:
                print('get login btn')
                login_btn = self.driver.find_element_by_css_selector('.fm-btm>button')
            except Exception as e:
                print('can not get login btn', e)
            else:
                login_btn.click()
                print('login complete')
                return True

    def click_next(self):
        """
        点击下一页
        """
        if self.count > 0:
            try:
                next = self.driver.find_element_by_css_selector('.next>a')
            except Exception as e:
                print(e)
            else:
                self.count -= 1
                next.click()
            self.get_info()

    def get_info(self):
        """
        提取商品信息
        """
        # 检查商品区域是否加载完毕，默认隐性等待时间是30s，这里wait_until方法可以延迟到60s
        self.wait_until(60, 0.5, self.check_goods_area)
        goods_area = self.driver.find_element_by_id('mainsrp-itemlist')
        title_eles = goods_area.find_elements_by_xpath(
            "//div[@class='item']/a/div[@class='info']/span[@class='title']")
        price_eles = goods_area.find_elements_by_xpath(
            "//div[@class='item']/a/div[@class='info']/p[@class='price']/span/strong")
        seller_eles = goods_area.find_elements_by_xpath(
            "//div[@class='item']/a/div[@class='info']/p/span[@class='shopNick']")
        bougnt_eles = goods_area.find_elements_by_xpath(
            "//div[@class='item']/a/div[@class='info']/p/span[@class='payNum']")
        dsr_truth_eles = goods_area.find_elements_by_xpath(
            "//div[@class='item']/a/div[@class='info']/div[@class='moreInfo']/div/span/span[@class='dsr-info-num']")
        dsr_service_eles = goods_area.find_elements_by_xpath(
            "//div[@class='item']/a/div[@class='info']/div[@class='moreInfo']/div/ul/li[2]/span/b")
        dsr_speed_eles = goods_area.find_elements_by_xpath(
            "//div[@class='item']/a/div[@class='info']/div[@class='moreInfo']/div/ul/li[3]/span/b")

        for i, title_ele in enumerate(title_eles):
            try:
                print(
                    title_ele.text,
                    price_eles[i].text,
                    seller_eles[i].text,
                    bougnt_eles[i].text,
                    dsr_truth_eles[i].text,
                    dsr_service_eles[i].get_attribute('innerHTML'),
                    dsr_speed_eles[i].get_attribute('innerHTML')
                )
            except Exception as e:
                print(e)
        self.click_next()

    def check_goods_area(self):
        """
        检测商品区域是否已经可以抓取
        """
        try:
            goods_area = self.driver.find_element_by_id('mainsrp-itemlist')
        except Exception as e:
            print('wait...', e)
            return False
        else:
            return True

    def wait_until(self, timeout, pool_time, method):
        """
        检测目标，直到目标出现或者超时
        """
        start_time = time.time()
        while True:
            time.sleep(pool_time)
            current_time = time.time()
            if current_time - start_time > timeout:
                raise TimeoutError('timeout error')
            if method():
                break

    def runspider(self):
        self.search_action()
        # 未登陆状态下搜索会跳转到登陆页面
        if self.driver.current_url.find("login") != -1:
            self.login()
        self.get_info()


taobao_spider = TaobaoSpider(browser)
taobao_spider.runspider()
