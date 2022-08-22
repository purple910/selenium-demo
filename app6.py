"""
    @Time           : 2022/8/17 14:38
    @Author         : fate
    @Description    : 爬取facebook用户帖子中照片
    @File           : app6.py
"""
import time

import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

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
browser.implicitly_wait(10)  # 隐形等待10秒
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
email = get_facebook_username(".env")
browser.find_element(by=By.ID, value='email').send_keys(email)
browser.find_element(by=By.ID, value='pass').clear()
password = get_facebook_password(".env")
browser.find_element(by=By.ID, value='pass').send_keys(password)

# 模拟点击登录按钮，两种不同的点击方法
try:
    browser.find_element(by=By.XPATH, value='//button[@id="loginbutton"]').send_keys(Keys.ENTER)
except:
    browser.find_element(by=By.XPATH, value='//input[@tabindex="4"]').send_keys(Keys.ENTER)
    browser.find_element(by=By.XPATH, value='//a[@href="https://www.facebook.com/?ref=logo"]').send_keys(Keys.ENTER)
time.sleep(5)

# 用户主页结构：#https://www.facebook.com/fan.alice.31/
# 构造url
name = 'fan.alice.31'
url = 'https://www.facebook.com/' + name + '/'
browser.get(url)  # 访问用户主页
time.sleep(1)

# 下拉滑动条至底部，加载出所有帖子信息
t = True
while t:
    check_height = browser.execute_script("return document.body.scrollHeight;")
    for r in range(20):
        time.sleep(2)
        browser.execute_script("window.scrollBy(0,1500)")
    check_height1 = browser.execute_script("return document.body.scrollHeight;")
    if check_height == check_height1:
        t = False
time.sleep(2)
print("滑动结束")

# 定位发布日期，找到每篇帖子的超链接
post_urls = []
# for link in browser.find_elements_by_xpath("//span[starts-with(@id,'jsc_c')]/span[2]/span/a"):
for link in browser.find_elements(by=By.XPATH, value="//span[starts-with(@id,'jsc_c')]/span[2]/span/a"):
    url = str(link.get_attribute('href')).split('?')[0]
    # 注意！！！link.get_attribute('href')返回的一个结果为：
    # https://www.facebook.com/fan.alice.31/posts/1574509182705311?__cft__[0]=AZWWrKVCLX2teHSF7weZfTtfpdLvUhCwTwZj9eGyviXSYa1OWmlH0MOMt8XeEo0Q0U1LaK2eSor1TEuL5QluW1f8RQPdd0omdAZM8PccCmEoLO-iY9goWjfXZxpnNO4XguQAXRifjmy-U6YZYp6baUxNfnep0cFscw6pczE2NJ72Aw&__tn__=%2CO%2CP-R
    # 其中，只有？前面部分为用户帖子对应的链接，因此，使用了split进行字符串分割
    post_urls.append(url)

# 删除 'https://www.facebook.com/photo/'这类链接
post_urls = list(set(post_urls))
for url in post_urls:
    if url == 'https://www.facebook.com/photo/':
        post_urls.remove(url)
print(len(post_urls))

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

browser.close()
browser.quit()
