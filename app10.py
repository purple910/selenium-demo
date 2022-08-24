"""
    @Time           : 2022/8/23 11:54
    @Author         : fate
    @Description    : 多窗口
    @File           : app10.py
"""
import chromedriver_autoinstaller
from selenium import webdriver
import time

from selenium.webdriver.chrome.options import Options

options = Options()
driver_path = chromedriver_autoinstaller.install()
options.add_argument('log-level=3')
# options.headless = True
driver = webdriver.Chrome(options=options, executable_path=driver_path)

driver.get('https://www.baidu.com/')

# 打开一个新的页面
driver.execute_script("window.open('https://www.zhihu.com')")
driver.execute_script("window.open('https://www.lagou.com/')")
driver.execute_script("window.open('https://www.jianshu.com/')")

win1 = driver.window_handles[0]
driver.switch_to.window(win1)
print(driver.current_url)

time.sleep(2)

win2 = driver.window_handles[1]
driver.switch_to.window(win2)
print(driver.current_url)

time.sleep(2)

win3 = driver.window_handles[2]
driver.switch_to.window(win3)
print(driver.current_url)

time.sleep(2)

win4 = driver.window_handles[3]
driver.switch_to.window(win4)
print(driver.current_url)


