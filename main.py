#!/usr/bin/python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import urllib.request
import time
import random
import os
import csv
import pandas as pd
import sys
from datetime import datetime
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env', verbose=True)
# 브랜드별 향수 정보 가져오기
def brand_perfume_crawler(dir_path, brand_name, brand_idx, site_url, site_name, header):
    keyword = brand_name.replace(' ', '-')  # 공백 하이픈(-)처리

    try:
        link = (site_url + '/designers/{}.html').format(keyword)
        res = requests.get(link, headers={'User-agent': header})  # 헤더 추가해서 429 에러 우회
        bs = BeautifulSoup(res.text, 'html.parser')

        # csv 파일 생성
        file = open(dir_path + brand_name + ".csv", mode="w", encoding="utf-8", newline="")
        writer = csv.writer(file)
        writer.writerow(["p.name", "i.name", "position"])

        # 1. 브랜드별 향수 목록 가져오기
        all_perfume_url = []
        for i in bs.select(
                'body div#main-content div#brands div.cell.text-left.prefumeHbox.px1-box-shadow div.flex-child-auto h3 a'):
            perfume_url = i["href"]
            all_perfume_url.append(perfume_url)
        for i in all_perfume_url:
            print(i)

        print()
        time.sleep(300)

        # 2. 특정 향수 정보 가져오기
        for perfume_url in all_perfume_url:

            time.sleep(random.randrange(30, 60))

            res2 = requests.get(site_url + perfume_url, headers={'User-agent': header})  # 헤더 추가해서 429 에러 우회
            bs2 = BeautifulSoup(res2.text, 'html.parser')
            perfume_info = {}
            perfume_keyword_list = []
            top_note_list = []
            attribute_error_count = 0

            # body 내부 main content 발췌
            main_content = bs2.select_one(
                'body div#main-content div.grid-x.grid-margin-x div.grid-x.bg-white.grid-padding-x.grid-padding-y')

            # 향수 이름
            perfume_name = main_content.select_one('div#toptop > h1').text
            print('향수 이름 : {}'.format(perfume_name))

            # 향수 이미지
            perfume_img = main_content.select_one(
                'div.cell.small-12 div.grid-x.grid-margin-x.grid-margin-y div.cell.small-6.text-center div.cell.small-12 img')[
                "src"]
            urllib.request.urlretrieve(perfume_img, dir_path + perfume_name + ".jpg")
            print('향수 이미지 : {}'.format(perfume_img))

            # 향수 키워드 목록
            for i in main_content.select(
                    'div.cell.small-12 div.grid-x.grid-margin-x.grid-margin-y div.cell.small-6.text-center div.grid-x div.cell.accord-box'):
                keyword = i.select_one('div.accord-bar').text
                perfume_keyword_list.append(keyword)
            print('향수 키워드 목록 : {}'.format(perfume_keyword_list))

            # 향수 스토리 요약 & 본문
            perfume_story_raw = main_content.select_one(
                'div.cell.small-12 div.grid-x.grid-margin-x.grid-margin-y div[itemprop=description]')
            perfume_story_summary = perfume_story_raw.select_one('p').text
            print('향수 스토리 요약 : {}'.format(perfume_story_summary))
            perfume_story_detail_raw = perfume_story_raw.select('div.' + site_name + '-blockquote p')
            perfume_story_detail_str = ''
            for i in perfume_story_detail_raw:
                perfume_story_detail_str += i.text + ' \n'
            perfume_story_detail = perfume_story_detail_str[:-2]  # 문자열 맨 끝 \n 제거
            print('향수 스토리 본문 : {}'.format(perfume_story_detail))

            # 향수 노트(top/middle/bottom)
            perfume_notes_raw = main_content.select('div#pyramid div.cell div div[style^="display: flex"]')

            top_raw = perfume_notes_raw[0]
            top_note_list = [i.text for i in top_raw]
            position = 'TOP' if len(perfume_notes_raw) > 1 else 'SINGLE'
            for t in top_note_list:
                writer.writerow([perfume_name, t, position])
            print('향수 top 노트 목록 : {}'.format(top_note_list))

            if len(perfume_notes_raw) > 1:
                middle_raw = perfume_notes_raw[1]
                middle_note_list = [i.text for i in middle_raw]
                for m in middle_note_list:
                    writer.writerow([perfume_name, m, 'MIDDLE'])
                print('향수 middle 노트 목록 : {}'.format(middle_note_list))

                bottom_raw = perfume_notes_raw[2]
                bottom_note_list = [i.text for i in bottom_raw]
                for b in bottom_note_list:
                    writer.writerow([perfume_name, b, 'BASE'])
                print('향수 bottom 노트 목록 : {}'.format(bottom_note_list))

            print('--------------------------------------------------------------------')

        file.close()

    except AttributeError as e:
        print(e)

    return all_perfume_url


def run(dir_path, brand_name):
    # 환경변수 불러오기
    site_url = os.getenv('SITE_URL')
    site_name = os.getenv('SITE_NAME')
    header = os.getenv('HEADER')

    perfume_list = brand_perfume_crawler(path, brandName, site_url, site_name, header)
    pd.read_csv(path + brandName + ".csv")
    perfume_list = brand_perfume_crawler(dir_path, brand_name, brandIdx, site_url, site_name, header)
    pd.read_csv(dir_path + brand_name + ".csv")


if __name__ == '__main__':
    input_keyword = sys.argv[1]
    brandName = input_keyword.replace(' ', '-')
    path = './outputs/' + datetime.now().strftime("%Y.%m.%d_%H.%M.%S") + '/' + brandName + '/'
    os.makedirs(path)
    run(path, brandName)
