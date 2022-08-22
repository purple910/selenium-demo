"""
    @Time           : 2022/8/17 14:53
    @Author         : fate
    @Description    : 对facebook的用户的帖子中照片
    @File           : main2.py
"""
import os
import time

import chromedriver_autoinstaller
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0"
proxies = {
    "http": "http://192.168.7.96:7890",
    "https": "http://192.168.7.96:7890",
}


def login_in():
    """
    用户登录
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
    browser.find_element(by=By.ID, value='email').send_keys('purple910@qq.com')
    browser.find_element(by=By.ID, value='pass').clear()
    browser.find_element(by=By.ID, value='pass').send_keys('2018077362@QQ.com')

    # 模拟点击登录按钮，两种不同的点击方法
    try:
        browser.find_element(by=By.XPATH, value='//button[@id="loginbutton"]').send_keys(Keys.ENTER)
    except:
        browser.find_element(by=By.XPATH, value='//input[@tabindex="4"]').send_keys(Keys.ENTER)
        browser.find_element(by=By.XPATH, value='//a[@href="https://www.facebook.com/?ref=logo"]').send_keys(Keys.ENTER)
    time.sleep(5)

    return browser


def scroll_bottom(url, browser):
    """
    下拉滑动条至底部，加载出所有帖子信息
    :param url:
    :return:
    """
    # 访问用户主页
    browser.get(url)
    time.sleep(1)

    t = True
    volid = 0
    while t:
        volid = volid + 1
        check_height = browser.execute_script("return document.body.scrollHeight;")
        for r in range(10):
            time.sleep(2)
            browser.execute_script("window.scrollBy(0,1500)")
        check_height1 = browser.execute_script("return document.body.scrollHeight;")
        if check_height == check_height1:
            t = False

        if volid >= 5:
            t = False

    time.sleep(2)
    print("滑动结束")


def get_urls(browser):
    """
    定位发布日期，找到每篇帖子的超链接
    :param browser:
    :return:
    """
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

    return post_urls


def save_img(dirname, url):
    """
    照片保存
    :param url:
    :return:
    """
    with requests.get(url, headers={'User-Agent': ua}, proxies=proxies) as resp:
        # print(resp.status_code)
        resp.raise_for_status()
        # resp.encoding = res.apparent_encoding
        # 将图片内容写入
        with open(dirname + '{}.jpg'.format(time.time()), 'wb') as f:
            f.write(resp.content)
            f.close()


def save(imgList, content, ptime: time.time(), dirname):
    """
    帖子数据存储 dirname/img|content.txt
    :param imgList:
    :param content:
    :param ptime:
    :param dirname:
    :return:
    """
    os.makedirs("E://facebook//" + dirname, exist_ok=True)
    for img in imgList:
        if img and img.get_attribute("src") and str(img.get_attribute("src")).startswith("https://"):
            save_img("E://facebook//" + dirname + "//", img.get_attribute("src"))

    if content is not None and content.strip() != "":
        with open("E://facebook//" + dirname + "//" + '{}.txt'.format(time.time()), "w", encoding="utf-8") as f:
            f.write(content)
            f.close()


def get_info(post_urls, browser):
    """
    依次点击post_urls中的链接，进入用户帖子爬取帖子内容
    :return:
    """
    post_time = []
    contents = []
    work_url = []
    for url in post_urls:
        try:
            # 访问用户帖子 data-ad-comet-preview="message" data-ad-preview="message"
            browser.get(url)
            current_url = browser.current_url
            target = None
            content = None
            if current_url.__contains__("watch"):
                # 选取WatchPermalinkVideo的父节点
                target = browser.find_element(by=By.XPATH, value="//div[@data-pagelet='WatchPermalinkVideo']/..")
                content = target.find_element(by=By.XPATH, value="./div[2]/div[1]").text
                # print(content)
                # pass
            else:
                # 选取ignore-dynamic父节点的同级前一个节点
                targets = browser.find_elements(by=By.XPATH,
                                                value="//div[@data-visualcompletion='.gitignore-dynamic']/../preceding-sibling::div[1]")
                target = targets[1]

                # 可能没有文本信息
                # if target.find_element(by=By.XPATH, value="./div").get_attribute("data-ad-preview"):
                #     content = target.find_element(by=By.XPATH,
                #                                   value=".//div[@data-ad-preview='message']/div/div/span/div[1]").text
                #     print(content)
                content = target.text

            ptime = browser.find_element(by=By.XPATH, value=".//span[2]/span/a/span").text

            imgList = target.find_elements(by=By.XPATH, value=".//img[@src]")
            # for img in imgList:
            #     if img and img.get_attribute("src") and str(img.get_attribute("src")).startswith("https://"):
            #         # save_img(img.get_attribute("src"))
            #         print(img.get_attribute("src"))
            #         pass

            if current_url.__contains__("?v"):
                # print("1:" + current_url.split("?v=")[-1])
                save(imgList, content, ptime, current_url.split("?v=")[-1])
            else:
                # print("2:" + current_url.split("/")[-1])
                save(imgList, content, ptime, current_url.split("/")[-1])

            # print(ptime)
        except Exception as e:
            print(url)
            print(e)
            print('跳过该链接~')
        time.sleep(1)


if __name__ == '__main__':
    # 用户主页结构：#https://www.facebook.com/fan.alice.31/
    # 构造url
    name = 'joebiden'
    # name = 'fan.alice.31'
    url = 'https://www.facebook.com/' + name + '/'
    with login_in() as browser:
        # scroll_bottom(url, browser)
        #
        # post_urls = get_urls(browser)
        post_urls = [
            "https://www.facebook.com/joebiden/posts/pfbid02SmYC2DFBkbAzEasFpSbYkGJDM6zm2zUxBmSW8WTFN4ZQcKsYpCtcnnKySkQuxkiBl",
            "https://www.facebook.com/joebiden/posts/pfbid0tTPGahX1gVAqcfP7P3g6rbi4vwUWfA1TrQNjyVZLdEamoZDcRTE3zuxd84ixRGVQl",
            "https://www.facebook.com/watch/?v=1169659546923764",
            "https://www.facebook.com/joebiden/posts/pfbid03d29YWU4R4xgMidsqoUU1HrbeD2vMzMS4dpFva541Ntabp6Ah77Y49HoveCkkUYwl"]

        get_info(post_urls, browser)
