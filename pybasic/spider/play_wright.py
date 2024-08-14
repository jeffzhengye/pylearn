from playwright.sync_api import sync_playwright
from playwright.async_api import async_playwright
import re
from playwright.sync_api import Page, expect
from concurrent.futures import ThreadPoolExecutor
import requests
import io
from PIL import Image
from time import sleep


url_to_crawl = "https://www.toutiao.com/article/7239268512915735078/?log_from=08ce2c1744a9d_1685766129923"
# url_to_crawl = "https://www.baidu.com/"
url_to_crawl = "https://mbd.baidu.com/newspage/data/landingsuper?context=%7B%22nid%22%3A%22news_9317152609071613940%22%7D&n_type=-1&p_from=-1"

from playwright.sync_api import sync_playwright

# playwright = sync_playwright().start()

# browser = playwright.chromium.launch()
# page = browser.new_page()
# page.goto("https://playwright.dev/")
# page.screenshot(path="example.png")
# browser.close()

# playwright.stop()

# browser = playwright.chromium.connect_over_cdp("http://localhost:12345/")
# default_context = browser.contexts[0]
# page = default_context.pages[0]

# page.goto("https://playwright.dev/")
# page.screenshot(path="example1.png")
# browser.close()

# playwright.stop()


from playwright.sync_api import sync_playwright
import os
user_dir = 'D:/tmp'

# if not os.path.exists(user_dir):
#   os.makedirs(user_dir)

# with sync_playwright() as p:
#   browser = p.chromium.launch_persistent_context(user_dir, headless=False)
#   page = browser.new_page()
#   page.goto('https://playwright.dev/python', wait_until='domcontentloaded')
#   input('hold on')

with sync_playwright() as p:
    # login
    proxy={
        "server": "http://192.168.1.45:10809",
        # "username": "",
        # "password": ""
    }
    # browser = p.chromium.launch(headless=False, proxy=proxy)
    browser = p.chromium.launch_persistent_context(user_dir, headless=False)
    # context = browser.new_context(storage_state='D:/tmp/state.json')
    # context = browser.new_context()
    # page = context.new_page()
    page = browser.new_page()
    # page = browser.new_page(storage_state='D:/tmp/state.json')
    page.goto('https://www.toutiao.com/w/1787763802490884/?log_from=2d887c8041c5f_1705561878883')
    sleep(10)
    page.close()
    
    page = browser.new_page()
    page.goto("https://author.baidu.com/home?from=bjh_article&app_id=1690957261742989")
    sleep(10)
    page.close()
    
    page = browser.new_page()
    page.goto("https://wallhere.com/zh/wallpaper/2245884")
    input('hold on')
    # sleep(25)  # just wait for redirect - you can wait for a element...
    page.context.storage_state(path='D:/tmp/state.json')
    # page.screenshot(path='D:/tmp/after_state_init.png')

    page.close()
    browser.close()

input('hold on')

# with sync_playwright() as p:
#     # open admin dashboard without login... 
#     browser = p.chromium.launch(headless=False)
#     context = browser.new_context()
#     page = browser.new_page(storage_state='D:/tmp/state.json')
#     page.goto(f'https://www.toutiao.com/')
    
#     page1 = browser.new_page(storage_state='D:/tmp/state.json')
#     page1.goto("https://author.baidu.com/home?from=bjh_article&app_id=1690957261742989")
#     sleep(15)
#     page.screenshot(path='D:/tmp/open_using_saved_state.png')
#     page.close()
#     browser.close()