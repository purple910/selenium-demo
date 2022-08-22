"""
    @Time           : 2022/8/17 15:02
    @Author         : fate
    @Description    : 获取Twitter的用户帖子
    @File           : app7.py
"""
import time
import pandas as pd

import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By

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

# 用户主页结构：#https://twitter.com/JoeBiden
url = 'https://twitter.com/JoeBiden/media/'
browser.get(url)
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
for link in browser.find_elements(by=By.XPATH, value="//a/time/parent::a"):
    url = link.get_attribute("href")
    post_urls.append(url)

print(len(post_urls))
# post_urls = ["https://twitter.com/JoeBiden/status/1545808322384764928",
#              "https://twitter.com/JoeBiden/status/1545821338790764545"]

# 依次点击post_urls中的链接，进入用户帖子爬取帖子内容
infos = []
for url in post_urls:
    try:
        browser.get(url)  # 访问用户帖子
        # article = browser.find_element(by=By.XPATH, value="//article[@tabindex=-1]")
        content = browser.find_element(by=By.XPATH, value="//article[@tabindex=-1]/div/div/div/div[3]/div[2]/div/div/span").text
        # videos = article.find_elements(by=By.XPATH, value="//video")
        # //article/div/div/div/div[3]/div[3]/div/div/div/div/div/div/ a/div/div[2]/div/img
        # //article/div/div/div/div[3]/div[3]/div/div/div/div/div/div/ a/div/div[2]/div/img
        # //article/div/div/div/div[3]/div[3]/div/div/div/div/div/div/ div[2]/div/div[2]/a/div/div/img
        # //article/div/div/div/div[3]/div[3]/div/div/div/div/div/div/ div[2]/div/div[1]/a/div/div/img
        images = browser.find_elements(by=By.XPATH, value="//article[@tabindex=-1]/img[@draggable='true']")

        info = {}
        if content:
            print('content:' + content)
            info['content']=content

        # if videos:
        #     for video in videos:
        #         src = video.get_attribute("src")
        #         print('video:' + src)

        if images:
            imgList= []
            for img in images:
                src = img.get_attribute("src")
                print('img:' + src)
                imgList.append(src)
            info['imgList',imgList]

    except:
        print('跳过该链接~')
    finally:
        infos.append(info)
    time.sleep(2)

browser.close()
browser.quit()


comm_df = pd.DataFrame(infos)
print('here')
comm_df.to_csv(r'./twitter_JoeBiden.csv', encoding='utf_8_sig', index=False)
