#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import csv
import json
import sys
import urllib
from datetime import datetime
import re
import time

from src.CommonCrawler import common_crawler
from src.repository.BrandRepository import get_brand_idx
from src.repository.PerfumeRepository import get_perfume_idx
from src.repository.IngredientRepository import get_ingredient_idx
from src.repository.NoteRepository import create_note

import ssl

ssl._create_default_https_context = ssl._create_unverified_context

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

TOP = 1
MIDDLE = 2
BASE = 3
SINGLE = 4


# 브랜드별 향수 정보 가져오기
def brand_perfume_crawler(dir_path, brand_name, brand_idx):
    keyword = brand_name.replace(' ', '-')  # 공백 하이픈(-)처리

    with open(os.path.join(BASE_DIR, "../json/perfume_list.json"), encoding='UTF8') as json_file:
        json_perfume_list = json.load(json_file)
    with open(os.path.join(BASE_DIR, "../json/perfume.json"), encoding='UTF8') as json_file:
        json_perfume = json.load(json_file)

    link = json_perfume_list["base_url"].format(keyword)
    print(link)
    result_link = common_crawler(json_perfume_list, base_url=link)

    perfume_list = []
    for href in [x["href"] for x in result_link["link"]]:
        link = json_perfume["base_url"].format(keyword) + href
        print(link)
        result = common_crawler(json_perfume, base_url=link)
        perfume = {"englishName": result["name"][0].text, "imageUrl": result["perfume_img"][0]["src"],
                   "story": re.sub(r'[\r\n]', '', result["story"][0].text)}

        perfume_idx = get_perfume_idx(perfume["englishName"], brand_idx, perfume["imageUrl"], perfume["story"])
        perfume["perfumeIdx"] = perfume_idx

        keyword_list = [x.text for x in result["keywords"]]
        print('향수 키워드 리스트 : {}'.format(keyword_list))

        # 향수 이미지
        perfume_img_url = perfume["imageUrl"]
        image_path = os.path.join(dir_path, str(perfume["perfumeIdx"]))
        if not os.path.exists(image_path):
            os.makedirs(image_path)
        image_file = image_path + "/{}_1.png".format(perfume_idx)
        print('향수 이미지 : {}'.format(perfume_img_url))
        if not os.path.exists(image_file):
            urllib.request.urlretrieve(perfume_img_url, image_file)
            time.sleep(1 + (15 * 156) % 3)

        note_list = []

        perfume_notes_raw = result["notes"]

        if len(perfume_notes_raw) > 0:
            top_raw = perfume_notes_raw[0]
            top_note_list = [i.text for i in top_raw]
            position = TOP if len(perfume_notes_raw) > 1 else SINGLE
            for t in top_note_list:
                note_list.append([perfume["englishName"], t, position])
            print('향수 top 노트 목록 : {}'.format(top_note_list))

        if len(perfume_notes_raw) > 1:
            middle_raw = perfume_notes_raw[1]
            middle_note_list = [i.text for i in middle_raw]
            for m in middle_note_list:
                note_list.append([perfume["englishName"], m, MIDDLE])
            print('향수 middle 노트 목록 : {}'.format(middle_note_list))

        if len(perfume_notes_raw) > 2:
            bottom_raw = perfume_notes_raw[2]
            bottom_note_list = [i.text for i in bottom_raw]
            for b in bottom_note_list:
                note_list.append([perfume["englishName"], b, BASE])
            print('향수 bottom 노트 목록 : {}'.format(bottom_note_list))

        print(perfume)
        print(note_list)
        print(keyword_list)
        perfume_list.append(perfume)
        print('--------------------------------------------------------------------')
        for note_row in note_list:
            print(note_row[1])
            ingredient_idx = get_ingredient_idx(note_row[1], '', 1)
            note_type = note_row[2]
            create_note(perfume_idx, ingredient_idx, note_type)

    print(perfume_list)
    return perfume_list


if __name__ == '__main__':
    from dotenv import load_dotenv

    # .env 파일을 절대 경로로 불러오기.
    # (python 2.8부터는 상대 경로로도 가능한 것으로 보인다.)
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # 현재 수행중인 코드가 담긴 파일의 디렉토리 절대 경로를 얻는다.
    load_dotenv(
        dotenv_path=os.path.join(BASE_DIR, "../.env"))  # .env 파일의 상대경로와 현재 디렉토리의 절대 경로를 조합해서, .env파일을 절대 경로로 불러온다.
    input_keyword = sys.argv[1]
    input_brand_name = input_keyword.replace(' ', '-')
    folder_name = datetime.now().strftime("%Y.%m.%d")

    path = '../outputs/{}/perfumes/'.format(folder_name)
    if not os.path.exists(path):
        os.makedirs(path)
    print('start test')
    print('generated file: {}'.format(folder_name))
    brandIdx = get_brand_idx(input_brand_name)
    perfume_list_result = brand_perfume_crawler(path, input_brand_name, brandIdx)
    if len(perfume_list_result) == 0:
        quit()
    with open(path + "{}.csv".format(input_brand_name), mode="w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        print(perfume_list_result[0])
        columns = perfume_list_result[0].keys()
        print(columns)
        writer.writerow(columns)
        for perfume_item in perfume_list_result:
            row = []
            for key in columns:
                row.append(perfume_item[key])
            writer.writerow(row)
        print("===========Generated {}.csv".format(brand_name))
