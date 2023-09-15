import hashlib
import requests
from datetime import datetime

import config

ENDPOINTS = {
    "login": "/authentication/login",
    "logout": "/authentication/logout",
    "get-all-devices": "/devices/getAll",
    "get-all-profiles": "/profiles/getAll",
    "get-all-statuses": "/statuses/getForAllDevices",
    "get-all-actions": "/actions/getAll",
    "get-all-counters": "/counters/getAll",
    "get-all-access-bands": "/accessBands/getAll",
    "get-all-access-media-groups": "/accessMediaGroups/getAll"
}


def hash_md5(text, to_upper=False):
    result = hashlib.md5(text.encode()).hexdigest()
    if to_upper:
        return result.upper()
    return result


def auth_header(token):
    header = {
        'Content-Type': 'application/json',
        'fio-access-token': token
    }
    return header


def url_builder(endpoint):
    tail = ENDPOINTS[endpoint]
    return f'{config.protocol}://{config.ip}/keydom/api-external{tail}'


def check_response(response, message1="Token is valid", message2="Token is invalid", message3="Communication with Keydom is down"):
    if type(response) is requests.models.Response:
        print("Response is a requests.models.Response")
        print(type(response))
        print(response.status_code)
        if response.status_code == 200:
            print(message1)
            return {"return": True, "date": datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), "message": message1}
        elif response.status_code == 401:
            print(message2)
            return {"return": False, "date": datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), "message": "Invalid token"}
        elif response.status_code == 404:
            print(message3)
            return {"return": False, "date": datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), "message": "There is no communication with Keydom"}

    return False


class KeydomManager:
    def __init__(self):
        self.USERNAME = config.username
        self.PASSWORD = config.password
        self.PASSWORDHASH = hash_md5(self.PASSWORD, True)

        self.token = None

        self.obj_details(self.__init__.__name__)

    def get_username(self):
        return str(self.USERNAME)

    def get_password(self):
        return str(self.PASSWORD)

    def get_password_hash(self):
        return str(self.PASSWORDHASH)

    def get_token(self):
        return str(self.token)

    def set_username(self, username):
        self.USERNAME = username
        return True

    def set_password(self, password):
        self.PASSWORD = password
        self.PASSWORDHASH = hash_md5(password, True)
        return True

    def set_token(self, token):
        self.token(token)
        return True

    def obj_details(self, method):
        print("METHOD: " + str(method))
        print("--------------------")
        print("username: " + str(self.USERNAME))
        print("password: " + str(self.PASSWORD))
        print("passwordHash: " + str(self.PASSWORDHASH))
        print("token: " + str(self.token))
        print("--------------------")
        print("\n")

    def login(self):
        api_url = url_builder("login")
        data = {
            'username': self.USERNAME,
            'passwordHash': self.PASSWORDHASH
        }

        try:
            response = requests.post(api_url, data=data, verify=False)
            self.token = response.json()["data"]["token"]
            self.obj_details(self.login.__name__)   # Print the object details
        except Exception as e:
            return {"error": True, "date": datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), "message": "Exception", "data": str(e)}

        check_response(response, "Logged in", "Login failed")

        return False

    def logout(self):
        api_url = url_builder("logout")

        try:
            response = requests.post(api_url, headers=auth_header(self.token), verify=False)
            self.obj_details(self.logout.__name__)   # Print the object details
        except Exception as e:
            return {"error": True, "date": datetime.now().strftime("%m/%d/%Y"), "time": datetime.now().strftime("%H:%M:%S"), "message": "Exception", "data": str(e)}

        check_response(response, "Logged out", "Logout failed")

        return False

    def is_valid(self):
        # Check if the authentication token is valid
        api_url = url_builder("get-all-access-bands")

        try:
            response = requests.get(api_url, headers=auth_header(self.token), verify=False)
            self.obj_details(self.is_valid.__name__)   # Print the object details
        except Exception as e:
            return {"error": True, "date": datetime.now().strftime("%m/%d/%Y"), "time": datetime.now().strftime("%H:%M:%S"), "message": "Exception", "data": str(e)}

        check_response(response)

        return False
