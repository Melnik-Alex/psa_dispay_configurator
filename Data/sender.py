# importing the requests library
import requests
import uuid
import hashlib
import json

# defining the api-endpoint
API_ENDPOINT = "http://62.113.105.77:1234"

# your API key here
VERSION = 'V00011'
USER_ID = str(uuid.getnode())


class Sender():

    def send_data(self, user_id, z0200, z0400, z0500, z0600, z2100):
        data = {
            "userId": USER_ID,
            "username": '12345',
            "zone0200": z0200,
            "zone0400": z0400,
            "zone0500": z0500,
            "zone0600": z0600,
            "zone2100": z2100,
            "zone0f": "",
            "zoneFF": ""
        }
        hash_data = hashlib.md5(json.dumps(data, sort_keys=True).encode('utf-8')).hexdigest()
        # sending post request and saving response as response object
        r = requests.post(url=API_ENDPOINT, json=data)

        # extracting response text
        response = r.json()
        version = response['version']
        response_hash = response['secret']
        print('Recived hash: ', hash_data)
        print('Calculated hash: ', response)
        try:
            assert VERSION == version
            print('Версии совпадают!')
        except:
            print('Версии не совпадают!')
        try:
            assert hash_data == response_hash
            print('Контрольные суммы совпадают!')
        except:
            print('Контрольные суммы не совпадают!')
        return response


if __name__ == "__main__":
    sender = Sender()
    sender.send_data(user_id='laleksss',
                     z0200='qwerнt',
                     z0400='asdfg',
                     z0500='zxcvb',
                     z0600='hjkkjh',
                     z2100='09weuosndls')
