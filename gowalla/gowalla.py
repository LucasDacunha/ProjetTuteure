import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import diffprivlib.models as dp

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
checkins['check_in_time'] = checkins['check_in_time'].str[:13]
location_to_date = {}
link_between = {}

checkinsTMF = checkins.loc[checkins['user'].isin(checkins['user'].value_counts()[:10000].index.tolist())]

"""for row in checkinsTMF.index:
    if checkinsTMF['location_id'][row] in location_to_date:
        if checkinsTMF['check_in_time'][row] in location_to_date[checkinsTMF['location_id'][row]]:
            location_to_date[checkinsTMF['location_id'][row]][checkinsTMF['check_in_time'][row]]\
                .append(checkinsTMF['user'][row])
        else:
            location_to_date[checkinsTMF['location_id'][row]][checkinsTMF['check_in_time'][row]] = \
                [checkinsTMF['user'][row]]
    else:
        date_to_user = {checkinsTMF['check_in_time'][row]: [checkinsTMF['user'][row]]}
        location_to_date[checkinsTMF['location_id'][row]] = date_to_user

    user_list = location_to_date[checkinsTMF['location_id'][row]][checkinsTMF['check_in_time'][row]]
    user = checkinsTMF['user'][row]
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
                link_between[u][user] = 1"""

# print("location to date to users for location 14637 :")
# print(location_to_date[14637])

"""sorted_dict = {}
sorted_key = sorted(link_between[0], key=link_between[0].get, reverse=True)
for k in sorted_key:
    sorted_dict[k] = link_between[0][k]
print()
print("link for user 0 :")
print(sorted_dict)"""

# 10 pos les plus visités parmis les 10000 users les plus fréquents
users_more_frequent_locations = {}
for row in checkinsTMF.index:
    if checkinsTMF['user'][row] in users_more_frequent_locations:
        users_more_frequent_locations[checkinsTMF['user'][row]].append(checkinsTMF['location_id'][row])
    else:
        user_to_location = [checkinsTMF['location_id'][row]]
        users_more_frequent_locations[checkinsTMF['user'][row]] = user_to_location

for key in users_more_frequent_locations:
    users_more_frequent_locations[key] = \
        list(dict.fromkeys([item for items, c in Counter(users_more_frequent_locations[key]).
                           most_common() for item in [items] * c]))[:10]

# print(users_more_frequent_locations)
rows = []
for key in users_more_frequent_locations:
    rows.append(
        checkins[(checkins["user"] == key) & (checkins["location_id"] == users_more_frequent_locations[key][0])].iloc[
            0])
dataF = pd.DataFrame(rows, columns=["user", "check_in_time", "latitude", "longitude", "location_id"])
del dataF["check_in_time"]

K_clusters = range(1, 10)
kmeans = [dp.KMeans(n_clusters=i) for i in K_clusters]
Y_axis = dataF[['latitude']]
X_axis = dataF[['longitude']]
score = [kmeans[i].fit(Y_axis).score(Y_axis) for i in range(len(kmeans))]
# Visualize
plt.plot(K_clusters, score)
plt.xlabel('Number of Clusters')
plt.ylabel('Score')
plt.title('Elbow Curve')
plt.show()

kmeans = dp.KMeans(n_clusters=3, init='k-means++')
kmeans.fit(dataF[dataF.columns[1:3]])  # Compute k-means clustering.
dataF['cluster_label'] = kmeans.fit_predict(dataF[dataF.columns[1:3]])
centers = kmeans.cluster_centers_  # Coordinates of cluster centers.
labels = kmeans.predict(dataF[dataF.columns[1:3]])  # Labels of each point
print(dataF)

dataF.plot.scatter(x='latitude', y='longitude', c=labels, s=50, cmap='viridis')
plt.scatter(centers[:, 0], centers[:, 1], c='black', s=200, alpha=0.5)
plt.show()
