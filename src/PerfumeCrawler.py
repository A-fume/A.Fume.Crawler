#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import csv
import json
import urllib
from datetime import datetime
import re
import sys

from src.repository.BrandRepository import get_brand_idx
from src.CommonCrawler import common_crawler

import ssl

ssl._create_default_https_context = ssl._create_unverified_context

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


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
        perfume = {"perfumeName": result["name"][0].text, "imageUrl": result["perfume_img"][0]["src"],
                   "story": re.sub(r'[\r\n]', '', result["story"][0].text)}

        keyword_list = [x.text for x in result["keywords"]]
        print('향수 키워드 리스트 : {}'.format(keyword_list))

        # 향수 이미지
        perfume_img_url = perfume["imageUrl"]
        image_path = os.path.join(dir_path, perfume["perfumeName"].replace(' ', "_"))
        if not os.path.exists(image_path):
            os.makedirs(image_path)
        image_file = image_path + "/{}.jpg".format(perfume["perfumeName"].replace(' ', "_"))
        print('향수 이미지 : {}'.format(perfume_img_url))
        urllib.request.urlretrieve(perfume_img_url, image_file)

        note_list = []

        perfume_notes_raw = result["notes"]

        if len(perfume_notes_raw) > 0:
            top_raw = perfume_notes_raw[0]
            top_note_list = [i.text for i in top_raw]
            position = 'TOP' if len(perfume_notes_raw) > 1 else 'SINGLE'
            for t in top_note_list:
                note_list.append([perfume["perfumeName"], t, position])
            print('향수 top 노트 목록 : {}'.format(top_note_list))

        if len(perfume_notes_raw) > 1:
            middle_raw = perfume_notes_raw[1]
            middle_note_list = [i.text for i in middle_raw]
            for m in middle_note_list:
                note_list.append([perfume["perfumeName"], m, 'MIDDLE'])
            print('향수 middle 노트 목록 : {}'.format(middle_note_list))

        if len(perfume_notes_raw) > 2:
            bottom_raw = perfume_notes_raw[2]
            bottom_note_list = [i.text for i in bottom_raw]
            for b in bottom_note_list:
                note_list.append([perfume["perfumeName"], b, 'BASE'])
            print('향수 bottom 노트 목록 : {}'.format(bottom_note_list))

        print(perfume)
        print(note_list)
        print(keyword_list)
        perfume_list.append(perfume)
        print('--------------------------------------------------------------------')

    print(perfume_list)
    return perfume_list
