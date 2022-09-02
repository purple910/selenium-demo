# urls = set([])
#
# urls.add('aa')
# urls.add('aa')
# urls.add('aa11')
# # urls.add(['aa','bbb11','ccc11'])
#
# print(len(urls))
#
# for u in urls:
#     print(u)
#
# temp = "https://pbs.twimg.com/profile_images/1308769664240160770/AfgzWVE7_normal.jpg".endswith("normal",-4,-1)
# print(temp)


# txt = "apple, banana, cherry"
# # 将 max 参数设置为 1，将返回包含 2 个元素的列表！
# x = txt.rsplit(", ")[-1]
# print(x)
# import os
#
# dirname = "111111"
# os.makedirs("E://facebook//" + dirname, exist_ok=True)


# a= []
# a.append("aaa")
# a.append("bbb")
# a.append("ccc")
# a.append("aaa")
# a = list(set(a))
# print(len(a))
import time

import requests

a = 'aa'
v = 12

print({a, v})

ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0"
proxies = {
    "http": "http://192.168.7.96:7890",
    "https": "http://192.168.7.96:7890",
}

with requests.get("https://bioguide.congress.gov/bioguide/photo/S/S000320.jpg", headers={'User-Agent': ua},
                  proxies=proxies) as resp:
    # print(resp.status_code)
    resp.raise_for_status()
    # resp.encoding = res.apparent_encoding
    # 将图片内容写入
    with open('{}.jpg'.format(time.time()), 'wb') as f:
        f.write(resp.content)
        f.close()
