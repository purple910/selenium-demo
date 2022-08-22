"""
    @Time           : 2022/8/17 12:03
    @Author         : fate
    @Description    : 对facebook的照片进行向下滚动获取下一页数据
    @File           : app4.py
"""

# 导入所需要包
import json

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
import time
import chromedriver_autoinstaller
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# Chromewebdriver路径
ca = DesiredCapabilities.CHROME
ca["goog:loggingPrefs"] = {"performance": "ALL"}

options = ChromeOptions()
# options.add_experimental_option('perfLoggingPrefs', {'enableNetwork': True})
options.add_argument('log-level=3')

driver_path = chromedriver_autoinstaller.install()

browser = webdriver.Chrome()
browser.maximize_window()

# url地址
url = 'https://www.facebook.com/POTUS/photos'

# 访问地址
browser.get(url)

# ***这里需要一个时间暂缓***(=>1即可)
time.sleep(2)

# 定义一个初始值 校验滚动条到底
temp_height = 0

while True:
    print(11111111111111111111111111111)
    # 执行js，滑动到最底部
    browser.execute_script("window.scrollTo(0,document.body.scrollHeight);")

    # 暂缓时间，点击下一页
    time.sleep(3)

    # 获取当前滚动条距离顶部的距离
    check_height = browser.execute_script(
        "return document.documentElement.scrollTop || window.pageYOffset || document.body.scrollTop;")

    # 判断是否还可以向下滚动？
    if check_height == temp_height:
        break
    temp_height = check_height
    print(check_height)

    print(22222222222222222222222)

# 最后退出
browser.quit()
