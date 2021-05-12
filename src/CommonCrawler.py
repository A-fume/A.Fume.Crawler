from bs4 import BeautifulSoup

import time
import random
import os
from urllib.parse import quote
from selenium import webdriver

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


def get_html(base_url):
    encoded_url = quote(base_url, safe='')
    try:
        with open(os.path.join(BASE_DIR, '../cached/' + encoded_url), encoding='UTF8') as file:
            cached = ""
            for line in file:
                cached += line
        print("♖ cached " + base_url)
        return cached
    except FileNotFoundError:
        driver = webdriver.Chrome(executable_path=os.path.join(BASE_DIR, '../chromedriver'))
        time.sleep(180 + (random.randrange(10, 95) * random.randrange(10, 96)) % 60)
        driver.get(url=base_url)
        html = driver.page_source

        f = open(os.path.join(BASE_DIR, '../cached/' + encoded_url), 'w')
        f.write(html)
        time.sleep(5)
        driver.close()
        f.close()
        return html


def common_crawler(config, base_url=None):
    print(config["description"])
    base_url = base_url or config["base_url"]

    tree = config["tree"]

    html = get_html(base_url)
    bs = BeautifulSoup(html, 'html.parser')
    result = {}

    def recursive(current_tree, current_bs, log):

        if current_bs is None:
            raise RuntimeError("can not find [" + log + "]")

        if current_tree.get("children") is not None:
            if isinstance(current_tree["children"], list):
                for child in current_tree["children"]:
                    recursive(child, current_bs.select_one(current_tree["selector"]),
                              "->".join([log, (current_tree.get("description") or ".")]))
            else:
                recursive(current_tree["children"], current_bs.select_one(current_tree["selector"]),
                          "->".join([log, (current_tree.get("description") or ".")]))
            return
        key = current_tree["alias"]
        data = current_bs.select(current_tree["selector"])
        print(log + ":" + key)
        result[key] = data
        return

    recursive(tree, bs, "/")

    return result
