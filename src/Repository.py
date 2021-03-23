import requests
import os
from dotenv import load_dotenv

if __name__ == '__main__':
    load_dotenv(dotenv_path='../.env', verbose=True)


class Auth:
    __jwtToken = ""

    def getJWToken(self):
        if len(self.__jwtToken) > 0:
            return self.__jwtToken
        email = os.getenv('ADMIN_EMAIL')
        password = os.getenv('ADMIN_PWD')

        URL = 'http://3.35.246.117:3001/A.fume/api/0.0.1/user/login'
        response = requests.post(URL, {"email": email, "password": password})
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


headers = {'Content-Type': 'application/json; charset=utf-8',
           'x-access-token': ('Bearer ' + Auth.instance().getJWToken())}


def getPerfumeIdx(english_name):
    url = 'http://3.35.246.117:3001/A.fume/api/0.0.1/getPerfumeIdx'
    response = requests.post(url, headers=headers, json={"englishName": english_name})
    if response.status_code / 100 > 2:
        print(response.status_code)
        print(response.text)
        return -1
    return response.json()['data']


def createBrand(english_name):
    name = english_name
    firstInitial = "-"
    description = ""
    imageUrl = ""
    url = 'http://3.35.246.117:3001/A.fume/api/0.0.1/brand'
    response = requests.post(url, headers=headers,
                             json={"name": name, "englishName": english_name, "firstInitial": firstInitial,
                                   "description": description, "imageUrl": imageUrl})
    return response.json()['data']


def getBrandIdx(english_name):
    url = 'http://3.35.246.117:3001/A.fume/api/0.0.1/brand/find'
    response = requests.post(url, headers=headers, json={"englishName": english_name})
    if response.status_code / 100 > 2:
        return createBrand(english_name)
    return response.json()['data']['brandIdx']


if __name__ == '__main__':
    if getPerfumeIdx('154 Cologne') == 1:
        print('success getPerfumeIdx()')
    else:
        print('failed getPerfumeIdx()')
    if getBrandIdx('GALIMARD') == 3:
        print('success getBrandIdx()')
    else:
        print('failed getBrandIdx()')
