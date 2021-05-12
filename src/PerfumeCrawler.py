#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import csv
import json
import urllib
from datetime import datetime
import re
import sys
import time
from urllib.parse import quote

from src.repository.BrandRepository import get_brand_idx
from src.CommonCrawler import common_crawler
from src.repository.PerfumeRepository import get_perfume_idx

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
        image_file = image_path + "/{}.jpg".format(perfume["englishName"].replace(' ', "_"))
        print('향수 이미지 : {}'.format(perfume_img_url))
        if not os.path.exists(image_file):
            urllib.request.urlretrieve(perfume_img_url, image_file)
            time.sleep(1 + (15 * 156) % 3)

        note_list = []

        perfume_notes_raw = result["notes"]

        if len(perfume_notes_raw) > 0:
            top_raw = perfume_notes_raw[0]
            top_note_list = [i.text for i in top_raw]
            position = 'TOP' if len(perfume_notes_raw) > 1 else 'SINGLE'
            for t in top_note_list:
                note_list.append([perfume["englishName"], t, position])
            print('향수 top 노트 목록 : {}'.format(top_note_list))

        if len(perfume_notes_raw) > 1:
            middle_raw = perfume_notes_raw[1]
            middle_note_list = [i.text for i in middle_raw]
            for m in middle_note_list:
                note_list.append([perfume["englishName"], m, 'MIDDLE'])
            print('향수 middle 노트 목록 : {}'.format(middle_note_list))

        if len(perfume_notes_raw) > 2:
            bottom_raw = perfume_notes_raw[2]
            bottom_note_list = [i.text for i in bottom_raw]
            for b in bottom_note_list:
                note_list.append([perfume["englishName"], b, 'BASE'])
            print('향수 bottom 노트 목록 : {}'.format(bottom_note_list))

        print(perfume)
        print(note_list)
        print(keyword_list)
        perfume_list.append(perfume)
        print('--------------------------------------------------------------------')

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
    brand_name = input_keyword.replace(' ', '-')
    # "Jo-Malone", "4160 TUESDAYS LONDON", "GALIMARD", "KENZO", "GUERLAIN PARIS", "GOUTAL PARIS", "GUCCI",
    #                   "Cartier",
    #                   "Cholé", "DAVIDOFF", "Dani Mackenzie", "The Different Company", "THE BODY SHOP", "the SAEM",
    #                   "DEMETER", "Dolce & Gabbana", "DIOR", "Diptiyque Paris", "LACOSTE", "L'ARTISAN PARFUMEUR",
    #                   "RALPH LAUREN", "LANVIN", "RANCÉ 1795", "LANCOME PARIS",
    brand_list = ["LUSH", "LOEWE", "Lolita Lempicka",
                  "LOUIS VUITTON", "Le Labo", "MARC JACOPS", "Mercedes-Benz", "MEMO PARIS", "Maison Margiela PARIS",
                  "Maison Francis Kurkdjian Paris", "MONTBLANC", "MIRKO BUFFINI FIRENZE", "By Kilian", "BYREDO",
                  "Van Cleef & Arpels", "BURBERRY", "Verawang", "VERSACE", "BOTTEGA VENETA", "BOUCHERON", "BVLGARI",
                  "BULY 1803", "Santa Maria Novella", "CHANEL", "SERGE LUTENS", "Chopard", "SCUDERIA FERRARI",
                  "AMOUAGE", "Abercrombie & Fitch", "ACQUA DI PARMA", "Atelier Cologne", "AFRIMO", "ANNA SUI",
                  "ATKINSONS", "A Lab on fire", "HERMÉS PARIS", "ESTÉE LAUDER", "AERIN", "AVON", "Elizabeth Arden",
                  "ISSEY MIYAKE", "Jean Paul Gaultier", "XERJOFF", "Jo Malone London", "GIORGIO ARMAMI",
                  "john varvatos", "JIMMY CHOO", "JILL STUART", "Calvin Klein", "KENNETH COLE", "CREED", "CLEAN",
                  "Kiehl's", "TOMMY HILFIGER", "TOM FORD", "paco rabanne", "PARFUMS de MARLY", "Ferragamo", "Ferrari",
                  "PENHALIGON'S", "Forment", "Paul Smith", "POLO RALPH LAUREN", "FUEGUIA 1833", "PUIG", "Fragonard",
                  "PRADA", "FREDERIC MALLE", "fresh", "FLORIS LONDON", "philosophy", "HUGO BOSS"]

    # folder_name = datetime.now().strftime("%Y.%m.%d_%H.%M.%S")
    folder_name = datetime.now().strftime("%Y.%m.%d")
    for brand_name in brand_list:
        path = '../outputs/' + folder_name + "/" + brand_name + '/perfumes/'
        if not os.path.exists(path):
            os.makedirs(path)
        print('start test')
        print('generated file: ' + folder_name)

        brandIdx = get_brand_idx(brand_name)

        perfume_list_result = brand_perfume_crawler(path, brand_name, brandIdx)
        if len(perfume_list_result) == 0:
            continue

        with open(path + "{}.csv".format(brand_name), mode="w", encoding="utf-8", newline="") as file:
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
