# using this file to primarily test out any questions about my code 
# also used to add docs+metadata based on the new doc enrichment function
from bs4 import BeautifulSoup
import requests
import urllib
import time
import os
from datetime import date
from datetime import date
import chromadb
import random

from scraper import scrape_vt_dining_locations
from LLM_stuff import process_data

#with open("/Users/ayush/Desktop/BeautSoupCrawlerDining/scripts/nutritioninfo.txt", "w") as f:
    #f.write("LeBron James.")

#file = open("newfile.txt", "w")
#file.write("hello")
#file.close()

#full_path = os.path.join(dir_path, file_name)
# dir_path is the path to save all my stuff into, file_name will be appended to the end 

dir_path = "/Users/ayush/Desktop/BeautSoupCrawlerDining/DiningHalls"
url = "https://foodpro.students.vt.edu/menus/"

locations = scrape_vt_dining_locations(url)
hall_names = []

for loc in locations: 
    response = requests.get(loc)
    soup = BeautifulSoup(response.text, 'html.parser')

    hall_name = soup.find(id="dining_center_name_container").text.strip()
    if "/" in hall_name:
        hall_name = hall_name.replace("/", "or")
    hall_names.append(hall_name)

item_dict = {}

for hall in hall_names:

    path = os.path.join(dir_path, hall)
    path += ".txt"

    with open(path, "r") as file:
        lines = file.readlines()
    
    name = hall
    
    for i in range(1, len(lines), 2): 
        
        mtadata = {}

        name_line = lines[i]
        calories = lines[i+1]

        name_line = name_line.replace("(", "")
        name_line = name_line.replace(": Calories", "")
        name_line = name_line.replace("\n", "")

        calories = calories.replace("                                      ", "")
        calories = calories.replace(" protein unavailable)", "")
        calories = calories.replace("\n", "")

        protein = random.uniform(15.0, 45.0)
        protein = str(protein)


        day = date.today().strftime("%Y-%m-%d")

        mtadata["Calories"] = calories
        mtadata["Protein"] = f"{protein}g"
        mtadata["Date"] = day
        mtadata["Location"] = name
        mtadata["Dish"] = name_line
        mtadata["Ingredients"] = "N/A"

        item_dict[name_line] = mtadata

chroma_path = os.path.join("/Users/ayush/Desktop/BeautSoupCrawlerDining/scripts", "ChromaClient")
chroma_client = chromadb.PersistentClient(path=chroma_path)

collection = chroma_client.get_or_create_collection("Dining_Collection")

process_data(collection=collection, ticker="newlyenriched", item_dict=item_dict, current_id=0)

# the function: 
# open each file in the dining halls folder 
# with the readlines, every two lines is 1 thing
# use random float generator for generating the protein amount

