from bs4 import BeautifulSoup
import requests
import urllib
import time
import os
import datetime
from datetime import date
import chromadb

#with open("/Users/ayush/Desktop/BeautSoupCrawlerDining/scripts/nutritioninfo.txt", "w") as f:
    #f.write("LeBron James.")

#file = open("newfile.txt", "w")
#file.write("hello")
#file.close()

#full_path = os.path.join(dir_path, file_name)
# dir_path is the path to save all my stuff into, file_name will be appended to the end 

dir_path = dir_path = "/Users/ayush/Desktop/BeautSoupCrawlerDining/scripts"

chroma_path = os.path.join(dir_path, "ChromaClient")

chroma_client = chromadb.PersistentClient(path=chroma_path)

collection = chroma_client.get_collection("Dining_Collection")

results = collection.query(
    query_texts=["High calorie foods"],
    n_results=5,
    include=['documents', 'metadatas']
)

print(results)