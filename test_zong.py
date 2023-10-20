'''
-*- coding: utf-8 -*-
@File  : In order to proficiently operate crawlers.py
@author: zh
@NOTE  :
@Time  : 2023/08/20 17:04
'''
import os
from urllib.parse import urljoin
import requests
from PIL import Image
from bs4 import BeautifulSoup
import time
from io import BytesIO
from selenium import webdriver
import random
from selenium.webdriver.common.by import By

count = 0


def handle_dynamics_page(url, headers):
    print('正在处理动态网页，请稍等...')
    random_headers = random.choice(headers)
    option = webdriver.EdgeOptions()
    # option.add_argument('headless')
    option.add_argument(f'user-agent={random_headers}')

    driver = webdriver.Edge(options=option)
    driver.get(url)
    time.sleep(2)

    pre_height = driver.execute_script('return document.body.scrollHeight')

    while True:
        driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
        time.sleep(2)
        now_height = driver.execute_script('return document.body.scrollHeight')

        if now_height == pre_height:
            break
        pre_height = now_height
    time.sleep(1)
    driver.find_element(By.XPATH, '/html/body/div[8]/div/div[1]/a').click()
    time.sleep(0.5)
    page_source_dynamics = driver.page_source
    driver.quit()
    print('动态网页已处理完毕...')
    return page_source_dynamics


def get_image_url_lists(page_source_dynamics):
    img_url_lists = set()

    soup = BeautifulSoup(page_source_dynamics, 'lxml')
    img_soup_lists = soup.find_all('img')

    for img_soup_list in img_soup_lists:
        img_src_url = img_soup_list['src']
        img_src_url_whole = urljoin(url_1, img_src_url)
        img_url_lists.add(img_src_url_whole)

    return img_url_lists


def save_image_to_local(img_path, img_url_lists, img_width_min, img_height_min):
    try:
        global count
        if not os.path.exists(img_path):
            os.makedirs(img_path)

        for img_url in img_url_lists:
            img_response = requests.get(img_url)
            img_data = BytesIO(img_response.content)
            img = Image.open(img_data)

            img_width, img_height = img.size

            if img_width >= img_width_min and img_height >= img_height_min:
                img_name = img_url.split('/')[-1].split('_')[0]+'.jpg'
                img_file_path = os.path.join(img_path, img_name)

                with open(img_file_path, 'wb') as f:
                    f.write(img_response.content)
                    count += 1
                    print(f'第{count}张已保存....')



    except Exception as e:
        print(e)


if __name__ == '__main__':
    url_1 = 'http://www.duitang.com/category/?cat=avatar#!hot-p2'
    headers_1 = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 "
        "Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/92.0.902.84 "
        "Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/91.0.2"
    ]
    img_path_1 = 'e:/images_1'
    img_width_min_1 = 50
    img_height_min_1 = 50

    page_source = handle_dynamics_page(url_1, headers_1)
    img_url_lists_1 = get_image_url_lists(page_source)
    save_image_to_local(img_path_1, img_url_lists_1, img_width_min_1, img_height_min_1)
    print(f'共保存了{count}张图片...')