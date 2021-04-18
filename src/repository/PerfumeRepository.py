import requests
from Auth import Auth


def get_perfume_idx(english_name):
    response = Auth.instance().request(requests.post, url='/getPerfumeIdx', json={"englishName": english_name})
    if response.status_code / 100 > 2:
        print(response.status_code)
        print(response.text)
        return -1
    return response.json()['data']


if __name__ == '__main__':
    from dotenv import load_dotenv
    import os

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    load_dotenv(dotenv_path=os.path.join(BASE_DIR, '../../.env'), verbose=True)

    if get_perfume_idx('154 Cologne') == 1:
        print('success getPerfumeIdx()')
    else:
        print('failed getPerfumeIdx()')
