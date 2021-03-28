import requests
import os
from dotenv import load_dotenv


class Auth:
    __jwtToken = ""

    def get_jwt_token(self, email, password):
        if len(self.__jwtToken) > 0:
            return self.__jwtToken

        url = 'http://3.35.246.117:3001/A.fume/api/0.0.1/user/login'
        response = requests.post(url, {"email": email, "password": password})
        if response.status_code / 100 > 2:
            print(response.status_code)
            print(response.text)
            raise ConnectionError('Failed to login')
        return response.json()['data']['token']

    __instance = None

    @classmethod
    def __getInstance(cls):
        return cls.__instance

    @classmethod
    def instance(cls, *args, **kargs):
        cls.__instance = cls(*args, **kargs)
        cls.instance = cls.__getInstance
        return cls.__instance


headers = {}


def set_header(_email, _password):
    global headers
    headers = {'Content-Type': 'application/json; charset=utf-8',
               'x-access-token': ('Bearer ' + Auth.instance().get_jwt_token(_email, _password))}


def get_perfume_idx(english_name):
    url = 'http://3.35.246.117:3001/A.fume/api/0.0.1/getPerfumeIdx'
    response = requests.post(url, headers=headers, json={"englishName": english_name})
    if response.status_code / 100 > 2:
        print(response.status_code)
        print(response.text)
        return -1
    return response.json()['data']


def create_brand(english_name):
    name = english_name
    firstInitial = "-"
    description = ""
    imageUrl = ""
    url = 'http://3.35.246.117:3001/A.fume/api/0.0.1/brand'
    response = requests.post(url, headers=headers,
                             json={"name": name, "englishName": english_name, "firstInitial": firstInitial,
                                   "description": description, "imageUrl": imageUrl})
    return response.json()['data']


def get_brand_idx(english_name):
    url = 'http://3.35.246.117:3001/A.fume/api/0.0.1/brand/find'
    response = requests.post(url, headers=headers, json={"englishName": english_name})
    if response.status_code / 100 > 2:
        return create_brand(english_name)
    return response.json()['data']['brandIdx']


def create_series(english_name):
    name = english_name
    description = ""
    image_url = ""
    url = 'http://3.35.246.117:3001/A.fume/api/0.0.1/series'
    print(headers)
    response = requests.post(url, headers=headers,
                             json={"name": name, "englishName": english_name, "description": description,
                                   "imageUrl": image_url})
    print(response)
    return response.json()['data']


def get_series_idx(english_name):
    url = 'http://3.35.246.117:3001/A.fume/api/0.0.1/series/find'
    response = requests.post(url, headers=headers, json={"englishName": english_name})
    if response.status_code / 100 > 2:
        return create_series(english_name)
    return response.json()['data']['seriesIdx']


def create_ingredient(english_name, description, series_idx):
    name = english_name
    image_url = ""
    url = 'http://3.35.246.117:3001/A.fume/api/0.0.1/ingredient'
    print(headers)
    response = requests.post(url, headers=headers,
                             json={"name": name, "englishName": english_name, "description": description,
                                   "imageUrl": image_url, "seriesIdx": series_idx})
    print(response)
    return response.json()['data']


def get_ingredient_idx(english_name, description, series_idx):
    url = 'http://3.35.246.117:3001/A.fume/api/0.0.1/ingredient/find'
    response = requests.post(url, headers=headers, json={"englishName": english_name})
    if response.status_code / 100 > 2:
        return create_ingredient(english_name, description, series_idx)
    return response.json()['data']['ingredientIdx']


if __name__ == '__main__':
    load_dotenv(dotenv_path='../.env', verbose=True)
    email = os.getenv('ADMIN_EMAIL')
    password = os.getenv('ADMIN_PWD')
    set_header(email, password)

    if get_perfume_idx('154 Cologne') == 1:
        print('success getPerfumeIdx()')
    else:
        print('failed getPerfumeIdx()')
    if get_brand_idx('GALIMARD') == 3:
        print('success getBrandIdx()')
    else:
        print('failed getBrandIdx()')
    if get_series_idx('Floral') == 2:
        print('success getSeriesIdx()')
    else:
        print('failed getSeriesIdx()')
    if get_ingredient_idx('Grapefruit') == 2:
        print('success getIngredientIdx()')
    else:
        print('failed getIngredientIdx()')
