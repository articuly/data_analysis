# coding:utf-8
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import Options

# options 文档 https://sites.google.com/a/chromium.org/chromedriver/capabilities
options = Options()
# 添加代理
# proxy = '--proxy-server=127.0.0.1:49567'
# options.add_argument(proxy)

# 隐藏显示正收到自动测试软件控制
options.add_experimental_option('excludeSwitches', ['enable-automation'])

# 创建浏览器实例
# browser=webdriver.Firefox(r'D:\Browser\Firefox\geckodriver.exe')
browser = webdriver.chrome.webdriver.WebDriver(r'D:\Browser\Chromium\chromedriver.exe', options=options)
# browser = webdriver.chrome.webdriver.WebDriver(r'D:\Browser\Chrome\chromedriver.exe', options=options)

browser.get('http://www.baidu.com')
search_box = browser.find_element_by_id('kw')
search_box.send_keys('python')
submit_button = browser.find_element_by_id('su')
submit_button.click()

# 运行JS脚本
browser.execute_script('alert("I can control the browser")')

# 交互动作
# from selenium.webdriver import ActionChains
# action = ActionChains(browser)
