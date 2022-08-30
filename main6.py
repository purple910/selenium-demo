"""
    @Time           : 2022/8/19 10:55
    @Author         : fate
    @Description    : 获取英国官员的信息
    英国：
    https://www.gov.uk/government/how-government-works
    https://www.gov.uk/government/ministers

    加拿大:
    https://www.canada.ca/en/government/ministers.html

    新西兰：
    https://www.parliament.nz/en/mps-and-electorates/members-of-parliament/

    德国：
    https://www.bundesregierung.de/breg-en/federal-cabinet

    法国：
    https://www.gouvernement.fr/composition-du-gouvernement

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
    browser.get("https://www.gov.uk/government/ministers")
    time.sleep(2)

    rootUrl = "https://www.gov.uk"
    urlList = []

    personLink = browser.find_elements(by=By.XPATH, value="//a[@class='app-person-link']")

    for link in personLink:
        name = link.find_element(by=By.XPATH, value="..//span[contains(@class,'app-person-link__name')]").text
        url = link.get_attribute("href")
        urlList.append({'url': url, 'name': name})

    return urlList


if __name__ == '__main__':
    with init() as browser:

        urlList = get_urls(browser)
        # urlList = [{'url': 'https://www.gov.uk/government/people/rebecca-harris'}]
        print(len(urlList))

        userList = []
        for temp in urlList:
            url = temp['url']
            print(url)
            browser.get(url)
            # browser.implicitly_wait(3)
            time.sleep(2)

            content = browser.find_element(by=By.ID, value="content")

            job = content.find_element(by=By.TAG_NAME, value="header").text
            user = {"job": job}

            try:
                user["image"] = content.find_element(by=By.XPATH, value=".//figure/img").get_attribute("src")
            except:
                pass

            userList.append({**temp, **user})

        print(userList)
