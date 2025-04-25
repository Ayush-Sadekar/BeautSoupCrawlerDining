from bs4 import BeautifulSoup
import requests
import urllib
import time
import os

# this function gets the link for each dining location
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

base_url = "https://foodpro.students.vt.edu/menus/"

location_menu_urls = scrape_vt_dining_locations(base_url)


# this function gets the link for each menu item. Returns a dictionary. Each key is a dining hall, and it corresponds to a list of the link of each menu item
def get_menu_items(urls):

    link_dict = {}

    for url in urls:

        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        food_links = set()

        hall_name = soup.find(id="dining_center_name_container").text.strip()

        links = soup.find_all('a', href=True)

        for link in links:
            href = link['href']
            absolute_url = urllib.parse.urljoin(url, href)

            if "label.aspx?locationNum=" in absolute_url and absolute_url not in food_links:
                food_links.add(absolute_url)

        link_dict[hall_name] = food_links
    
    return link_dict

my_dict = get_menu_items(location_menu_urls)

# this function extracts the nutrition information from each link in the list corresponding to the keys of the dictionary from the last function. Creates a long String -- maybe just write a text file

def write_file(food_dict):

    file_text = ""

    for key in food_dict.keys():

        file_text += key + ": "
        food_list = food_dict[key]



        for item in food_list:

            response = requests.get(item)
            soup = BeautifulSoup(response.text, 'html.parser')

            recipe_title = soup.find(id="recipe_title")
            if recipe_title is None:
                pass
            else:
                item_Name = soup.find(id="recipe_title").text.strip()
                calories = soup.find(id="calories_container").text.strip()
                file_text += "(" + item_Name + ": " + calories + " "
                #protein = soup.find('p', class_="col-lg-12").text.strip() if soup.find('p', class_="col-lg-12") != None or soup.find('p', class_="col-lg-12").text != None else "protein unavailable"
                file_text += ")\n"
    
    with open("/Users/ayush/Desktop/BeautSoupCrawlerDining/scripts/nutritioninfo.txt", "w") as f:
        f.write(file_text)

write_file(my_dict)

def write_dining_file(location_url, file_name, dir_path):

    file_text = ""

    response = requests.get(location_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    hall_name = soup.find(id="dining_center_name_container").text.strip()
    file_text += "Dining Hall Name: " + hall_name + "\n"

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
                    calories = new_soup.find(id="calories_container").text.strip()
                    file_text += "(" + item_Name + ": " + calories + " "
                    
                    protein = new_soup.find('p', class_ = "col-lg-12")
                    if protein is None:
                        protein = "protein unavailable"
                    else:
                        protein = new_soup.find('p', class_ = "col-lg-12").text.strip()
                    file_text += protein + ")\n"


                food_items.add(absolute_url)
    
    full_path = os.path.join(dir_path, file_name)
    file = open(full_path, "w")
    file.write(file_text)
    file.close()


def get_hours():

    


