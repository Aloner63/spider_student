'''
-*- coding: utf-8 -*-    
@File  : tkd_get.py
@author: zh
@NOTE  : 天科大--实验
@Time  : 2023/08/20 23:59
'''

import os
from itertools import cycle
from urllib.parse import urljoin
import requests
from PIL import Image
from bs4 import BeautifulSoup
import time
from io import BytesIO
from selenium import webdriver
import random
from selenium.webdriver.common.by import By
from threading import Thread, Lock

count = 0
lock = Lock()


def get_info():
    global count

    proxy_servers = "51.158.54.46:49139"

    url = 'https://www.zjtu.cc/label/rb/'
    headers = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0",
        "Opera/9.80 (Windows NT 6.1; Win64; x64) Presto/2.12.388 Version/12.18"
    ]
    random_header = random.choice(headers)
    option = webdriver.EdgeOptions()
    # option.add_argument('headless')
    option.add_argument(f'headers={random_header}')
    option.add_argument(f'proxy-server={proxy_servers}')  # 使用代理
    driver = webdriver.Edge(options=option)

    driver.get(url)
    i = 1
    while i < 10:
        driver.refresh()
        time.sleep(0.5)

        i += 1
        with lock:
            count += 1
            print(f'第{count}次刷新...')
    driver.quit()


if __name__ == '__main__':
    threads = []

    start = time.time()
    for _ in range(8):
        thread = Thread(target=lambda: get_info())
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    end = time.time()
    time_p = end - start
    print('程序运行结束...')
    print(f'共运行了{time_p:.2f}秒')
