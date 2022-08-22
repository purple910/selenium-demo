"""
    @Time           : 2022/8/17 14:02
    @Author         : fate
    @Description    : 对facebook用户的帖子中照片进行爬取,指定帖子
    @File           : app5.py
"""
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
from selenium.webdriver.chrome.options import Options as ChromeOptions
from util import *

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
browser.implicitly_wait(2)  # 隐形等待10秒
# 访问facebook网页
try:
    browser.get('https://www.facebook.com/login.php?login_attempt=1&lwv=110/')
    time.sleep(2)
# 如果打开facebook页面失败，则尝试重新加载
except:
    browser.find_element(by=By.ID, value='reload-button').click()
    print('重新刷新页面~')
time.sleep(2)

# 输入账户密码
browser.find_element(by=By.ID, value='email').clear()
browser.find_element(by=By.ID, value='email').send_keys(get_facebook_username(".env"))
browser.find_element(by=By.ID, value='pass').clear()
browser.find_element(by=By.ID, value='pass').send_keys(get_facebook_password(".env"))

# 模拟点击登录按钮，两种不同的点击方法
try:
    browser.find_element(by=By.XPATH, value='//button[@id="loginbutton"]').send_keys(Keys.ENTER)
except:
    browser.find_element(by=By.XPATH, value='//input[@tabindex="4"]').send_keys(Keys.ENTER)
    browser.find_element(by=By.XPATH, value='//a[@href="https://www.facebook.com/?ref=logo"]').send_keys(Keys.ENTER)

time.sleep(1)

post_urls = [
    "https://www.facebook.com/fan.alice.31/posts/pfbid0WQXu4zHvo9ePRhuRa8xHgASNNp7Mq7RjsmBKcQmJkPoroV3jAd5vW7dev7EBgFXYl",
    "https://www.facebook.com/fan.alice.31/posts/pfbid0kBjSzsoYmLSpmCFwn8Xr1eaih6SLnRkLpAzRi75fiMTWFZYNkPxZs9iQ1YwhYn9vl"]
# 依次点击post_urls中的链接，进入用户帖子爬取帖子内容
post_time = []
contents = []
work_url = []
for url in post_urls:
    try:
        browser.get(url)  # 访问用户帖子
        ptime = browser.find_element(by=By.XPATH, value="//span[2]/span/a/span").text
        content = browser.find_element(by=By.XPATH, value="//div[@data-ad-preview='message']/div/div/span/div[1]").text
        imgList: list = browser.find_elements(by=By.XPATH, value="//img[@src]")
        for img in imgList:
            if img and img.get_attribute("src") and str(img.get_attribute("src")).startswith("https://"):
                print(img.get_attribute("src"))
    except:
        print('跳过该链接~')
    time.sleep(1)

print('Done!')

browser.close()
browser.quit()
