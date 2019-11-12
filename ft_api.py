import socket
import requests as req
import sys
import json
from getopt import gnu_getopt as getopt

HOST = 'localhost'
PORT = 9090
REDIR_URI = f'{HOST}:{PORT}'
ENDPOINT = 'https://api.intra.42.fr/'

CAMPUS = '1' # 1 = France 2 = USA .... x = KOREA

POST, PUT, GET, PATCH, DELETE = (
    'POST', 'PUT', 'GET', 'PATCH', 'DELETE'
)



def get_code(uid:str, secret:str):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        print("Hit the 'try this url' button!")
        s.listen()
        connection, address = s.accept()
        with connection:
            print('Connected by', address)
            data = connection.recv(128)
            if not data:
                return None
            else:
                return (str(data).split(' ')[1][7:])

class FT_API(object):
    
    def __init__(self, uid:str, secret:str, req_code:str=None, redirect:str=None, token:str=None):
        self.uid = uid
        self.secret = secret
        self.req_code = req_code
        self.__token = token
        self.redirect = redirect
        if self.__token == None:
            try:
                self.__token = self.Authenticate()
            except Exception as e:
                raise Exception(e)
        self.session = req.Session()
        self.session.headers.update({'Authorization': f'Bearer {self.__token}'})

    def Authenticate(self):
        if self.req_code:
            auth_data = {
                            'grant_type':'authorization_code',
                            'client_id': self.uid,
                            'client_secret': self.secret,
                            'code': self.req_code,
                            'redirect_uri':self.redirect    
                        }
        else:
            auth_data = {
                            'grant_type':'client_credentials',
                            'client_id': self.uid,
                            'client_secret': self.secret
                        }

        resp = req.post("https://api.intra.42.fr/oauth/token", data=auth_data)
        resp.raise_for_status()
        parsed_resp = resp.json()
        print(parsed_resp['access_token'])
        print(parsed_resp['expires_in'])
        return (parsed_resp['access_token'])

    def api_example(self, id=None, **kwargs):
        return HttpRequest(target, self.session, **kwargs)

def main():
    uid = None
    secret = None
    redir_uri = None
    req_code = None
    uid = input("UID = ")
    secret = input("42SECRET = ")
    if uid is None or secret is None:
         sys.exit()
    user = input("are you 'anonymous' or 'authenticated' user? > ")
    if user != 'authenticated':
        if user != 'anonymous':
            print("wrong user input")
            sys.exit()
    if user == 'authenticated':
        print("Please log-in to intranet and send request to 'REDIRECT URI' in your api setting")
        redir_uri = input("REDIRECTION_URI = ")
        req_code = get_code(uid, secret)
        print("your req_code is", req_code)
    api = FT_API(uid, secret, req_code, redir_uri)
    print("auth successfullly finished")
    
    
    """
    curl -F grant_type=authorization_code -F client_id=uid -F client_secret=secret \
    -F code=request_code -F redirect_uri=http://localhost:9090 \
    -X POST https://api.intra.42.fr/oauth/token
    """

if __name__ == '__main__':
    main()