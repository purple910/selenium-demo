"""
    @Time           : 2022/8/23 15:31
    @Author         : fate
    @Description    : 反反爬虫
    @File           : app11.py
"""
# 浏览器配置对象
from selenium import webdriver

options = webdriver.ChromeOptions()
# 以开发者模式启动浏览器
options.add_experimental_option('excludeSwitches', ['enable-automation'])
# 屏蔽以开发者运行提示框
# options.add_experimental_option('useAutomationExtension', False)
# 屏蔽保存密码提示框
prefs = {'credentials_enable_service': False, 'profile.password_manager_enabled': False}
options.add_experimental_option('prefs', prefs)
# chrome 88 或更高版本的反爬虫特征处理
options.add_argument('--disable-blink-features=AutomationControlled')
# 浏览器对象
driver = webdriver.Chrome(options=options)
# 读取脚本 下载 stealth.min.js 到本地
with open('stealth.min.js', mode='r', encoding='utf-8') as f:
    string = f.read()
# 移除 selenium 中的爬虫特征
driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {'source': string})

driver.get("https://www.bing.com/")
