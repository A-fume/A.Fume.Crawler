import requests
from src.repository.Auth import Auth


def create_note(perfume_idx, ingredient_idx, note_type):
    response = Auth.instance().request(requests.post, url='/note',
                                       json={"perfumeIdx": perfume_idx,
                                             "ingredientIdx": ingredient_idx,
                                             "type": note_type
                                             })
    print(response.text)
    if "중복" in response.text:
        print("중복")
        return update_note(perfume_idx, ingredient_idx, note_type)
    return response.status_code / 100 == 2


def update_note(perfume_idx, ingredient_idx, note_type):
    response = Auth.instance().request(requests.put, url='/note',
                                       json={"perfumeIdx": perfume_idx,
                                             "ingredientIdx": ingredient_idx,
                                             "type": note_type
                                             })
    print(response.text)
    return response.status_code / 100 == 2


if __name__ == '__main__':
    from dotenv import load_dotenv
    import os

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    load_dotenv(dotenv_path=os.path.join(BASE_DIR, '../../.env'), verbose=True)

    if not create_note(1, 1, 4):
        print("fail to create")
