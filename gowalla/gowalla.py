import pandas as pd

# pd.set_option('display.max_rows', None)

checkins = pd.read_csv("Gowalla_totalCheckins.txt", delimiter="\t")
checkins.columns = ["user", "check_in_time", "latitude", "longitude", "location_id"]
checkins = checkins.convert_dtypes()

edges = pd.read_csv("Gowalla_edges.txt", delimiter="\t")
edges.columns = ["user", "friend"]

"""checkins_user0 = checkins[checkins["user"] == 0]
edges_friends_of_0 = edges[edges["user"] == 0]
checkins_friends_of_0 = checkins[checkins["user"].isin(edges[edges["user"] == 0].friend)]
checkins_in_common_with_0 = checkins_friends_of_0[checkins_friends_of_0["location_id"].isin(checkins_user0.location_id)]
# checkins_in_common_from_0 = checkins_user0[checkins_user0["location_id"].isin(checkins_friends_of_0.location_id)]

# print(checkins_in_common_with_0)
checkins_in_common_with_0['check_in_time'] = checkins_in_common_with_0['check_in_time'].str[:10]
checkins_user0['check_in_time'] = checkins_user0['check_in_time'].str[:10]

for index_friend, value_friend in checkins_in_common_with_0.iterrows():
    for index0, value0 in checkins_user0.iterrows():
        if value_friend.check_in_time == value0.check_in_time and value_friend.location_id == value0.location_id:
            print(value0)
            print(value_friend)"""

# Dictionnaire
checkins['check_in_time'] = checkins['check_in_time'].str[:10]
location_to_date = {}
link_between = {}

for row in checkins.index:
    if checkins['location_id'][row] in location_to_date:
        if checkins['check_in_time'][row] in location_to_date[checkins['location_id'][row]]:
            location_to_date[checkins['location_id'][row]][checkins['check_in_time'][row]].append(checkins['user'][row])
        else:
            location_to_date[checkins['location_id'][row]][checkins['check_in_time'][row]] = [checkins['user'][row]]
    else:
        date_to_user = {checkins['check_in_time'][row]: [checkins['user'][row]]}
        location_to_date[checkins['location_id'][row]] = date_to_user

    user_list = location_to_date[checkins['location_id'][row]][checkins['check_in_time'][row]]
    user = checkins['user'][row]
    if user not in link_between:
        link_between[user] = {}
    for u in user_list:
        if u != user:
            if u in link_between[user]:
                link_between[user][u] += 1
            else:
                link_between[user][u] = 1
            if user in link_between[u]:
                link_between[u][user] += 1
            else:
                link_between[u][user] = 1

# print(location_to_date[420315])
print(link_between[0])
sorted_dict = {}
sorted_key = sorted(link_between[0], key=link_between[0].get, reverse=True)
for k in sorted_key:
    sorted_dict[k] = link_between[0][k]

print(sorted_dict)
