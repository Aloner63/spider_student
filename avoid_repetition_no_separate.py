'''
-*- coding: utf-8 -*-
@File  : avoid_repetition_no_separate.py
@author: zh
@NOTE  : 图片的爬取,避免重复图片的保存，不分函数版
@Time  : 2023/08/03 17:51
'''




import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os


url = 'https://e.dangdang.com/list-ZTXYTL-comment-0-1.html'
headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/52.0.2743.116 Safari/537.36'
    }
# 发起HTTP请求并获取页面内容
response = requests.get(url=url, headers=headers)
response.encoding = response.apparent_encoding
content = response.text
soup = BeautifulSoup(content, 'lxml')
img_tags = soup.find_all('img')



try:
    img_path = 'e:/images'

    if not os.path.exists(img_path):
            os.makedirs(img_path)

    img_url_lists = set()
    for img_tag in img_tags:
        img_url = img_tag['src']
        img_url_whole = urljoin(url, img_url)
        img_url_lists.add(img_url_whole)

    for img_url_er in img_url_lists:
        img_name = img_url_er.split('/')[-1].split('?')[0]
        img_file_path = os.path.join(img_path, img_name)

        img_response = requests.get(img_url_er)

        with open(img_file_path, 'wb') as f:
            f.write(img_response.content)

            print(f' 图片 <{img_name}> 已经保存到 {img_path}')


except Exception as e:
        print(e)

