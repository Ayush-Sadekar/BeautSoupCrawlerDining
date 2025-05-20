from bs4 import BeautifulSoup
import requests
import urllib
import time
import os
from datetime import date

# this function gets the link for each dining location (STILL USING THIS)
def scrape_vt_dining_locations(base_url):
    
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    
    visited_urls = set()
    
    
    links = soup.find_all('a', href=True)
    
    for link in links:
        href = link['href']
        absolute_url = urllib.parse.urljoin(base_url, href)
        
        
        if "MenuAtLocation.aspx" in absolute_url and absolute_url not in visited_urls:
            #print(f"Found dining location: {absolute_url}")
            visited_urls.add(absolute_url)
    
    return visited_urls

# new function to use that implements metadata
# USING THIS
def get_item_and_metadata(location_url):

    item_dict = {}

    response = requests.get(location_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    hall_name = soup.find(id="dining_center_name_container").text.strip()

    links = soup.find_all('a', href=True)
    food_items = set()

    for link in links:
        
        href = link['href']
        absolute_url = urllib.parse.urljoin(location_url, href)

        if "label.aspx?locationNum=" in absolute_url and absolute_url not in food_items:
            
            new_response = requests.get(absolute_url)
            new_soup = BeautifulSoup(new_response.text, "html.parser")

            recipe_title = new_soup.find(id="recipe_title")

            if recipe_title is None:
                pass
            else:
                item_Name = new_soup.find(id="recipe_title").text.strip()
                calories = new_soup.find(id="calories_container").text.strip().replace("Calories\r\n", "").replace(" ", "")
                ingredients = new_soup.find(class_="ingredients_container")
                if ingredients is None:
                    ingredients = "ingredients unavailable"
                else:
                    ingredients = ingredients.text.strip()
                protein = new_soup.find(class_ = "col-lg-12 daily_value protein").text.strip().replace("Protein ", "")

                item_dict[item_Name] = {"Dish": recipe_title.text.strip(), "Location": hall_name, "Calories": calories, "Ingredients": ingredients, "Protein": protein, "Date": date.today().strftime("%Y-%m-%d")}
            
            food_items.add(absolute_url)
    
    return item_dict

url = "https://foodpro.students.vt.edu/menus/"

locations = scrape_vt_dining_locations(url)
