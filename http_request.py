import json
import requests as req

ENDPOINT = 'https://api.intra.42.fr/'
POST, PUT, GET, PATCH, DELETE = (
    'POST', 'PUT', 'GET', 'PATCH', 'DELETE'
)

TARGET = '{endpoint}{target}{param}'

class HttpRequest(object):
    def __init__(self, target, session, **kwargs):
        self.url = f"https://api.intra.42.fr/{target}"
        self.session = session
        # Needs to handle kwargs into different parameters

    def ParseParam(self)
        pass

    def Get(self):
        resp = self.session.get(self.url + self.ParseParam())
        resp.raise_for_status()
        

    def Put(self, data):
        # resp = self.session.put()
        pass
    def Post(self, data):
        # resp = self.session.post()
        pass

    def PATCH(self, data):
        # resp = self.session.patch()
        pass

    def DELETE(self):
        # resp = self.session.delete()
        pass

