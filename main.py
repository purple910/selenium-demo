"""
    @Time           : 2022/8/17 12:03
    @Author         : fate
    @Description    : 对facebook的用户的照片进行爬取并保存到本地
    @File           : app4.py
"""
# 导入所需要包
import json

import requests
from selenium import webdriver
from selenium.common import WebDriverException
from selenium.webdriver.chrome.options import Options as ChromeOptions
import time
import chromedriver_autoinstaller
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

caps = {
    'browserName': 'chrome',
    'version': '',
    'platform': 'ANY',
    'goog:loggingPrefs': {'performance': 'ALL'},
    'goog:chromeOptions': {'extensions': [], 'args': ['--headless']}
}
# Chromewebdriver路径
options = ChromeOptions()
driver_path = chromedriver_autoinstaller.install()
options.add_argument('log-level=3')
browser = webdriver.Chrome(options=options, executable_path=driver_path, desired_capabilities=caps)

# url地址
url = 'https://www.facebook.com/POTUS/photos'
# https://www.facebook.com/FLOTUS/photos
# https://www.facebook.com/barackobama/photos
# https://www.facebook.com/georgewbush/photos
# https://www.facebook.com/presidentjimmycarter/photos
# https://www.facebook.com/billclinton/photos
# https://www.facebook.com/NaftaliBennett/photos
# https://www.facebook.com/mikepompeo/photos
#

ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0"
proxies = {
    "http": "http://192.168.7.96:7890",
    "https": "http://192.168.7.96:7890",
}
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

    # 重要：获取浏览器请求的信息，包括了每一个请求的请求方法/请求头，requestId等信息
    logs = browser.get_log("performance")
    for item in logs:
        log = json.loads(item["message"])["message"]
        # if "Network.response" in log["method"] or "Network.request" in log["method"] or "Network.webSocket" in log["method"]:
        # pprint(log)
        if log["method"] == 'Network.responseReceived':
            url = log['params']['response']['url']
            if url == 'data:,':  # 过滤掉初始data页面，后续可以根据 log['params']['response']['type']过滤请求类型
                continue

            if url != 'https://www.facebook.com/api/graphql/':
                continue
            print('请求', url)
            request_id = log['params']['requestId']

            # request_headers = log['params']['response']['requestHeaders']
            # response_headers = log['params']['response']['headers']
            # response_time = log['params']['response']['responseTime']
            # status_code = log['params']['response']['status']

            try:
                request_data = browser.execute_cdp_cmd('Network.getRequestPostData', {'requestId': request_id})
            except WebDriverException:  # 没有后台数据获取时会有异常
                request_data = None

            response_body = browser.execute_cdp_cmd('Network.getResponseBody', {'requestId': request_id})['body']
            data = json.loads(response_body)
            for temp in data['extensions']['prefetch_uris_v2']:
                print('响应', temp['uri'])
                if not temp['uri']:
                    continue
                with requests.get(temp['uri'], headers={'User-Agent': ua}, proxies=proxies) as resp:
                    # print(resp.status_code)
                    resp.raise_for_status()
                    # resp.encoding = res.apparent_encoding
                    # 将图片内容写入
                    with open('E://facebook//{}.jpg'.format(time.time()), 'wb') as f:
                        f.write(resp.content)
                        f.close()

    print(22222222222222222222222)

# 最后退出
browser.close()
browser.quit()
