import os
import chromadb
from sentence_transformers import SentenceTransformer
from datetime import date
import shutil
from scraper import scrape_vt_dining_locations, write_dining_file
from LLM_stuff import query_func

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


def get_text(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def delete_files_in_folder(folder_path):
    try:
        # check if folder exists
        if not os.path.exists(folder_path):
            print(f"The folder {folder_path} does not exist.")
            return
        
        # check each file
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            
            # check if it is a file
            if os.path.isfile(file_path):
                # delete file
                os.remove(file_path)
                print(f"Deleted: {file_path}")
            
        print(f"All files in {folder_path} have been deleted.")
        
    except Exception as e:
        print(f"An error occurred: {e}")

if (date_string != dateText):

    with open(date_path, 'w') as date_file:
        date_file.write(date_string)
    
    delete_files_in_folder("/Users/ayush/Desktop/BeautSoupCrawlerDining/DiningHalls")
    
    try:
    
        # scrape dining hall websites
        dining_halls = scrape_vt_dining_locations("https://foodpro.students.vt.edu/menus/")
        dining_file_paths = []

        d_file_path = "/Users/ayush/Desktop/BeautSoupCrawlerDining/DiningHalls"

        for hall in dining_halls:
            dining_file_paths.append(write_dining_file(hall, d_file_path))

        # get/create DB client and update documents
        chroma_client = chromadb.PersistentClient(path=chroma_path)
        collection = chroma_client.get_or_create_collection("Dining_Collection")

        documents = []
        ids = []

        id = 0
        for file in dining_file_paths:
            file = os.path.join(dir_path, file)
            text = get_text(file)
            documents.append(text)
            ids.append(f"doc_{id}")

            id += 1

        collection.upsert(
            documents=documents,
            ids=ids
        )

        # get user query and feed to LLM for a response
        query = input("What are your nutrition goals for today?\n>>>")
        query_func(query, collection)

    except Exception as e:
        print(f"Error updating dining information: {e}")

else:
    
    # Only need to scrape once per day. Just load persistent client, which saves documents and ids from first scrape
    chroma_client = chromadb.PersistentClient(path=chroma_path)
    collection = chroma_client.get_collection("Dining_Collection")

    query = input("What are your nutrition goals for today?\n>>>")

    query_func(query, collection)
