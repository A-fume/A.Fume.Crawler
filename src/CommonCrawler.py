from bs4 import BeautifulSoup

import time
import random
from selenium import webdriver

driver = webdriver.Chrome(executable_path='../chromedriver')


def common_crawler(config, base_url=None):
    print(config["description"])
    base_url = base_url or config["base_url"]
    print(base_url)
    tree = config["tree"]

    time.sleep(random.randrange(1, 5))
    driver.get(url=base_url)

    bs = BeautifulSoup(driver.page_source, 'html.parser')
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
        time.sleep(random.randrange(1, 5))
        return

    recursive(tree, bs, "/")

    return result
