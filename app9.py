"""
    @Time           : 2022/8/18 9:18
    @Author         : fate
    @Description    : Twitter的登录脚本
    @File           : app9.py
"""
import time
from turtle import pd

import chromedriver_autoinstaller
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from util import *


def check_exists_by_xpath(xpath, driver):
    """
    判断xpath是否存在
    :param xpath:
    :param driver:
    :return:
    """
    timeout = 3
    try:
        driver.find_element(by=By.XPATH, value=xpath)
    except NoSuchElementException:
        return False
    return True

def check_exists_by_link_text(text, driver):
    """
    判断文本内容是否存在
    :param text:
    :param driver:
    :return:
    """
    try:
        driver.find_element_by_link_text(text)
    except NoSuchElementException:
        return False
    return True

def log_in():
    """
    模拟用户登录
    :return:
    """
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

    # 用户登录
    browser.get('https://twitter.com/i/flow/login')
    email_xpath = '//input[@autocomplete="username"]'
    password_xpath = '//input[@autocomplete="current-password"]'
    username_xpath = '//input[@data-testid="ocfEnterTextTextInput"]'

    # enter email
    email_el = browser.find_element(by=By.XPATH, value=email_xpath)
    email = get_twitter_email(".env")
    email_el.send_keys(email)
    # 回车
    email_el.send_keys(Keys.ENTER)
    time.sleep(2)

    if check_exists_by_xpath(username_xpath,browser):
        username_el = browser.find_element(by=By.XPATH, value=username_xpath)
        username = get_twitter_username(".env")
        username_el.send_keys(username)
        # 回车
        username_el.send_keys(Keys.ENTER)
        time.sleep(2)

    # enter password
    password_el = browser.find_element(by=By.XPATH,value=password_xpath)
    password= get_twitter_password(".env")
    password_el.send_keys(password)
    password_el.send_keys(Keys.ENTER)
    time.sleep(5)
    # 主页
    browser.get('https://twitter.com/home')
    time.sleep(5)

    return browser


if __name__ == '__main__':
    with log_in() as browser:
        # browser.close()
        pass
