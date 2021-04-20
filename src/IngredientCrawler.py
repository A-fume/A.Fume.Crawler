#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import csv
import json
from datetime import datetime

from src.repository.IngredientRepository import get_ingredient_idx
from src.repository.SeriesRepository import get_series_idx
from src.CommonCrawler import common_crawler

# 현재 수행중인 코드가 담긴 파일의 디렉토리 절대 경로를 얻는다.
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


# 재료 리스트 가져오기
def ingredient_list_crawler(dir_path):
    with open(os.path.join(BASE_DIR, "../json/ingredient_list.json")) as json_file:
        json_ingredient_list = json.load(json_file)

    with open(os.path.join(BASE_DIR, "../json/ingredient.json")) as json_file:
        json_ingredient = json.load(json_file)

    result_link = common_crawler(json_ingredient_list)

    ingredient_list = []
    for href in map(lambda x: x["href"], result_link["link"]):
        result = common_crawler(json_ingredient, base_url=href)

        ingredient = {"ingredientName": result["name"][0].text, "seriesName": result["seriesName"][0].text}
        if len(result["description"]) > 0:
            ingredient["description"] = result["description"][0].text.replace('Odor profile: ', '')
        else:
            ingredient["description"] = ''
        ingredient["seriesIdx"] = get_series_idx(ingredient["seriesName"])
        ingredient["ingredientIdx"] = get_ingredient_idx(ingredient["ingredientName"], ingredient["description"],
                                                         ingredient["seriesIdx"])

        ingredient_list.append(ingredient)
        print(str(ingredient))

    try:
        # csv 파일 생성
        file = open(dir_path + "ingredients.csv", mode="w", encoding="utf-8", newline="")
        writer = csv.writer(file)
        columns = ["ingredientIdx", "name", "englishName", "description", "imageUrl", "seriesIdx"]
        writer.writerow(columns)

        for ingredient in ingredient_list:
            row = []
            for column in columns:
                if column in ingredient:
                    row.append(ingredient[column])
                else:
                    row.append('')
            writer.writerow(row)
        file.close()
    except AttributeError as e:
        print(e)
    return ingredient_list


if __name__ == '__main__':
    from dotenv import load_dotenv

    # .env 파일을 절대 경로로 불러오기.
    # (python 2.8부터는 상대 경로로도 가능한 것으로 보인다.)
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # 현재 수행중인 코드가 담긴 파일의 디렉토리 절대 경로를 얻는다.
    load_dotenv(
        dotenv_path=os.path.join(BASE_DIR, "../.env"))  # .env 파일의 상대경로와 현재 디렉토리의 절대 경로를 조합해서, .env파일을 절대 경로로 불러온다.

    folder_name = datetime.now().strftime("%Y.%m.%d_%H.%M.%S")
    path = '../outputs/' + folder_name + '/ingredients/'
    os.makedirs(path)
    print('start test')
    print('generated file: ' + folder_name)
    ingredient_list_crawler(dir_path=path)
