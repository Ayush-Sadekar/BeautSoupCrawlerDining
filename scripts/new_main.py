import chromadb
from sentence_transformers import SentenceTransformer
from datetime import date
import os
from scraper import scrape_vt_dining_locations, get_item_and_metadata
from LLM_stuff import query_func, process_data

# directories
dir_path = "/Users/ayush/Desktop/BeautSoupCrawlerDining/scripts"
date_path = os.path.join(dir_path, "date.txt")
chroma_path = os.path.join(dir_path, "ChromaClient")

chroma_client = chromadb.PersistentClient(path=chroma_path)

dateText = ""

try:
    with open(date_path, 'r', encoding='utf-8') as file:
        dateText = file.read()
except FileNotFoundError:
    dateText = ""

today = date.today()
date_string = today.strftime("%Y-%m-%d")

if (date_string != dateText):

    with open(date_path, 'w') as date_file:
        date_file.write(date_string)
    
    try:

        dining_halls = scrape_vt_dining_locations("https://foodpro.students.vt.edu/menus/")

        chroma_client = chromadb.PersistentClient(path=chroma_path)
        collection = chroma_client.get_or_create_collection("Dining_Collection")

        current_id = 0

        for hall in dining_halls:
            hall_dict = get_item_and_metadata(hall)

            