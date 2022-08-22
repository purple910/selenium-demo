"""
    @Time           : 2022/8/17 12:03
    @Author         : fate
    @Description    : 获取响应体信息
    @File           : app4.py
"""

import json
from pprint import pprint

import chromedriver_autoinstaller
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options as ChromeOptions

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
driver = webdriver.Chrome(options=options, executable_path=driver_path, desired_capabilities=caps)

driver.get('https://httpbin.org/get')
logs = driver.get_log("performance")
for item in logs:
    log = json.loads(item["message"])["message"]
    # if "Network.response" in log["method"] or "Network.request" in log["method"] or "Network.webSocket" in log["method"]:
    # pprint(log)
    if log["method"] == 'Network.responseReceived':
        url = log['params']['response']['url']
        if url == 'data:,':  # 过滤掉初始data页面，后续可以根据 log['params']['response']['type']过滤请求类型
            continue
        print('请求', url)
        request_id = log['params']['requestId']

        # request_headers = log['params']['response']['requestHeaders']
        response_headers = log['params']['response']['headers']
        response_time = log['params']['response']['responseTime']
        status_code = log['params']['response']['status']

        try:
            request_data = driver.execute_cdp_cmd('Network.getRequestPostData', {'requestId': request_id})
        except WebDriverException:  # 没有后台数据获取时会有异常
            request_data = None

        response_body = driver.execute_cdp_cmd('Network.getResponseBody', {'requestId': request_id})['body']
        print('响应', response_body)

driver.close()