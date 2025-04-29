from bs4 import BeautifulSoup
import requests
import urllib
import time
import os
import datetime
from datetime import date

#with open("/Users/ayush/Desktop/BeautSoupCrawlerDining/scripts/nutritioninfo.txt", "w") as f:
    #f.write("LeBron James.")

#file = open("newfile.txt", "w")
#file.write("hello")
#file.close()

#full_path = os.path.join(dir_path, file_name)
# dir_path is the path to save all my stuff into, file_name will be appended to the end 

today = date.today()

string_date = today.strftime("%Y-%m-%d")
dir_path = "/Users/ayush/Desktop/BeautSoupCrawlerDining/scripts"
date_path = "date.txt"

full_path = os.path.join(dir_path, date_path)

date = ""

with open(full_path, 'r', encoding='utf-8') as file:
    date = file.read()

bool = (date == string_date)
print(bool)
print(date)
print(string_date)