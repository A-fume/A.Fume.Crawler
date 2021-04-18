import requests
from Auth import Auth


def create_brand(english_name):
    name = english_name
    firstInitial = "-"
    description = ""
    imageUrl = ""
    response = Auth.instance().request(requests.post, url='/brand',
                                       json={"name": name, "englishName": english_name, "firstInitial": firstInitial,
                                             "description": description, "imageUrl": imageUrl})
    return response.json()['data']


def get_brand_idx(english_name):
    response = Auth.instance().request(requests.post, url='/brand/find',
                                       json={"englishName": english_name})
    if response.status_code / 100 > 2:
        return create_brand(english_name)
    return response.json()['data']['brandIdx']


if __name__ == '__main__':
    from dotenv import load_dotenv
    import os

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    load_dotenv(dotenv_path=os.path.join(BASE_DIR, '../../.env'), verbose=True)
    
    if get_brand_idx('GALIMARD') == 3:
        print('success getBrandIdx()')
    else:
        print('failed getBrandIdx()')
