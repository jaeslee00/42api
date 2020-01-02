idx = 1
data = []
while True:
    down = jai.campus_users('1', filter={"pool_year":"2019", "pool_month":"july"}, page={"size":100, "number":idx}).get()
    if len(down) < 1:
        break
    data = data + down
    idx += 1
    sleep(0.5)

user_list = []
for idx, elem in enumerate(data):
    if elem["login"].find("3b3-") > -1:
        pass
    else:
        user_list.append([idx, elem["login"], elem["id"]])

users_projects = {}
for user in user_list:
    resp = api.users(user[1]).get()
    sleep(0.5)
    scores = {}
    for p in resp["projects_users"]:
        if p["project"]["slug"].find("c-piscine") > -1:
            scores.update({p["project"]["slug"] : p["final_mark"]})
    users_projects.append({"login":resp["login"], "scores" : scores})

# list : users_projects
# list : users_feedback
# list : users_diff
# list : users_megatron

list : c-piscine(without rush)

for user in user_list:
    resp = jai.users_teams(user["id"], filter={"project_id" : })

for team in teams:
    for scale_team in team["scale_teams"]:
        corrector = scale_team["corrector"]["id"]
        given_mark = scale_team["final_mark"]
        moulinette_mark = team["teams_uploads"][0]["final_mark"]
        diff = given_mark - moulinette_mark

{
  "cursus_user": {
    "begin_at": "2019-11-22 13:43:10 UTC",
    "cursus_id": "1",
    "user_id": "67127",
  }
}
