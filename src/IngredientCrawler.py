#!/usr/bin/python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import time
import random
import os
import csv
from datetime import datetime
from dotenv import load_dotenv
import Repository
from Repository import get_ingredient_idx
from Repository import get_series_idx
from Repository import set_header


# 재료 링크 리스트 가져오기
def ingredient_list_crawler(dir_path, site_url, query_ingredient, query_ingredient_name, query_ingredient_series_name,
                            query_ingredient_descripyion,
                            header):
    try:
        res = requests.get(site_url, headers={'User-agent': header})  # 헤더 추가해서 429 에러 우회
        bs = BeautifulSoup(res.text, 'html.parser')

        # csv 파일 생성
        file = open(dir_path + "ingredients.csv", mode="w", encoding="utf-8", newline="")
        writer = csv.writer(file)
        writer.writerow(["ingredientIdx", "name", "englishName", "description", "imageUrl", "seriesIdx"])

        # 1. 재료 목록 가져오기
        all_ingredient_url = []
        for i in bs.select(query_ingredient):
            ingredient_url = i["href"]
            all_ingredient_url.append(ingredient_url)
        print(all_ingredient_url)

        # 2. 특정 재료 정보 가져오기
        for ingredient_url in all_ingredient_url:
            time.sleep(random.randrange(3, 6))
            print(ingredient_url)

            res2 = requests.get(ingredient_url, headers={'User-agent': header})  # 헤더 추가해서 429 에러 우회
            bs2 = BeautifulSoup(res2.text, 'html.parser')
            ingredient_info = {}

            # body 내부 main content 발췌
            main_content = bs2.select_one('#main-content')

            # body 내부 main content 발췌
            ingredient_name = main_content.select_one(query_ingredient_name).text
            print(ingredient_name)

            series_name = main_content.select_one(query_ingredient_series_name).text
            print(series_name)
            series_idx = get_series_idx(series_name)
            print(series_idx)

            div_ingredient = main_content.select_one(query_ingredient_descripyion)

            ingredient_description = ''
            if div_ingredient is not None:
                ingredient_description = div_ingredient.text.replace('Odor profile: ', '')
            print(ingredient_description)

            ingredient_idx = get_ingredient_idx(ingredient_name, ingredient_description, series_idx)

            print(ingredient_name + "/" + ingredient_description + "/" + str(series_idx))
            writer.writerow([ingredient_idx, ingredient_name, ingredient_name, ingredient_description, "", series_idx])

        file.close()

    except AttributeError as e:
        print(e)

    return all_ingredient_url


if __name__ == '__main__':
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    load_dotenv(dotenv_path=os.path.join(BASE_DIR, "../.env"))
    email = os.getenv('ADMIN_EMAIL')
    password = os.getenv('ADMIN_PWD')
    site_url_ingredient = os.getenv('SITE_URL_INGREDIENT')
    print(email, password, site_url_ingredient)
    set_header(email, password)

    site_url_ingredient = os.getenv('SITE_URL_INGREDIENT')
    query_ingredient = os.getenv('QUERY_INGREDIENT_HREF')
    query_ingredient_name = os.getenv('QUERY_INGREDIENT_NAME')
    query_ingredient_series_name = os.getenv('QUERY_INGREDIENT_SERIES_NAME')
    query_ingredient_description = os.getenv('QUERY_INGREDIENT_DESCRIPTION')
    header = os.getenv('HEADER')

    folder_name = datetime.now().strftime("%Y.%m.%d_%H.%M.%S")
    path = '../outputs/' + folder_name + '/ingredients/'
    os.makedirs(path)
    print('start test')
    print('generated file: ' + folder_name)
    ingredient_list_crawler(dir_path=path, site_url=site_url_ingredient, query_ingredient=query_ingredient,
                            query_ingredient_name=query_ingredient_name,
                            query_ingredient_series_name=query_ingredient_series_name,
                            query_ingredient_descripyion=query_ingredient_description,
                            header=header)
