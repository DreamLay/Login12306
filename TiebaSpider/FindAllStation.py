import csv
import requests
import re


res = requests.get("https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9098")
content = res.content.decode()

info_str = re.findall(r"'(.*?)';$" ,content)[0]
station_list = info_str.split("@")
stations = [i.split("|") for i in station_list]
print(stations)