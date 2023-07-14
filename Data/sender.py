# importing the requests library
import requests
import subprocess
import hashlib
import json
from requests.exceptions import ConnectTimeout

# defining the api-endpoint
server_adress = "http://62.113.105.77:1234"


# your API key here


class Sender():
    version_sw = 'V0001'
    version_key = '.s/f21d31c653#4$#!@(CJ)kd*2!_e49605253bf'
    secret_key = '!;lO)DS!lsdfikLOIn*%&29431-0679823vcxlk11,dn'
    unic_id = str(subprocess.check_output('wmic csproduct get uuid').decode().split('\n')[1].strip())

    def send_data(self, rf080, rf0fe, r0200, r0400, r0500, r0600, r2100, w0200, w0400, w0500, w0600, w2100):
        data = {
            "userId": self.unic_id,
            "w_zoneF080": rf080,
            "w_zoneF0FE": rf0fe,
            "Read": " ",
            "r_zone0200": r0200,
            "r_zone0400": r0400,
            "r_zone0500": r0500,
            "r_zone0600": r0600,
            "r_zone2100": r2100,
            "Wrote": " ",
            "w_zone0200": w0200,
            "w_zone0400": w0400,
            "w_zone0500": w0500,
            "w_zone0600": w0600,
            "w_zone2100": w2100,
        }
        hash_data = hashlib.md5(
            json.dumps(data, sort_keys=True).encode('utf-8') + self.secret_key.encode('utf-8')).hexdigest()
        # sending post request and saving response as response object
        try:
            r = requests.post(url=server_adress, json=data, timeout=5.0)
        except ConnectTimeout:
            return 2

        # extracting response text
        try:
            response = r.json()
            response_hash = response['secret']
            try:
                assert hash_data == response_hash
                return 1
            except:
                return False
        except:
            response = r.text
            return 0

    def check_version(self):
        data = {
            "version": self.version_sw + self.version_key
        }
        version_hash_data = hashlib.md5(
            json.dumps(self.version_sw + self.version_key, sort_keys=True).encode('utf-8')).hexdigest()
        try:
            r = requests.post(url=server_adress, json=data, timeout=5.0)
        except ConnectTimeout:
            return 2
        try:
            response = r.json()
            response_hash = response['secret_ver']
            assert response_hash == version_hash_data
            return 1
        except:
            return 0
