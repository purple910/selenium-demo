"""
    @Time           : 2022/8/17 12:03
    @Author         : fate
    @Description    : 对facebook的照片进行向下滚动获取下一页数据，并获取请求信息
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
browser = webdriver.Chrome(options=options, executable_path=driver_path, desired_capabilities=ca)

# url地址
url = 'https://www.facebook.com/POTUS/photos'

# 访问地址
browser.get(url)

# ***这里需要一个时间暂缓***(=>1即可)
time.sleep(2)

# 定义一个初始值 校验滚动条到底
temp_height = 0

request_list = []  # 所有的请求
response_list = []  # 所有的返回
cache_list = []  # 所有的缓存读取记录

while True:
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

    log = browser.get_log("performance")

    for responseReceived in log:
        # print(responseReceived)
        # //*[@id="mount_0_0_PC"]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div/div/div/div/div/div[3]/div[1]/div[2]/div/div/a/img

        message = json.loads(responseReceived['message'])['message']

        # 获取所有请求信息(请求信息集中在requestWillBeSent)
        if message['method'] == 'Network.requestWillBeSent':
            # request_id = message['params']['requestId']
            # request = message['params']['request']
            # try:
            #
            #     # 尝试获取请求body，type为浏览器开发者模式network下类型筛选（用于区分接口请求和页面请求）
            #     request_list.append({'id': request_id, 'type': message['params']['type'],
            #                          'url': request['url'], 'method': request['method'],
            #                          'req_time': responseReceived['timestamp'], 'req_headers': request['headers'],
            #                          'req_body': json.loads(request['postData'])})
            # except:
            #     request_list.append({'id': request_id, 'type': message['params']['type'],
            #                          'url': request['url'], 'method': request['method'],
            #                          'req_time': responseReceived['timestamp'], 'req_headers': request['headers']})
            pass
        # 获取所有返回信息(返回信息集中在responseReceived，但是其中无body信息)
        elif message['method'] == 'Network.responseReceived':
            request_id = message['params']['requestId']
            response = message['params']['response']
            try:  # responseReceived日志中无response body信息，需要额外进行获取
                resp_body = json.loads(
                    browser.execute_cdp_cmd('Network.getResponseBody', {'requestId': request_id})['body'])
            except:
                resp_body = None

            # print(response['url'])
            if response['url'] != 'https://www.facebook.com/api/graphql/':
                continue
            print("---------------------------")
            print(resp_body)
            print("+++++++++++++++++++++++++++")
            try:
                # 能获取到requestHeaders尽量使用，因为此处比较全
                response_list.append({'id': request_id, 'type': message['params']['type'], 'url': response['url'],
                                      'resp_time': responseReceived['timestamp'],
                                      'req_headers': response['requestHeaders'], 'resp_status': response['status'],
                                      'resp_headers': response['headers'], 'resp_body': resp_body})
            except:
                response_list.append({'id': request_id, 'type': message['params']['type'], 'url': response['url'],
                                      'resp_time': responseReceived['timestamp'], 'resp_status': response['status'],
                                      'resp_headers': response['headers'], 'resp_body': resp_body})
        # 获取是否为缓存请求(从浏览器缓存直接获取，一般为css、js文件请求)
        elif message['method'] == 'Network.requestServedFromCache':
            request_id = message['params']['requestId']
            cache_list.append({'id': request_id})

    print(22222222222222222222222)

# 最后退出
browser.quit()

# 请求信息
# print(request_list)
print(response_list)
