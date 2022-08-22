"""
    @Time           : 2022/8/19 10:55
    @Author         : fate
    @Description    : https://www.senate.gov/states/DE/intro.htm
    @File           : main5.py
"""
import time

import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
# 从个人网站中获取Twitter、Facebook地址
# $x('//a[contains(@href,"https://twitter.com")]')
from selenium.webdriver.common.by import By


def init():
    # 设置浏览器
    options = ChromeOptions()
    options.add_argument('log-level=3')
    prefs = {
        'profile.default_content_setting_values':
            {'notifications': 2}  # 禁止谷歌浏览器弹出通知消息
    }
    options.add_experimental_option('prefs', prefs)

    driver_path = chromedriver_autoinstaller.install()
    browser = webdriver.Chrome(options=options, executable_path=driver_path)
    browser.maximize_window()  # 浏览器窗口最大化
    browser.implicitly_wait(10)  # 隐形等待10秒

    return browser


def get_urls(browser):
    browser.get("https://www.senate.gov/states/DE/intro.htm")
    time.sleep(2)

    rootUrl = "https://www.senate.gov"
    urlList = []

    statesSelection = browser.find_element(by=By.ID, value="statesSelection")
    options = statesSelection.find_elements(by=By.TAG_NAME, value="option")
    for option in options:
        # print(option.text)
        val = option.get_attribute("value")
        if val is not None and val != "":
            urlList.append(rootUrl + val)

    hrefList = []
    for url in urlList:
        browser.get(url)
        time.sleep(1)

        introduction = browser.find_elements(by=By.XPATH, value="//div[@class='state-row']")[0]
        peoples = introduction.find_elements(by=By.CLASS_NAME, value="state-column")
        for people in peoples:
            href = people.find_element(by=By.XPATH, value="./a/img/..").get_attribute("href")
            # print(href)
            hrefList.append(href)

    return hrefList


if __name__ == '__main__':
    with init() as browser:

        urlList = get_urls(browser)
        print(len(urlList))

        userList = []
        for url in urlList:
            browser.get(url)
            time.sleep(2)

            user = {}
            user['url'] = url
            twitter = browser.find_elements(by=By.XPATH, value="//a[contains(@href,'https://twitter.com/')]")
            if twitter is not None and len(twitter) > 0:
                user['twitter'] = twitter[0].get_attribute("href")

            facebook = browser.find_elements(by=By.XPATH, value="//a[contains(@href,'https://www.facebook.com/')]")
            if facebook is not None and len(facebook) > 0:
                user['facebook'] = facebook[0].get_attribute("href")

            userList.append(user)

        print(userList)
