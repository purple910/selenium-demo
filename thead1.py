"""
    @Time           : 2022/8/22 14:27
    @Author         : fate
    @Description    : 多线程示例
    @File           : thead1.py
"""

import time

import chromedriver_autoinstaller


def sayhello(str):
    print(str)
    time.sleep(2)


name_list = ['xiaozi', 'aa', 'bb', 'cc']
start_time = time.time()
for i in range(len(name_list)):
    sayhello(name_list[i])
print('%d second' % (time.time() - start_time))

print("------------------------------")

import threadpool


def sayhello(str):
    print("Hello ", str)
    time.sleep(2)


name_list = ['xiaozi', 'aa', 'bb', 'cc']
start_time = time.time()
pool = threadpool.ThreadPool(10)
requests = threadpool.makeRequests(sayhello, name_list)
[pool.putRequest(req) for req in requests]
pool.wait()
print('%d second' % (time.time() - start_time))

print("================================================")
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions

def open(ip, url):
    options = ChromeOptions()
    options.add_argument('log-level=3')
    prefs = {
        'profile.default_content_setting_values':
            {'notifications': 2}  # 禁止谷歌浏览器弹出通知消息
    }

    # 添加debuggerAddress这个属性 可以操控我手动打开的浏览器（不过要事先开启用doc命令开启浏览器的远程调试而且端口与这个一样）
    options.add_experimental_option('debuggerAddress', ip)
    # options.add_experimental_option('prefs', prefs)

    driver_path = chromedriver_autoinstaller.install()
    browser = webdriver.Chrome(options=options, executable_path=driver_path)
    browser.maximize_window()  # 浏览器窗口最大化
    browser.implicitly_wait(10)  # 隐形等待10秒
    browser.get(url)


if __name__ == '__main__':
    # chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\selenum\AutomationProfile2"
    # chrome.exe --remote-debugging-port=9223 --user-data-dir="C:\selenum\AutomationProfile1"
    # chrome.exe --remote-debugging-port=9224 --user-data-dir="C:\selenum\AutomationProfile"
    for i in ['127.0.0.1:9223', '127.0.0.1:9224']:
        open(i, "https://www.senate.gov/states/DE/intro.htm")
