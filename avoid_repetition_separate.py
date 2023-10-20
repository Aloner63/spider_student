'''
-*- coding: utf-8 -*-
@File  : avoid_repetition_separate.py
@author: zh
@NOTE  : 图片的爬取,避免重复图片的保存，分函数版本
@Time  : 2023/08/03 17:51
'''

import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from PIL import Image
from io import BytesIO


def get_info(url, headers):
    try:
        response = requests.get(url=url, headers=headers)
        response.encoding = response.apparent_encoding
        content = response.text
        soup = BeautifulSoup(content, 'lxml')
        img_tags = soup.find_all('img')
        img_url_lists = set()

        for img_tag in img_tags:
            img_url = img_tag['src']
            img_url_whole = urljoin(url, img_url)
            img_url_lists.add(img_url_whole)

        return img_url_lists

    except Exception as e:
        print(e)
        return None


def save_img(img_url_lists, img_path, desired_width, desired_height):
    try:
        if not os.path.exists(img_path):
            os.makedirs(img_path)

        for img_url_er in img_url_lists:
            img_name = img_url_er.split('/')[-1].split('?')[0]
            img_file_path = os.path.join(img_path, img_name)

            img_response = requests.get(img_url_er)

            # Get image dimensions using PIL
            img_data = BytesIO(img_response.content)
            img = Image.open(img_data)
            img_width, img_height = img.size

            # Check if the image meets the desired size criteria
            if img_width >= desired_width and img_height >= desired_height:
                with open(img_file_path, 'wb') as f:
                    f.write(img_response.content)
                    print(f'图片 <{img_name}> 已经保存到 {img_path}')

    except Exception as e:
        print(e)


def main(page):
    url = 'http://www.duitang.com/category/?cat=avatar#!hot-p{}'.format(page)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/52.0.2743.116 Safari/537.36'
    }
    img_path = 'e:/images'
    desired_width = 100  # Adjust this value to your desired width
    desired_height = 100  # Adjust this value to your desired height

    img_url_lists = get_info(url, headers)
    if img_url_lists is not None:
        save_img(img_url_lists, img_path, desired_width, desired_height)


if __name__ == '__main__':

    main()

