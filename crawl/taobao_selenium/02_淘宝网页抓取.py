# coding:utf-8

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.webdriver import Options
import time

options = Options()
options.add_experimental_option('excludeSwitches', ['enable-automation'])

browser = webdriver.chrome.webdriver.WebDriver(r'D:\Browser\Chromium\chromedriver.exe', options=options)

# 打开网页
browser.get('https://www.taobao.com')
print(browser.current_url)

# 完成用户登陆
login_link = browser.find_element_by_css_selector('.site-nav-sign>a')
login_link.click()
# 直充用户名
user_input = browser.find_element_by_id('fm-login-id')
password_input = browser.find_element_by_id('fm-login-password')
user_input.send_keys('username')
password_input.send_keys('123456')
# 滑块拖动
block_area = browser.find_element_by_id('nocaptcha-password')
# 查看滑块位置，窗口变动会影响X，Y
print(block_area.location)
# 查看滑块区域，滑块移动范围
print(block_area.rect)
# 滑块
try:
    block_btn = browser.find_element_by_id('nc_1_n1z')
except Exception as e:
    block_btn = browser.find_element_by_id('nc_2_n1z')
print(block_btn)
# 拖动滑块
action = ActionChains(browser)
action.drag_and_drop_by_offset(block_btn, 300, 0).perform()
# 点击登陆
login_btn = browser.find_element_by_css_selector(".fm-btn>button")
login_btn.click()

# while True:
#     try:
#         time.sleep(3)
#         login_btn = browser.find_element_by_class_name("icon-qrcode")
#     except Exception as e:
#         continue
#     else:
#         login_btn.click()
#         break

# 等待网页准备好，再搜索
while True:
    try:
        time.sleep(3)
        q = browser.find_element_by_id('q')
    except Exception as e:
        continue
    else:
        q.send_keys('树莓派')
        break

while True:
    try:
        time.sleep(3)
        search_btn = browser.find_element_by_class_name('btn-search')
    except Exception as e:
        continue
    else:
        search_btn.click()
        break

# 点击链接跳到新的窗口
while True:
    try:
        time.sleep(3)
        hot = browser.find_element_by_link_text('更多热卖')
    except Exception as e:
        continue
    else:
        hot.click()
        break

# 出现了多个页面标签
windows = browser.window_handles
browser.switch_to.window(windows[1])
while True:
    try:
        time.sleep(3)
        next = browser.find_element_by_partial_link_text('下一页')
    except Exception as e:
        continue
    else:
        next.click()
        break

while True:
    try:
        time.sleep(3)
        goods_area = browser.find_element_by_id("searchResult")
    except Exception as e:
        continue
    else:
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
        break

for i, title_ele in enumerate(title_eles):
    print(
        title_ele.text,
        price_eles[i].text,
        seller_eles[i].text,
        bougnt_eles[i].text,
        dsr_truth_eles[i].text,
        dsr_service_eles[i].get_attribute('innerHTML'),
        dsr_speed_eles[i].get_attribute('innerHTML')
    )

while True:
    try:
        time.sleep(3)
        next = browser.find_element_by_partial_link_text("下一页")
    except Exception as e:
        continue
    else:
        next.click()
        break
