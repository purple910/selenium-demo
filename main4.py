"""
    @Time           : 2022/8/18 16:49
    @Author         : fate
    @Description    : 获取美国内阁- 维基百科
    @File           : main4.py
"""
import json

import requests
from selenium import webdriver
from selenium.common import WebDriverException
from selenium.webdriver.chrome.options import Options as ChromeOptions
import time
import chromedriver_autoinstaller
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

caps = {
    'browserName': 'chrome',
    'version': '',
    'platform': 'ANY',
    'goog:loggingPrefs': {'performance': 'ALL'},
    'goog:chromeOptions': {'extensions': [], 'args': ['--headless']}
}

options = ChromeOptions()
driver_path = chromedriver_autoinstaller.install()
options.add_argument('log-level=3')
browser = webdriver.Chrome(options=options, executable_path=driver_path, desired_capabilities=caps)
browser.maximize_window()  # 浏览器窗口最大化
browser.implicitly_wait(10)  # 隐形等待10秒

# 美国内阁- 维基百科，自由的百科全书
browser.get("https://zh.m.wikipedia.org/zh-cn/%E7%BE%8E%E5%9B%BD%E5%86%85%E9%98%81")
time.sleep(2)

trs = browser.find_elements(by=By.XPATH, value="//*[@id='content-collapsible-block-0']/table/tbody/tr")

for tr in trs:
    position = tr.find_element(by=By.XPATH, value="./td[1]/*[3]").text
    name = tr.find_element(by=By.XPATH, value="./td[2]").text
    ptime = tr.find_element(by=By.XPATH, value="./td[3]").text
    print(position + "--" + name + "--" + ptime)
    print("=========================================")

browser.quit()
