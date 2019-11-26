import socket
import requests as req
import sys
import json
from getopt import gnu_getopt as getopt
import os

ENDPOINT = 'https://api.intra.42.fr'
HOST = "localhost"
PORT = 9090
REDIR_URI = "http://localhost:9090"

CAMPUS = '1' # 1 = France 2 = USA .... x = KOREA

# def get_code(uid:str, secret:str):
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#         s.bind((HOST, PORT))
#         print("Hit the 'try this url' button!")
#         s.listen()
#         connection, address = s.accept()
#         with connection:
#             print('Connected by', address)
#             data = connection.recv(128)
#             if not data:
#                 return None
#             else:
#                 return (str(data).split(' ')[1][7:])

def auth():
    uid = None
    secret = None
    with open("/Users/jaeslee/auth.txt", 'r') as file:
        uid = file.readline()[0:-1]
        secret = file.readline()[0:-1]
    return uid, secret

class HttpRequest(object):

    def __init__(self, target:str, session, **kwargs):
        self.url = f"{ENDPOINT}{target}"
        self.session = session
        if "filter" in kwargs:
            self.filter = kwargs["filter"]
        else:
            self.filter = {}
        if "page" in kwargs:
            self.page = kwargs["page"]
        else:
            self.page = {"size": 100, "number": 1} #size of page and index of page can be modified
        if "sort" in kwargs:
            self.sort = kwargs["sort"]
        else:
            self.sort = ""
        # Needs to handle kwargs into different parameters
    def parseParams(self):
        if self.filter:
            filtering = '&'.join([f"filter[{key}]={value}" for key, value in self.filter.items()]) + '&'
        else:
            filtering = ""
        if self.page:
            page = '&'.join([f"page[{key}]={value}" for key, value in self.page.items()])
        parsed_param = filtering + page
        if self.sort:
            parsed_param += f"&sort={self.sort}"
        print(parsed_param)
        return f"?{parsed_param}"

    def get(self):
        print("url : " + self.url)
        resp = self.session.get(self.url + self.parseParams())
        resp.raise_for_status()
        return resp.json()

    def put(self, data:json):
       resp = self.session.put(self.url, data=data)
       resp.raise_for_status()
       return resp

    def post(self, data:json):
        resp = self.session.post(self.url, json=data)
        # resp.raise_for_status()
        return resp

    def patch(self, data:json):
        resp = self.session.patch(self.url, data=data)
        resp.raise_for_status()
        return resp

    def delete(self):
        resp = self.session.delete(self.url)
        resp.raise_for_status()
        return resp


class FT_API(object):

    def __init__(self, uid:str, secret:str, req_code:str=None,
                    redirect:str=None, token:str=None):
        self.uid = uid
        self.secret = secret
        self.req_code = req_code
        self.__token = token
        self.redirect = redirect
        if self.__token == None:
            self.__token = self.Authenticate()
        self.session = req.Session()
        self.session.headers.update({"Authorization": f"Bearer {self.__token}"})

    def Authenticate(self):
        if self.req_code:
            auth_data = {
                            "grant_type":"authorization_code",
                            "client_id": self.uid,
                            "client_secret": self.secret,
                            "code": self.req_code,
                            "redirect_uri":self.redirect
                        }
        else:
            auth_data = {
                            "grant_type":"client_credentials",
                            "client_id": self.uid,
                            "client_secret": self.secret
                        }

        resp = req.post("https://api.intra.42.fr/oauth/token", data=auth_data)
        resp.raise_for_status()
        parsed_resp = resp.json()
        print(parsed_resp["access_token"])
        print("expires in:", parsed_resp["expires_in"], "seconds")
        return (parsed_resp["access_token"])

    #######################################################
    #                    users                            #
    #######################################################

    def users(self, user_id:str=None, **kwargs):
        if user_id:
            target = f"/v2/users/{user_id}"
        else:
            target = "/v2/users"
        return HttpRequest(target, self.session, **kwargs)

    def users_exams(self, user_id:str, **kwargs):
        target = f"/v2/users/{user_id}/exams"
        return HttpRequest(target, self.session, **kwargs)

    def users_slots(self, user_id:str, **kwargs):
        target = f"/v2/users/{user_id}/slots"
        return HttpRequest(target, self.session, **kwargs)

    def users_teams(self, user_id:str, **kwargs):
        target = f"/v2/users/{user_id}/teams"
        #return HttpRequest(target, self.session, **kwargs)
        return self.session()

    def users_roles(self, user_id:str, **kwargs):
        target = f"/v2/users/{user_id}/roles"

    def users_titles(self, user_id:str, **kwargs):
        target = f"/v2/users/{user_id}/roles"
        return HttpRequest(target, self.session, **kwargs)

    def users_titlesUsers(self, user_id:str, **kwargs):
        target = f"/v2/users/{user_id}/titles_users"
        return HttpRequest(target, self.session, **kwargs)

    def users_closes(self, user_id:str, **kwargs):
        target = f"/v2/users/{user_id}/closes"
        return HttpRequest(target, self.session, **kwargs)

    def users_groups(self, user_id:str, **kwargs):
        target = f"/v2/users/{user_id}/groups"
        return HttpRequest(target, self.session, **kwargs)

    def users_groupsUsers(self, user_id:str, **kwargs):
        target = f"/v2/users/{user_id}/groups_users"
        return HttpRequest(target, self.session, **kwargs)

    def users_projectsUsers(self, user_id:str, **kwargs):
        target = f"/v2/users/{user_id}/project_users"
        return HttpRequest(target, self.session, **kwargs)

    #######################################################
    #                      cursus                         #
    #######################################################

    def cursus(self, cursus_id:str=None, **kwargs):
        if cursus_id:
            target = f"/v2/cursus/{cursus_id}"
        else:
            target = "/v2/cursus"
        return HttpRequest(target, self.session, **kwargs)

    def cursus_users(self, cursus_id:str, **kwargs):
        target = f"/v2/cursus/{cursus_id}/users"
        return HttpRequest(target, self.session, **kwargs)

    def cursusUsers(self, cursus_user_id:str=None, **kwargs):
        if cursus_user_id:
            target = f"/v2/cursus_users/{cursus_user_id}"
        else:
            target = f"/v2/cursus_users"
        return HttpRequest(target, self.session, **kwargs)

    def cursus_cursusUsers(self, cursus_id:str, **kwargs):
        target = f"/v2/cursus/{cursus_id}/cursus_users"
        return HttpRequest(target, self.session, **kwargs)

    def cursus_projects(self, cursus_id:str, **kargs):
        target = f"/v2/cursus/{cursus_id}/projects"
        return HttpRequest(target, self.session, **kwargs)

    #######################################################
    #                    campus                           #
    #######################################################

    def campus_users(self, campus_id:str, **kwargs):
        target = f"/v2/campus/{campus_id}/users"
        return HttpRequest(target, self.session, **kwargs)

    def campus_exams(self, campus_id:str, **kwargs):
        target = f"/v2/campus/{campus_id}/exams"
        return HttpRequest(target, self.session, **kwargs)

    def campus_locations(self, campus_id, **kwargs):
        target =f"/v2/campus/{campus_id}/locations"
        return HttpRequest(target, self.session, **kwargs)

    #######################################################
    #                    projects users                   #
    #######################################################

    def projectUsers(self, project_user_id:str=None, **kwargs):
        if project_user_id:
            target = f"/v2/projects_users/{project_user_id}"
        else:
            target = "/v2/projects_users"
        return HttpRequest(target, self.session, **kwargs)

    def projects_projectsUsers(self, project_id:str, **kwargs):
        target = f"/v2/projects/{project_id}/projects_users"
        return HttpRequest(target, self.session, **kwargs)

    def projects_register(self, project_id:str, **kwargs):
        target = f"/v2/projects/{project_id}/register"
        return HttpRequest(target, self.session, **kwargs)

    #######################################################
    #                       roles                         #
    #######################################################

    def roles(self, role_id:str=None, **kwargs):
        if role_id:
            target = f"/v2/roles/{role_id}"
        else:
            target = "/v2/roles"
        return HttpRequest(target, self.session, **kwargs)

    def rolesEntities(self, role_id:str=None, **kwargs):
        if role_id:
            target = f"/v2/roles_entities/{role_id}"
        else:
            target = "/v2/roles_entities"
        return HttpRequest(target, self.session, **kwargs)

    def roles_rolesEntities(self, role_id:str, **kwargs):
        target = f"/v2/roles/{role_id}/roles_entities"
        return HttpRequest(target, self.session, **kwargs)

    #######################################################
    #                       groups                        #
    #######################################################

    def groups(self, group_id:str=None, **kwargs):
        if group_id:
            target = f"/v2/groups/{group_id}"
        else:
            target = "/v2/groups"
        return HttpRequest(target, self.session, **kwargs)

    def groups_groupsUsers(self, group_id:str=None, **kwargs):
        if group_id:
            target = f"/v2/groups/{group_id}/groups_users"
        else:
            target = "/v2/groups/{g}"
        return HttpRequest(target, self.session, **kwargs)

    def groupsUsers(self, group_user_id:str=None, **kwargs):
        if group_user_id:
            target = f"/v2/groups_users/{group_user_id}"
        else:
            target = f"/v2/groups_users"
        return HttpRequest(target, self.session, **kwargs)

    #######################################################
    #                       scales                        #
    #######################################################


    #######################################################
    #                   scales_teams                      #
    #######################################################


    #######################################################
    #                    evaluations                      #
    #######################################################
