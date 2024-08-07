import hashlib
import logging
import requests
import time
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
    "get-all-access-media-groups": "/accessMediaGroups/getAll",
    "insert-internal": "/users/internal/insert",
    "update-internal": "/users/internal/update",
    "insert-visitor": "/users/visitor/insert",
    "insert-business": "/users/business/insert",
    "get-page-access-media": "/accessMedias/getPage",
    "get-page-by-filter-access-media": "/accessMedias/getPageByFilter",
    "insert-access-media": "/accessMedias/insert",
    "update-access-media": "/accessMedias/update",
    "delete-access-media": "/accessMedias/delete",
    "unlink-access-media": "/accessMedias/unlink",
    "enable-access-media": "/accessMedias/enable",
    "disable-access-media": "/accessMedias/disable",
    "update-balance-access-media": "/accessMedias/updateBalance",
    "get-page-by-states-visit": "/visits/getPageByStates",
    "get-by-key-visit": "/visits/getByKey",
    "insert-visit": "/visits/insert",
    "delete-visit": "/visits/delete",
    "open-visit": "/visits/open",
    "close-visit": "/visits/close",
    "get-page-presence": "/presence/getPage",
    "get-page-for-emergency-points": "/presence/getPageForEmergencyPoints",
}


# --- AUXILIARY FUNCTIONS ---
def validity_end(start):
    # Convert start to a datetime object
    start_datetime = datetime.fromtimestamp(start)

    # Get the end time, which is 23:59:59 of the same day
    end_datetime = start_datetime.replace(hour=23, minute=59, second=59, microsecond=0)

    # Optionally, if you want end as a timestamp
    end = end_datetime.timestamp()

    return end


def hash_md5(text, to_upper=False):
    result = hashlib.md5(text.encode()).hexdigest()
    if to_upper:
        return result.upper()
    return result


def auth_header_json(token):
    header = {
        'Content-Type': 'application/json',
        'fio-access-token': token
    }
    return header


def auth_header(token):
    header = {
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

    # Login to Keydom
    def login(self):
        api_url = url_builder("login")
        data = {
            'username': self.USERNAME,
            'passwordHash': self.PASSWORDHASH
        }
        logging.info(api_url)
        logging.info(data)

        try:
            response = requests.post(api_url, data=data, verify=False)
            self.token = response.json()["data"]["token"]
            self.obj_details(self.login.__name__)   # Print the object details
            logging.info(response.json())
            logging.info("Token: %s", self.token)
        except requests.exceptions.RequestException as e:
            logging.error(e)
            return {"error": True, "date": datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), "message": "Exception", "data": str(e)}

        check_response(response, "Logged in", "Login failed")

        return True

    # Logout from Keydom
    def logout(self):
        api_url = url_builder("logout")
        logging.info(api_url)

        try:
            response = requests.post(api_url, headers=auth_header(self.token), verify=False)
            self.obj_details(self.logout.__name__)   # Print the object details
            logging.info(response.json())
            logging.info("Response: %s", response.text)
        except requests.exceptions.RequestException as e:
            logging.error(e)
            return {"error": True, "date": datetime.now().strftime("%m/%d/%Y"), "time": datetime.now().strftime("%H:%M:%S"), "message": "Exception", "data": str(e)}

        check_response(response, "Logged out", "Logout failed")

        return True

    # Check if the Keydom authentication token is valid
    def is_valid(self):
        api_url = url_builder("get-all-access-bands")

        try:
            response = requests.get(api_url, headers=auth_header(self.token), verify=False)
            self.obj_details(self.is_valid.__name__)   # Print the object details
        except requests.exceptions.RequestException as e:
            logging.error(e)
            return {"error": True, "date": datetime.now().strftime("%m/%d/%Y"), "time": datetime.now().strftime("%H:%M:%S"), "message": "Exception", "data": str(e)}

        check_response(response)

        return True


    # --- VISITORS ---

    # Insert a new internal user
    def insert_internal(self, uuid=None, first_name="Utente", last_name="Anonimo", qualification="Internal", registration_number=None, address=None, phone=None, mobile=None, email=None, notes=None, return_type="uuid"):
        self.login()

        api_url = url_builder("insert-internal")
        data = {
            "uuid": uuid,
            "firstName": first_name,
            "lastName": last_name,
            "qualification": qualification,
            "registrationNumber": registration_number,
            "address": address,
            "phone": phone,
            "mobile": mobile,
            "email": email,
            "notes": notes
        }

        logging.info(api_url)
        logging.info(data)

        try:
            response = requests.post(api_url, headers=auth_header(self.token), json=data, verify=False)
            self.obj_details(self.insert_internal.__name__)   # Print the object details
        except requests.exceptions.RequestException as e:
            logging.error(e)
            return {"error": True, "date": datetime.now().strftime("%m/%d/%Y"), "time": datetime.now().strftime("%H:%M:%S"), "message": "Exception", "data": str(e)}
        
        check_response(response)

        self.logout()

        if response.status_code == 200:
            logging.info(response.json())
        else:
            return False

        if return_type == "uuid":
            return response.json()["data"]["uuid"]
        elif return_type == "json":
            return response.json()

        return True


    # Update an existing internal user
    def update_internal(self, uuid, first_name, last_name, qualification="Internal", registration_number=None, address=None, phone=None, mobile=None, email=None, notes=None):
        self.login()

        api_url = url_builder("update-internal")
        data = {
            "uuid": uuid,
            "firstName": first_name,
            "lastName": last_name,
            "qualification": qualification,
            "registrationNumber": registration_number,
            "address": address,
            "phone": phone,
            "mobile": mobile,
            "email": email,
            "notes": notes
        }

        logging.info(api_url)
        logging.info(data)

        try:
            response = requests.put(api_url, headers=auth_header(self.token), json=data, verify=False)
            self.obj_details(self.update_internal.__name__)   # Print the object details
        except requests.exceptions.RequestException as e:
            logging.error(e)
            return {"error": True, "date": datetime.now().strftime("%m/%d/%Y"), "time": datetime.now().strftime("%H:%M:%S"), "message": "Exception", "data": str(e)}
        
        check_response(response)

        self.logout()

        if response.status_code == 200:
            logging.info(response.json())
        else:
            return False

        return True


    # Insert a new visitor
    def insert_visitor(self, uuid=None, first_name="Utente", last_name="Anonimo", qualification="External", registration_number="0000000", address="", phone="", mobile="", email="", document_number="0000000", return_type="uuid"):
        self.login()

        api_url = url_builder("insert-visitor")
        data = {
            "uuid": uuid,
            "firstName": first_name,
            "lastName": last_name,
            "qualification": qualification,
            "registrationNumber": registration_number,
            "address": address,
            "phone": phone,
            "mobile": mobile,
            "email": email,
            "documentNumber": document_number
        }

        logging.info(api_url)
        logging.info(data)

        try:
            response = requests.post(api_url, headers=auth_header(self.token), json=data, verify=False)
            self.obj_details(self.insert_visitor.__name__)   # Print the object details
        except requests.exceptions.RequestException as e:
            logging.error(e)
            return {"error": True, "date": datetime.now().strftime("%m/%d/%Y"), "time": datetime.now().strftime("%H:%M:%S"), "message": "Exception", "data": str(e)}
        
        check_response(response)

        self.logout()

        if response.status_code == 200:
            logging.info(response.json())
        else:
            return False

        if return_type == "uuid":
            return response.json()["data"]["uuid"]
        elif return_type == "json":
            return response.json()

        return True


    # Insert a new business user
    def insert_business(self, uuid=None, name="Business", address=None, phone=None, mobile=None, email=None, notes=None, return_type="uuid"):
        self.login()

        api_url = url_builder("insert-business")
        data = {
            "uuid": uuid,
            "name": name,
            "address": address,
            "phone": phone,
            "mobile": mobile,
            "email": email,
            "notes": notes
        }

        logging.info(api_url)
        logging.info(data)

        try:
            response = requests.post(api_url, headers=auth_header(self.token), json=data, verify=False)
            self.obj_details(self.insert_business.__name__)   # Print the object details
        except requests.exceptions.RequestException as e:
            logging.error(e)
            return {"error": True, "date": datetime.now().strftime("%m/%d/%Y"), "time": datetime.now().strftime("%H:%M:%S"), "message": "Exception", "data": str(e)}
        
        check_response(response)

        self.logout()

        if response.status_code == 200:
            logging.info(response.json())
        else:
            return False

        if return_type == "uuid":
            return response.json()["data"]["uuid"]
        elif return_type == "json":
            return response.json()

        return True


    # --- ACCESS MEDIAS ---

    # Insert a new badge
    def insert_access_media(self, identifier, uuid=None, mediaTypeCode=0, number=None, enabled=True, validityStart=time.time(), validityEnd=validity_end(time.time()), validityMode=0, antipassbackEnabled=True, countingEnabled=True, userUuid=None, profileUuidOrName=None, lifeCycleMode=0, relatedAccessMediaNumber=None):
        self.login()

        api_url = url_builder("insert-access-media")
        data = {
            "uuid": uuid,
            "identifier": identifier,
            "mediaTypeCode": mediaTypeCode,
            "number": number,
            "enabled": enabled,
            "validityStart": validityStart,
            "validityEnd": validityEnd,
            "validityMode": validityMode,
            "antipassbackEnabled": antipassbackEnabled,
            "countingEnabled": countingEnabled,
            "userUuid": userUuid,
            "profileUuidOrName": profileUuidOrName,
            "lifeCycleMode": lifeCycleMode,
            "relatedAccessMediaNumber": relatedAccessMediaNumber
        }

        logging.info(api_url)
        logging.info(data)

        try:
            response = requests.post(api_url, headers=auth_header(self.token), json=data, verify=False)
            self.obj_details(self.insert_access_media.__name__)   # Print the object details
        except Exception as e:
            return {"error": True, "date": datetime.now().strftime("%m/%d/%Y"), "time": datetime.now().strftime("%H:%M:%S"), "message": "Exception", "data": str(e)}

        check_response(response)

        self.logout()

        if response.status_code == 200:
            logging.info(response.json())
            return response.json()
        elif response.status_code == 400:
            logging.error(response.json())
            return response.json()

        return False


    # Update an existing badge
    def update_access_media(self, uuid, identifier, mediaTypeCode=0, enabled=True, validityStart=time.time(), validityEnd=validity_end(time.time()), validityMode=0, antipassbackEnabled=True, countingEnabled=True, userUuid=None, profileUuidOrName=None, lifeCycleMode=0):
        self.login()

        api_url = url_builder("update-access-media")
        data = {
            "uuid": uuid,
            "identifier": identifier,
            "mediaTypeCode": mediaTypeCode,
            "enabled": enabled,
            "validityStart": validityStart,
            "validityEnd": validityEnd,
            "validityMode": validityMode,
            "antipassbackEnabled": antipassbackEnabled,
            "countingEnabled": countingEnabled,
            "userUuid": userUuid,
            "profileUuidOrName": profileUuidOrName,
            "lifeCycleMode": lifeCycleMode
        }

        logging.info(api_url)
        logging.info(data)

        try:
            response = requests.put(api_url, headers=auth_header(self.token), json=data, verify=False)
            self.obj_details(self.update_access_media.__name__)   # Print the object details
        except Exception as e:
            return {"error": True, "date": datetime.now().strftime("%m/%d/%Y"), "time": datetime.now().strftime("%H:%M:%S"), "message": "Exception", "data": str(e)}

        check_response(response)

        self.logout()

        if response.status_code == 200:
            logging.info(response.json())
            return response.json()

        return False


    # Enable a badge
    def enable_access_media(self, uuid):
        self.login()

        api_url = url_builder("enable-access-media")
        data = {
            "uuid": uuid
        }

        logging.info(api_url)
        logging.info(data)

        try:
            response = requests.put(api_url, headers=auth_header(self.token), data=data, verify=False)
            self.obj_details(self.enable_access_media.__name__)   # Print the object details
        except requests.exceptions.RequestException as e:
            logging.error(e)
            return {"error": True, "date": datetime.now().strftime("%m/%d/%Y"), "time": datetime.now().strftime("%H:%M:%S"), "message": "Exception", "data": str(e)}
        
        check_response(response)

        self.logout()

        if response.status_code == 200:
            logging.info(response.json())
        else:
            return False

        return True


    # Disable a badge
    def disable_access_media(self, uuid):
        self.login()

        api_url = url_builder("disable-access-media")
        data = {
            "uuid": uuid
        }

        logging.info(api_url)
        logging.info(data)

        try:
            response = requests.put(api_url, headers=auth_header(self.token), data=data, verify=False)
            self.obj_details(self.disable_access_media.__name__)   # Print the object details
        except requests.exceptions.RequestException as e:
            logging.error(e)
            return {"error": True, "date": datetime.now().strftime("%m/%d/%Y"), "time": datetime.now().strftime("%H:%M:%S"), "message": "Exception", "data": str(e)}
        
        check_response(response)

        self.logout()

        if response.status_code == 200:
            logging.info(response.json())
        else:
            return False

        return True


    # Unlink a badge from a user
    def unlink_access_media(self, id_badge):
        self.login()

        api_url = url_builder("unlink-access-media")
        data = {
            "uuid": id_badge
        }

        logging.info(api_url)
        logging.info(data)

        try:
            response = requests.put(api_url, headers=auth_header(self.token), data=data, verify=False)
            self.obj_details(self.unlink_access_media.__name__)   # Print the object details
        except requests.exceptions.RequestException as e:
            logging.error(e)
            return {"error": True, "date": datetime.now().strftime("%m/%d/%Y"), "time": datetime.now().strftime("%H:%M:%S"), "message": "Exception", "data": str(e)}

        check_response(response, "Badge reset", "Badge reset failed")

        self.logout()

        if response.status_code == 200:
            logging.info(response.json())
        else:
            return False

        return True


    # Get uuid of a badge starting from the badge number
    def get_access_media_uuid(self, badge_number):
        self.login()

        api_url = url_builder("get-page-by-filter-access-media")
        data = {
            "pageIndex": 0,
            "pageSize": 1,
            "numberFilterPattern": str(badge_number)
        }

        logging.info(api_url)
        logging.info(data)

        try:
            response = requests.post(api_url, headers=auth_header(self.token), json=data, verify=False)
            self.obj_details(self.get_access_media_uuid.__name__)   # Print the object details
        except requests.exceptions.RequestException as e:
            logging.error(e)
            return {"error": True, "date": datetime.now().strftime("%m/%d/%Y"), "time": datetime.now().strftime("%H:%M:%S"), "message": "Exception", "data": str(e)}

        check_response(response)

        self.logout()

        if response.status_code == 200:
            logging.info(response.json())
        else:
            return False

        return response.json()["data"][0]["uuid"]


    # Get identifier of a badge starting from the badge number
    def get_access_media_identifier(self, badge_number):
        self.login()

        api_url = url_builder("get-page-by-filter-access-media")
        data = {
            "pageIndex": 0,
            "pageSize": 1,
            "numberFilterPattern": str(badge_number)
            }
        logging.info(api_url)
        logging.info(data)

        try:
            response = requests.post(api_url, headers=auth_header(self.token), json=data, verify=False)
            self.obj_details(self.get_access_media_uuid.__name__)   # Print the object details
            logging.info(response.json())
        except requests.exceptions.RequestException as e:
            logging.error(e)
            return {"error": True, "date": datetime.now().strftime("%m/%d/%Y"), "time": datetime.now().strftime("%H:%M:%S"), "message": "Exception", "data": str(e)}

        check_response(response)

        self.logout()

        return response.json()["data"][0]["identifier"]


    # Update the balance of a badge
    def update_balance_access_media(self, uuid, balance):
        self.login()

        api_url = url_builder("update-balance-access-media")
        data = {
            "uuid": uuid,
            "balance": balance
        }

        logging.info(api_url)
        logging.info(data)

        try:
            response = requests.put(api_url, headers=auth_header(self.token), json=data, verify=False)
            self.obj_details(self.update_balance_access_media.__name__)   # Print the object details
        except requests.exceptions.RequestException as e:
            logging.error(e)
            return {"error": True, "date": datetime.now().strftime("%m/%d/%Y"), "time": datetime.now().strftime("%H:%M:%S"), "message": "Exception", "data": str(e)}

        check_response(response)

        self.logout()

        if response.status_code == 200:
            logging.info(response.json())
        else:
            return False

        return True


    # --- VISITS ---

    def get_visits(self, states=[0], page_index=0, page_size=10):
        self.login()

        api_url = url_builder("get-page-by-states-visit")
        data = {
            "visitStates": states,
            "pageIndex": page_index,
            "pageSize": page_size
        }

        logging.info(api_url)
        logging.info(data)

        try:
            response = requests.get(api_url, headers=auth_header(self.token), json=data, verify=False)
            self.obj_details(self.get_created_visits.__name__)   # Print the object details
        except requests.exceptions.RequestException as e:
            logging.error(e)
            return {"error": True, "date": datetime.now().strftime("%m/%d/%Y"), "time": datetime.now().strftime("%H:%M:%S"), "message": "Exception", "data": str(e)}

        check_response(response)

        self.logout()

        if response.status_code == 200:
            logging.info(response.json())
        else:
            return False

        return response.json()

    # Get the list of created visits
    def get_created_visits(self, page_index=0, page_size=10):
        return self.get_visits(states=[0], page_index=page_index, page_size=page_size)

    # Get the list of in-progress visits
    def get_in_progress_visits(self, page_index=0, page_size=10):
        return self.get_visits(states=[1], page_index=page_index, page_size=page_size)

    # Get the list of completed visits
    def get_completed_visits(self, page_index=0, page_size=10):
        return self.get_visits(states=[2], page_index=page_index, page_size=page_size)

    # Get the list of all visits
    def get_all_visits(self, page_index=0, page_size=10):
        return self.get_visits(states=[0, 1, 2], page_index=page_index, page_size=page_size)


    # Get the details of a visit
    def get_visit_details(self, key):
        self.login()

        api_url = url_builder("get-by-key-visit")
        data = {
            "key": key
        }

        logging.info(api_url)
        logging.info(data)

        try:
            response = requests.post(api_url, headers=auth_header(self.token), json=data, verify=False)
            self.obj_details(self.get_visit_details.__name__)   # Print the object details
        except requests.exceptions.RequestException as e:
            logging.error(e)
            return {"error": True, "date": datetime.now().strftime("%m/%d/%Y"), "time": datetime.now().strftime("%H:%M:%S"), "message": "Exception", "data": str(e)}

        check_response(response)

        self.logout()

        if response.status_code == 200:
            logging.info(response.json())
        else:
            return False

        return response.json()


    # Insert a new visit
    def insert_visit(self, userUuid, uuid=None, start=time.time(), end=validity_end(time.time()), field1=None, field2=None, field3=None, notes=None, preVisitAccessMediaType=None, preVisitAccessMediaIdentifier=None, preVisitProfileUuid=None, visitFirstAccessMediaType=None, visitFirstAccessMediaIdentifier=None, visitFirstAccessMediaNumber=None, visitFirstProfileUuid=None, visitSecondAccessMediaType=None, visitSecondAccessMediaIdentifier=None, visitSecondAccessMediaNumber=None, visitSecondProfileUuid=None, visitThirdAccessMediaType=None, visitThirdAccessMediaIdentifier=None, visitThirdAccessMediaNumber=None, visitThirdProfileUuid=None, relatedUserUuid=None, openVisitNow=True, return_type="key"):
        self.login()

        api_url = url_builder("insert-visit")
        data = {
            "uuid": uuid,
            "userUuid": userUuid,
            "initialTimestamp": start,
            "finalTimestamp": end,
            "field1": field1,
            "field2": field2,
            "field3": field3,
            "notes": notes,
            "preVisitAccessMediaType": preVisitAccessMediaType,
            "preVisitAccessMediaIdentifier": preVisitAccessMediaIdentifier,
            "preVisitProfileUuid": preVisitProfileUuid,
            "visitFirstAccessMediaType": visitFirstAccessMediaType,
            "visitFirstAccessMediaIdentifier": visitFirstAccessMediaIdentifier,
            "visitFirstAccessMediaNumber": visitFirstAccessMediaNumber,
            "visitFirstProfileUuid": visitFirstProfileUuid,
            "visitSecondAccessMediaType": visitSecondAccessMediaType,
            "visitSecondAccessMediaIdentifier": visitSecondAccessMediaIdentifier,
            "visitSecondAccessMediaNumber": visitSecondAccessMediaNumber,
            "visitSecondProfileUuid": visitSecondProfileUuid,
            "visitThirdAccessMediaType": visitThirdAccessMediaType,
            "visitThirdAccessMediaIdentifier": visitThirdAccessMediaIdentifier,
            "visitThirdAccessMediaNumber": visitThirdAccessMediaNumber,
            "visitThirdProfileUuid": visitThirdProfileUuid,
            "relatedUserUuid": relatedUserUuid,
            "openVisitNow": openVisitNow
        }

        logging.info(api_url)
        logging.info(data)

        try:
            response = requests.post(api_url, headers=auth_header(self.token), json=data, verify=False)
            self.obj_details(self.insert_visit.__name__)   # Print the object details
        except requests.exceptions.RequestException as e:
            logging.error(e)
            return {"error": True, "date": datetime.now().strftime("%m/%d/%Y"), "time": datetime.now().strftime("%H:%M:%S"), "message": "Exception", "data": str(e)}

        check_response(response)

        self.logout()

        if response.status_code == 200:
            logging.info(response.json())
        else:
            return False

        if return_type == "key":
            return response.json()["data"]["key"]
        elif return_type == "json":
            return response.json()

        return True


    # Delete a visit
    def delete_visit(self, key):
        self.login()

        api_url = url_builder("delete-visit")
        data = {
            "uuid": key
        }

        logging.info(api_url)
        logging.info(data)

        try:
            response = requests.delete(api_url, headers=auth_header(self.token), params=data, verify=False)
            self.obj_details(self.delete_visit.__name__)   # Print the object details
        except requests.exceptions.RequestException as e:
            logging.error(e)
            return {"error": True, "date": datetime.now().strftime("%m/%d/%Y"), "time": datetime.now().strftime("%H:%M:%S"), "message": "Exception", "data": str(e)}

        check_response(response)

        self.logout()

        if response.status_code == 200:
            logging.info(response.json())
        else:
            return False

        return True


    # Open a visit
    def open_visit(self, key):
        self.login()

        api_url = url_builder("open-visit")
        data = {
            "uuid": key
        }

        logging.info(api_url)
        logging.info(data)

        try:
            response = requests.post(api_url, headers=auth_header(self.token), json=data, verify=False)
            self.obj_details(self.open_visit.__name__)   # Print the object details
        except requests.exceptions.RequestException as e:
            logging.error(e)
            return {"error": True, "date": datetime.now().strftime("%m/%d/%Y"), "time": datetime.now().strftime("%H:%M:%S"), "message": "Exception", "data": str(e)}

        check_response(response)

        self.logout()

        if response.status_code == 200:
            logging.info(response.json())
        else:
            return False

        return True


    # Close a visit
    def close_visit(self, key):
        self.login()

        api_url = url_builder("close-visit")
        data = {
            "uuid": key
        }

        logging.info(api_url)
        logging.info(data)

        try:
            response = requests.post(api_url, headers=auth_header(self.token), json=data, verify=False)
            self.obj_details(self.close_visit.__name__)   # Print the object details
        except requests.exceptions.RequestException as e:
            logging.error(e)
            return {"error": True, "date": datetime.now().strftime("%m/%d/%Y"), "time": datetime.now().strftime("%H:%M:%S"), "message": "Exception", "data": str(e)}

        check_response(response)

        self.logout()

        if response.status_code == 200:
            logging.info(response.json())
        else:
            return False

        return True


    # --- PRESENCE ---

    # Get the list of presences
    def get_presences(self, page_index=0, page_size=10):
        self.login()

        api_url = url_builder("get-page-presence")
        data = {
            "pageIndex": page_index,
            "pageSize": page_size
        }

        logging.info(api_url)
        logging.info(data)

        try:
            response = requests.get(api_url, headers=auth_header(self.token), params=data, verify=False)
            self.obj_details(self.get_presences.__name__)   # Print the object details
        except requests.exceptions.RequestException as e:
            logging.error(e)
            return {"error": True, "date": datetime.now().strftime("%m/%d/%Y"), "time": datetime.now().strftime("%H:%M:%S"), "message": "Exception", "data": str(e)}

        check_response(response)

        self.logout()

        if response.status_code == 200:
            logging.info(response.json())
        else:
            return False

        return response.json()


    # Get the list of presences for emergency points
    def get_presences_emergency_points(self, page_index=0, page_size=10):
        self.login()

        api_url = url_builder("get-page-for-emergency-points")
        data = {
            "pageIndex": page_index,
            "pageSize": page_size
        }

        logging.info(api_url)
        logging.info(data)

        try:
            response = requests.get(api_url, headers=auth_header(self.token), params=data, verify=False)
            self.obj_details(self.get_presences_emergency_points.__name__)   # Print the object details
        except requests.exceptions.RequestException as e:
            logging.error(e)
            return {"error": True, "date": datetime.now().strftime("%m/%d/%Y"), "time": datetime.now().strftime("%H:%M:%S"), "message": "Exception", "data": str(e)}

        check_response(response)

        self.logout()

        if response.status_code == 200:
            logging.info(response.json())
        else:
            return False

        return response.json()