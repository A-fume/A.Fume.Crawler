import requests
import os


class Auth:
    __jwtToken = None

    def __init__(self):
        self.__email = os.getenv('ADMIN_EMAIL')
        self.__password = os.getenv('ADMIN_PWD')
        self.__base_url = os.getenv('A_FUME_API_SERVER')
        if self.__email is None or self.__password is None:
            raise ConnectionError('Please set .env about id and password')

        self.headers = {'Content-Type': 'application/json; charset=utf-8',
                        'x-access-token': ('Bearer ' + self.__get_jwt_token())}
        print(self.__get_jwt_token())

    def __get_jwt_token(self):
        if self.__jwtToken is not None:
            return self.__jwtToken

        url = self.__base_url + '/user/login'
        response = requests.post(url, {"email": self.__email, "password": self.__password})
        if response.status_code / 100 > 2:
            print(response.status_code)
            print(response.text)
            raise ConnectionError('Failed to login')
        return response.json()['data']['token']

    def request(self, func, *args, **kwargs):
        kwargs["url"] = self.__base_url + str(kwargs.get("url"))
        kwargs["headers"] = self.headers
        return func(*args, **kwargs)

    __instance = None

    @classmethod
    def __getInstance(cls):
        return cls.__instance

    @classmethod
    def instance(cls):
        cls.__instance = cls()
        cls.instance = cls.__getInstance
        return cls.__instance


if __name__ == '__main__':
    from dotenv import load_dotenv

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    load_dotenv(dotenv_path=os.path.join(BASE_DIR, '../../.env'), verbose=True)

    if Auth.instance() != Auth.instance():
        print("Not supported Singleton")
