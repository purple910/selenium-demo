"""
    @Time           : 2022/8/18 9:18
    @Author         : fate
    @Description    : Twitter的登录,以及对用户帖子爬取
    @File           : main3.py
"""
import time

import chromedriver_autoinstaller
import requests
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By

from util import *

ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0"
proxies = {
    "http": "http://192.168.7.96:7890",
    "https": "http://192.168.7.96:7890",
}


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

    if check_exists_by_xpath(username_xpath, browser):
        username_el = browser.find_element(by=By.XPATH, value=username_xpath)
        username = get_twitter_username(".env")
        username_el.send_keys(username)
        # 回车
        username_el.send_keys(Keys.ENTER)
        time.sleep(2)

    # enter password
    password_el = browser.find_element(by=By.XPATH, value=password_xpath)
    password = get_twitter_password(".env")
    password_el.send_keys(password)
    password_el.send_keys(Keys.ENTER)
    time.sleep(5)

    return browser


def scroll_bottom(url, browser):
    """
    将页面的滚动滑道底
    :param url:
    :param browser:
    :return:
    """
    browser.get(url)
    time.sleep(1)

    # 下拉滑动条至底部，加载出所有帖子信息
    post_urls = []
    t = True
    volid = 0
    while t:
        volid = volid + 1
        check_height = browser.execute_script("return document.body.scrollHeight;")
        for r in range(10):
            time.sleep(2)
            browser.execute_script("window.scrollBy(0,1500)")

            # 找到每篇帖子的超链接
            # post_urls.add(get_urls(browser))
            links = browser.find_elements(by=By.XPATH, value="//a/time/parent::a")
            for link in links:
                url = link.get_attribute("href")
                post_urls.append(url)

        check_height1 = browser.execute_script("return document.body.scrollHeight;")
        if check_height == check_height1:
            t = False
        if volid > 1:
            t = False
    post_urls = list(set(post_urls))
    time.sleep(2)
    print("滑动结束")
    print(len(post_urls))
    return post_urls


def get_urls(browser):
    """
    定位发布日期，找到每篇帖子的超链接
    :param browser:
    :return:
    """
    post_urls = []
    links = browser.find_elements(by=By.XPATH, value="//a/time/parent::a")
    for link in links:
        url = link.get_attribute("href")
        post_urls.append(url)
    return post_urls


def get_info(post_urls, browser):
    """
    获取帖子中内容与照片
    :param post_urls:
    :param browser:
    :return:
    """
    infos = []
    for url in post_urls:
        try:
            browser.get(url)  # 访问用户帖子 css-9pa8cd /div/img
            article = browser.find_element(by=By.XPATH, value="//article[@tabindex=-1]")
            content = browser.find_element(by=By.XPATH,
                                           value="//article[@tabindex=-1]/div/div/div/div[3]/div[2]/div/div/span").text
            videos = article.find_elements(by=By.XPATH, value=".//video")
            optime = article.find_elements(by=By.XPATH, value=".//a/span")
            images = article.find_elements(by=By.XPATH, value=".//img[@draggable='true']")

            info = {}
            info['url'] = browser.current_url

            if content:
                # print('content:' + content)
                info['content'] = content

            imgList = []
            if videos:
                for video in videos:
                    src = video.get_attribute("poster")
                    # print('video:' + src)
                    imgList.append(src)

            if images:
                for img in images:
                    src: str = img.get_attribute("src")
                    if src.endswith("_normal", 0, -4):
                        # print(src)
                        pass
                    else:
                        # print('img:' + src)
                        imgList.append(src)
            info['imgList'] = imgList

            if optime:
                info['time'] = optime[0].text
                # print(info['time'])


        except:
            print('跳过该链接~')
        finally:
            infos.append(info)
        time.sleep(2)

    return infos


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


def save(infoList: []):
    """
    帖子数据存储 dirname/img|content.txt
    :param imgList:
    :param content:
    :param ptime:
    :param dirname:
    :return:
    """
    for info in infoList:
        dirname = str(info['url']).split("/")[-1]
        os.makedirs("E://twitter//" + dirname, exist_ok=True)
        for img in info["imgList"]:
            # print(img)
            save_img("E://twitter//" + dirname + "//", img)

        content = info['content']
        if content is not None and content.strip() != "":
            with open("E://twitter//" + dirname + "//" + '{}.txt'.format(time.time()), "w", encoding="utf-8") as f:
                f.write(content)
                f.close()


if __name__ == '__main__':
    with log_in() as browser:
        # 获取所有帖子地址
        # 使用search (from:JoeBiden) until:2021-04-16 since:2021-01-01 -filter:links -filter:replies
        # https://twitter.com/search?q=(from%3AJoeBiden)%20until%3A2021-04-16%20since%3A2021-01-01%20-filter%3Alinks%20-filter%3Areplies&src=typed_query
        url = 'https://twitter.com/JoeBiden/media/'
        post_urls: set = scroll_bottom(url, browser)

        # post_urls = ["https://twitter.com/JoeBiden/status/1479460570847973378",
        #              "https://twitter.com/JoeBiden/status/1512173878285684737",
        #              "https://twitter.com/JoeBiden/status/1490028761261170697",
        #              "https://twitter.com/JoeBiden/status/1559631898619641857",
        #              "https://twitter.com/purple9410/status/1559832555536662528",
        #              "https://twitter.com/purple9410/status/1560145909828427776"]

        print(post_urls)
        infos: list = get_info(post_urls, browser)

        save(infos)

        # contents = []
        # images = []
        # for info in infos:
        #     contents.append(info['content'])
        #     # images.append(info['imgList'])
        #     print(info['imgList'])
        # comm_df = pd.DataFrame(contents)
        # print('here')
        # comm_df.to_csv(r'./twitter_info.csv', encoding='utf_8_sig', index=False)

        # browser.close()
