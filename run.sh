#!/bin/bash
echo afume Crawer v1.1

read -p '향수 브랜드 영문 이름을 입력하세요.\n사이트 내에서 정확한 명을 찾아 입력해주세요!(단어간 띄어쓰기, 대소문자 중요) : ' -r brandName

echo "$brandName 크롤링 시작"
python ./main.py "$brandName"