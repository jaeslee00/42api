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
        self.filter = kwargs['filters'] if 'filter' in kwargs else {}
        self.page = kwargs['pages'] if 'pages' in kwargs else {'size': 100, 'number': 1}
        self.sort = kwargs['sort'] if 'sort' in kwargs else ''
        # Needs to handle kwargs into different parameters

    def ParseParam(self)
        if self.filter:
            filtering = '&'.join([f'filter[{key}]={value}' for key, value in self.filter.items()])
        else:
            filtering = ''
        if self.pagination:
            pagination = '&'.join([f'page[{key}]={value}' for key, value in self.page.items()])
        else:
            pagination = ''
        parsed_param = filtering + pagination
        if self.sort:
            parsed_param += f'&sort={self.sort}'
        else:
            parsed_param += f'sort={self.sort}'
        
        
        

    def Get(self):
        # resp = self.session.get()
        resp.raise_for_status()
        

    def Put(self, data):
        # resp = self.session.put()
        resp.raise_for_status()
        pass
    def Post(self, data):
        # resp = self.session.post()
        resp.raise_for_status()
        pass

    def PATCH(self, data):
        # resp = self.session.patch()
        resp.raise_for_status()
        pass

    def DELETE(self):
        # resp = self.session.delete()
        resp.raise_for_status()
        pass

