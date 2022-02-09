import requests
from src.repository.Auth import Auth


def create_series(english_name):
    name = english_name
    description = ""
    image_url = ""

    response = Auth.instance().request(requests.post, url='/series',
                                       json={"name": name, "englishName": english_name, "description": description,
                                             "imageUrl": image_url})
    print(response)
    return response.json()['data']


def get_series_idx(english_name):
    response = Auth.instance().request(requests.post, url='/series/find', json={"englishName": english_name})
    if response.status_code / 100 > 2:
        return create_series(english_name)
    return response.json()['data']['seriesIdx']


if __name__ == '__main__':
    from dotenv import load_dotenv
    import os

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    load_dotenv(dotenv_path=os.path.join(BASE_DIR, '../../.env'), verbose=True)

    if get_series_idx('Floral') == 2:
        print('success getSeriesIdx()')
    else:
        print('failed getSeriesIdx()')
