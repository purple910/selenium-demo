"""
    @Time           : 2022/8/17 12:03
    @Author         : fate
    @Description    : selenium模块的基本使用
    @File           : app4.py
"""


# 导入所需要包
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
import time
import chromedriver_autoinstaller

# Chromewebdriver路径
options = ChromeOptions()
driver_path = chromedriver_autoinstaller.install()
options.add_argument('log-level=3')
# options.headless = True
browser = webdriver.Chrome(options=options, executable_path=driver_path)

# url地址
url = 'https://baidu.com'

# 访问地址
browser.get(url)

# 获取文本输入框对象
input_button = browser.find_element(by='xpath', value='//input[@id="kw"]')

# 暂缓时间输入
time.sleep(2)

# 向文本输入框输入内容
# 这里可暂缓时间方便查看，也可不暂缓时间
input_button.send_keys('罗翔')

# 获取百度一下按钮
submit = browser.find_element(by='xpath', value='//input[@id="su"]')

# 点击百度一下按钮
submit.click()

# ***这里需要一个时间暂缓***(=>1即可)
time.sleep(2)

# 滑动到最底部
js_button = 'document.documentElement.scrollTop=100000'

# 执行js，滑动到最底部
res = browser.execute_script(js_button)
print(res)

# 暂缓时间，点击下一页
time.sleep(2)

# 获取下一页对象
next_page = browser.find_element(by='xpath', value='//a[@class="n"]')

# 点击下一页
next_page.click()

# 暂缓时间
time.sleep(2)

# 返回上一页
browser.back()

# 暂缓时间
time.sleep(2)

# 回去
browser.forward()

# 暂缓时间
time.sleep(3)

# 最后退出
browser.quit()

