"""
    @Time           : 2022/8/17 16:20
    @Author         : fate
    @Description    : 爬取Twitter帖子内容，使用search
    @File           : app8.py
"""
import time

import chromedriver_autoinstaller
import pandas as pd
from lxml import html
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions


# 获取页面内所有帖子的url
def get_posts(url):
    """
    url:包含所有帖子的浏览页面
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
    wb = webdriver.Chrome(options=options, executable_path=driver_path)
    wb.maximize_window()  # 浏览器窗口最大化
    wb.implicitly_wait(10)  # 隐形等待10秒

    wb.get(url)
    time.sleep(3)

    # 处理网页加载
    js = 'return action=document.body.scrollHeight'
    height = wb.execute_script(js)
    wb.execute_script('window.scrollTo(0, document.body.scrollHeight)')
    time.sleep(5)

    t1 = int(time.time())
    status = True
    num = 0

    post_list = []

    while status:
        t2 = int(time.time())
        if t2 - t1 < 30:
            selector = html.etree.HTML(wb.page_source)  # # 是将HTML转化为二进制/html 格式
            infos = selector.xpath(
                "//*/div[@class='css-1dbjc4n r-18u37iz']/div[2]/div[2]/div[1]")  # //*/div[@class='css-1dbjc4n r-18u37iz']/div[2]/div[2]/div
            for info in infos:
                post = info.xpath("string(.)").strip()
                post_list.append(post)
            new_height = wb.execute_script(js)
            if new_height > height:
                time.sleep(1)
                wb.execute_script(
                    'window.scrollTo(0, document.body.scrollHeight)')
                height = new_height
                t1 = int(time.time())
        elif num < 3:
            time.sleep(3)
            num = num + 1
        else:  # 超时且重试后停止，到底页面底部
            status = False
    # return post_list
    comm_df = pd.DataFrame(post_list)
    print('here')
    comm_df.to_csv(r'./twitter_info.csv', encoding='utf_8_sig', index=False)


##只要推文的数据 √
get_posts('https://twitter.com/search?q=Beijing%20Winter%20Olympics%20Opening%20Ceremony&src=typed_query')
