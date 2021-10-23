import matplotlib.pyplot as plt
import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('max_colwidth', None)

city = pd.read_csv("san_francisco-traversals.csv")
# city = pd.read_csv("paris-traversals.csv")
city = city.convert_dtypes()

weekday = city[city["dayType"] == "weekday"]
weekend = city[city["dayType"] == "weekend"]

c = city.hexid.value_counts()

count_1 = city[city.hexid.isin(c.index[c.eq(1)])]
count_1_weekday = count_1[count_1["dayType"] == "weekday"]
count_1_weekend = count_1[count_1["dayType"] == "weekend"]

count_2 = city[city.hexid.isin(c.index[c.eq(2)])]
count_2_weekday = count_2[count_2["dayType"] == "weekday"]
count_2_weekend = count_2[count_2["dayType"] == "weekend"]


def print_values(data, text):
    print("Values of traversals" + text + " :")
    print(data.describe())
    print("Median is " + str(data.traversals.median()))
    print()
    print("Max value(s) are in hexid(s) : ")
    max_values = data[data["traversals"] == data.traversals.max()]
    print(max_values)
    print()
    print("Min value(s) are in hexid(s) : ")
    min_values = data[data["traversals"] == data.traversals.min()]
    print(min_values)
    print()
    print()


print_values(city, "")
print_values(weekday, " in weekdays")
print_values(weekend, " in weekends")
print_values(count_1, " that appears only in weekdays or in weekends")
print_values(count_1_weekday, " that appears only in weekdays")
print_values(count_1_weekend, " that appears only in weekends")
print_values(count_2, " that appears both in weekdays and in weekends")
print_values(count_2_weekday, " in weekdays between those that appears both in weekdays and in weekends")
print_values(count_2_weekend, " in weekends between those that appears both in weekdays and in weekends")

count_2_diff_hexids = count_2.hexid.count() / 2
nb_only_weekday_hexids = count_1_weekday.hexid.count()
nb_only_weekend_hexids = count_1_weekend.hexid.count()
nb_diff_hexid_total = int(count_2.hexid.count() / 2 + count_1_weekday.hexid.count() + count_1_weekend.hexid.count())
traversals_of_hexids = {'Both weekdays and weekends': count_2_diff_hexids,
                        'Only the weekdays': nb_only_weekday_hexids,
                        'Only the weekends': nb_only_weekend_hexids}
ser = pd.Series(data=traversals_of_hexids,
                index=['Both weekdays and weekends', 'Only the weekdays', 'Only the weekends'])
explode = (0.1, 0, 0)
ser.plot.pie(
    labels=["Both weekdays and weekends", "Only the weekdays", "Only the weekends"],
    colors=["m", "darkorange", "g"],
    explode=explode,
    shadow=True,
    startangle=90,
    autopct="%.2f",
    fontsize=10,
    figsize=(6, 4),
)
plt.ylabel("TOTAL : " + str(nb_diff_hexid_total))
plt.xlabel("TRAVERSALS OF HEXIDS :")
plt.show()


def make_plot_bar(text, col, city_s, weekday_s, weekend_s, count_1_s, count_1_weekday_s, count_1_weekend_s, count_2_s,
                  count_2_weekday_s, count_2_weekend_s):
    df = pd.DataFrame({
        'TYPES OF TRAVERSALS': ['All',
                                'All-weekdays',
                                'All-weekends',
                                'Xor-all',
                                'Xor-weekdays',
                                'Xor-weekends',
                                'And-all',
                                'And-weekdays',
                                'And-weekends'],
        text: [city_s,
               weekday_s,
               weekend_s,
               count_1_s,
               count_1_weekday_s,
               count_1_weekend_s,
               count_2_s,
               count_2_weekday_s,
               count_2_weekend_s]}, )
    df.plot.bar(x='TYPES OF TRAVERSALS', y=text, rot=45, color=col, figsize=(10, 10))
    plt.show()


make_plot_bar('mean of traversals', 'm',
              city.traversals.mean(),
              weekday.traversals.mean(),
              weekend.traversals.mean(),
              count_1.traversals.mean(),
              count_1_weekday.traversals.mean(),
              count_1_weekend.traversals.mean(),
              count_2.traversals.mean(),
              count_2_weekday.traversals.mean(),
              count_2_weekend.traversals.mean())

make_plot_bar('std of traversals', 'darkorange',
              city.traversals.std(),
              weekday.traversals.std(),
              weekend.traversals.std(),
              count_1.traversals.std(),
              count_1_weekday.traversals.std(),
              count_1_weekend.traversals.std(),
              count_2.traversals.std(),
              count_2_weekday.traversals.std(),
              count_2_weekend.traversals.std())

make_plot_bar('min of traversals', 'g',
              city.traversals.min(),
              weekday.traversals.min(),
              weekend.traversals.min(),
              count_1.traversals.min(),
              count_1_weekday.traversals.min(),
              count_1_weekend.traversals.min(),
              count_2.traversals.min(),
              count_2_weekday.traversals.min(),
              count_2_weekend.traversals.min())

make_plot_bar('max of traversals', 'aqua',
              city.traversals.max(),
              weekday.traversals.max(),
              weekend.traversals.max(),
              count_1.traversals.max(),
              count_1_weekday.traversals.max(),
              count_1_weekend.traversals.max(),
              count_2.traversals.max(),
              count_2_weekday.traversals.max(),
              count_2_weekend.traversals.max())

make_plot_bar('median of traversals', 'lightpink',
              city.traversals.median(),
              weekday.traversals.median(),
              weekend.traversals.median(),
              count_1.traversals.median(),
              count_1_weekday.traversals.median(),
              count_1_weekend.traversals.median(),
              count_2.traversals.median(),
              count_2_weekday.traversals.median(),
              count_2_weekend.traversals.median())


travel_time = pd.read_csv("san_francisco-censustracts-2020-1-All-MonthlyAggregate.csv")
travel_time = travel_time.convert_dtypes()
print(travel_time)

january = travel_time[travel_time["month"] == 1]
february = travel_time[travel_time["month"] == 2]
march = travel_time[travel_time["month"] == 3]

min_j = january[january["mean_travel_time"] == january.mean_travel_time.min()]
print(min_j)
max_j = january[january["mean_travel_time"] == january.mean_travel_time.max()]
print(max_j)
min_f = february[february["mean_travel_time"] == february.mean_travel_time.min()]
print(min_f)
max_f = february[february["mean_travel_time"] == february.mean_travel_time.max()]
print(max_f)
min_m = march[march["mean_travel_time"] == march.mean_travel_time.min()]
print(min_m)
max_m = march[march["mean_travel_time"] == march.mean_travel_time.max()]
print(max_m)

print()
print("count :")
print("janurary :")
cnt_src_j = january.sourceid.value_counts()
print(cnt_src_j)
cnt_dst_j = january.dstid.value_counts()
print(cnt_dst_j)
print("february :")
cnt_src_f = february.sourceid.value_counts()
print(cnt_src_f)
cnt_dst_f = february.dstid.value_counts()
print(cnt_dst_f)
print("march :")
cnt_src_m = march.sourceid.value_counts()
print(cnt_src_m)
cnt_dst_m = march.dstid.value_counts()
print(cnt_dst_m)

