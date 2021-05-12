import requests
from src.repository.Auth import Auth


def create_perfume(english_name, brand_idx, image_url, story):
    name = english_name
    abundance_rate = "None"
    release_date = "2021-05-09"
    volume_and_price = []
    print({"name": name, "englishName": english_name, "abundanceRate": abundance_rate,
           "volumeAndPrice": volume_and_price,
           "imageUrl": image_url, "brandIdx": brand_idx, "releaseDate": release_date,
           "story": story})
    response = Auth.instance().request(requests.post, url='/perfume',
                                       json={"name": name, "englishName": english_name, "abundanceRate": abundance_rate,
                                             "volumeAndPrice": volume_and_price,
                                             "imageUrl": image_url, "brandIdx": brand_idx, "releaseDate": release_date,
                                             "story": story})
    print(response.text)
    return response.json()['data']


def get_perfume_idx(english_name, brand_idx, image_url, story):
    response = Auth.instance().request(requests.post, url='/getPerfumeIdx', json={"englishName": english_name})
    if response.status_code / 100 > 2:
        return create_perfume(english_name, brand_idx, image_url, story)
    return response.json()['data']


if __name__ == '__main__':
    from dotenv import load_dotenv
    import os

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    load_dotenv(dotenv_path=os.path.join(BASE_DIR, '../../.env'), verbose=True)

    if get_perfume_idx('154 Cologne2', 1, "", "test story") == 1:
        print('success getPerfumeIdx()')
    else:
        print('failed getPerfumeIdx()')
