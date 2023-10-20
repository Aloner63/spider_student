'''
-*- coding: utf-8 -*-
@File  : In order to proficiently operate crawlers.py
@author: zh
@NOTE  :   多线程实现
@Time  : 2023/08/20 17:04
'''

import os
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver
import random
from selenium.webdriver.common.by import By
from threading import Thread, Lock


img_path = 'e:/images_2'
count = 0
lock = Lock()


def get_info(page):
    global count

    if not os.path.exists(img_path):
        os.makedirs(img_path)

    url = 'http://www.duitang.com/category/?cat=avatar#!hot-p{}'.format(page)
    headers = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ",
        "Chrome/90.0.4430.212 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0",
        "Opera/9.80 (Windows NT 6.1; Win64; x64) Presto/2.12.388 Version/12.18"
    ]
    random_header = random.choice(headers)
    option = webdriver.EdgeOptions()
    option.add_argument('headless')
    option.add_argument(f'headers={random_header}')
    driver = webdriver.Edge(options=option)

    driver.get(url)
    # print('正在处理动态网页，请稍等...')
    time.sleep(2)


    pra_height = driver.execute_script('return document.body.scrollHeight')
    while True:
        driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
        time.sleep(1)
        now_height = driver.execute_script('return document.body.scrollHeight')
        if pra_height == now_height:
            break
        pra_height = now_height
    driver.find_element(By.XPATH, '/html/body/div[8]/div/div[1]/a').click()
    time.sleep(1)
    # print('动态网页处理完成...')
    page_source = driver.page_source
    driver.quit()

    soup = BeautifulSoup(page_source, 'lxml')
    img_soup_lists = soup.find_all('img')
    img_url_lists = set()
    for img_soup_list in img_soup_lists:
        img_src = img_soup_list['src']
        img_src_whole = urljoin(url, img_src)   #保证链接的完整性
        img_url_lists.add(img_src_whole)

    for img_url_list in img_url_lists:
        img_name_1 = img_url_list.split('/')[-1].split('_')[0]
        img_name_2 = img_url_list.split('.')[-1].split('_')[0]

        img_name = f'{img_name_1}.{img_name_2}'
        img_file_path = os.path.join(img_path, img_name)
        img_response = requests.get(img_url_list)

        with lock:
            with open(img_file_path, 'wb') as f:
                f.write(img_response.content)
                count += 1
                print(f'第{count}张图片已保存...')


# if __name__ == '__main__':
#     for i in range(11, 30):
#         get_info(i)
#     print(f'共保存了{count}张图片...')
if __name__ == '__main__':
    threads = []
    j = 1
    start=time.time()
    print('正在处理动态网页，请稍等...')
    for _ in range(2):
        for i in range(j, j + 5):
            thread = Thread(target=get_info,args=(i,))
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()
        j += 5
    end=time.time()
    time_p=end-start
    print(f'共保存了{count}张图片...')
    print(f'共用了{time_p:.2f}秒')



