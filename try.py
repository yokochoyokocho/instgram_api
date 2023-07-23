import datetime

# value = "2023-07-03T07:00:00+0000"
# dte = datetime.datetime.strptime(value, '%Y-%m-%dT%H:%M:%S+0000')
# print(dte.month)
# print(dte.day)

# print(value["end_time"].dt.year)
# print(str[value].dt.year)

# str = '2023-07-15T07:00:00+0000'
# dte = datetime.datetime.strptime(str, '%Y-%m-%dT%H:%M:%S+0000')
# print(dte.month)
# 7
# print(dte.day)
# 15



value = "2023-07-03T07:00:00+0000"
dte = datetime.datetime.strptime(value, '%Y-%m-%dT%H:%M:%S+0000')

date_output = f"{dte.month}月{dte.day}日"
print(date_output)


# print(dte.month)
# print(dte.day)
