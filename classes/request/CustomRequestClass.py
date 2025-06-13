import sys
import requests # type: ignore

class CustomRequestClass():
    '''
    Classe permettant de généraliser les requêtes vers internet
    '''
    def __init__(self):
        pass
    def getRequest(self, url : str, data : str = None) -> str:
        try:
            r = requests.get(url, params=data)
            r.raise_for_status
            return r.text
        except requests.exceptions.HTTPError as err:
            print(err.request.url)
            print(err)
            print(err.response.text)
            sys.exit(1)
    def postRequest(self, url : str, data : str = None) -> str:
        try:
            r = requests.post(url, params=data)
            r.raise_for_status
            return r.text
        except requests.exceptions.HTTPError as err:
            print(err.request.url)
            print(err)
            print(err.response.text)
            sys.exit(1)
    def deleteRequest(self, url : str, data : str = None) -> str:
        try:
            r = requests.delete(url, params=data)
            r.raise_for_status
            return r.text
        except requests.exceptions.HTTPError as err:
            print(err.request.url)
            print(err)
            print(err.response.text)
            sys.exit(1)
        