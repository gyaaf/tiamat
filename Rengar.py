#importando as bibliotecas necessárias do programa

import psutil
import requests
import base64
import json
import urllib3
from time import sleep

urllib3.disable_warnings()


def find_league_client_credentials():
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        if proc.info['name'] == 'LeagueClientUx.exe':
            cmdline = proc.info['cmdline']
            port = None
            token = None
            for arg in cmdline:
                if arg.startswith('--app-port='):
                    port = arg.split('=')[1]
                elif arg.startswith('--remoting-auth-token='):
                    token = arg.split('=')[1]
            if port and token:
                return port, token
    return None, None

def check_league_client():
    while True:
        port_check, token_check = find_league_client_credentials()
        if port_check == None and token_check == None:
            sleep(2)
            continue
        else:
            break


def find_riot_client_credentials():
    port = None
    token = None
    for process in psutil.process_iter(attrs=['pid', 'name', 'cmdline']):
        if 'LeagueClientUx' in process.info['name']:
            for arg in process.info['cmdline']:
                if '--riotclient-auth-token=' in arg:
                    token = arg.split('=')[1]
                if '--riotclient-app-port=' in arg:
                    port = arg.split('=')[1]
            if token and port:
                break
    return port, token


def return_lcu_url(leaguePort):
    url = f'https://127.0.0.1:{str(leaguePort)}'
    return str(url)


def return_riot_url(riotPort):
    url = f'https://127.0.0.1:{riotPort}'
    return url


def return_riot_headers(riotToken):
    auth = base64.b64encode(f'riot:{riotToken}'.encode('utf-8')).decode('utf-8')
    headers = {
        'Authorization': f'Basic {auth}',
        'Content-Type': 'application/json'
    }
    return headers


def return_lcu_headers(leagueToken):
    auth = base64.b64encode(f'riot:{leagueToken}'.encode('utf-8')).decode('utf-8')
    headers = {
        'Authorization': f'Basic {auth}',
        'Content-Type': 'application/json'
    }
    return headers


class Rengar:
    def __init__(self):
        self.leaguePort, self.leagueToken = find_league_client_credentials()
        self.leagueUrl = return_lcu_url(self.leaguePort)
        self.leagueHeaders = return_lcu_headers(self.leagueToken)

        self.riotPort, self.riotToken = find_riot_client_credentials()
        self.riotUrl = return_riot_url(self.riotPort)
        self.riotHeaders = return_riot_headers(self.riotToken)

    def return_lcu_creds(self):
        return self.leaguePort, self.leagueToken, self.leagueUrl

    def return_riot_creds(self):
        return self.riotPort, self.riotToken, self.riotUrl

    def lcu_request(self, method, endpoint, body: dict):
        method = method.upper()
        url = f'{self.leagueUrl}{endpoint}'
        if body == "":
            body = None

        if body is not None:
            body = json.dumps(body)

        if method == "GET":
            req = requests.get(url, headers=self.leagueHeaders, data=body, verify=False)
        elif method == "POST":
            req = requests.post(url, headers=self.leagueHeaders, data=body, verify=False)
        elif method == "PUT":
            req = requests.put(url, headers=self.leagueHeaders, data=body, verify=False)
        elif method == "DELETE":
            req = requests.delete(url, headers=self.leagueHeaders, data=body, verify=False)
        elif method == "PATCH":
            req = requests.patch(url, headers=self.leagueHeaders, data=body, verify=False)
        else:
            raise ValueError('Invalid method')

        return req

    def riot_request(self, method, endpoint, body: dict):
        method = method.upper()
        url = f'{self.riotUrl}{endpoint}'
        if body == "":
            body = None
        
        if body is not None:
            body = json.dumps(body)

        if method == "GET":
            req = requests.get(url, headers=self.riotHeaders, data=body, verify=False)
        elif method == "POST":
            req = requests.post(url, headers=self.riotHeaders, data=body, verify=False)
        elif method == "PUT":
            req = requests.put(url, headers=self.riotHeaders, data=body, verify=False)
        elif method == "DELETE":
            req = requests.delete(url, headers=self.riotHeaders, data=body, verify=False)
        elif method == "PATCH":
            req = requests.patch(url, headers=self.riotHeaders, data=body, verify=False)
        else:
            raise ValueError('Invalid method')

        return req
