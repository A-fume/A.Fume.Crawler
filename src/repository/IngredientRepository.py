import requests
from Auth import Auth


def create_ingredient(english_name, description, series_idx):
    name = english_name
    image_url = ""
    response = Auth.instance().request(requests.post, url='/ingredient',
                                       json={"name": name, "englishName": english_name, "description": description,
                                             "imageUrl": image_url, "seriesIdx": series_idx})
    print(response)
    return response.json()['data']


def get_ingredient_idx(english_name, description, series_idx):
    response = Auth.instance().request(requests.post, url='/ingredient/find', json={"englishName": english_name})
    if response.status_code / 100 > 2:
        return create_ingredient(english_name, description, series_idx)
    return response.json()['data']['ingredientIdx']


if __name__ == '__main__':
    from dotenv import load_dotenv
    import os

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    load_dotenv(dotenv_path=os.path.join(BASE_DIR, '../../.env'), verbose=True)

    if get_ingredient_idx('Grapefruit', '', 1) == 2:
        print('success getIngredientIdx()')
    else:
        print('failed getIngredientIdx()')
