from bs4 import BeautifulSoup
import requests
import urllib
import time
import os
import ollama
import chromadb
from sentence_transformers import SentenceTransformer
from datetime import date

from scraper import scrape_vt_dining_locations, write_dining_file

dir_path = "/Users/ayush/Desktop/BeautSoupCrawlerDining/scripts"
date_path = "date.txt"

full_path = os.path.join(dir_path, date_path)

dateText = ""

with open(full_path, 'r', encoding='utf-8') as file:
    dateText = file.read()

today = date.today()

date_string = today.strftime("%Y-%m-%d")


dining_file_paths = []


def get_text(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

if (date_string != dateText):

    with open(full_path, 'w') as date_file:
        date_file.write(date_string)
    
    dining_halls = scrape_vt_dining_locations("https://foodpro.students.vt.edu/menus/")
    dir_path = "/Users/ayush/Desktop/BeautSoupCrawlerDining/scripts"

    dining_file_paths.clear()

    for hall in dining_halls:
        dining_file_paths.append(write_dining_file(hall, dir_path))


    chroma_client = chromadb.Client()
    collection = chroma_client.get_or_create_collection("RestaurantCollection")


    documents = []
    ids = []

    id = 0
    for file in dining_file_paths:
        file = os.path.join(dir_path, file)
        text = get_text(file)
        documents.append(text)
        ids.append(f"doc_{id}")

        id += 1

    collection.add(
        documents=documents,
        ids=ids
    )

    query = input("What are your nutrition goals for today?\n>>>")

    closestPages = collection.query(
        query_texts=[query],
        n_results=4
    )

    system_messages = []
    for doc in closestPages["documents"][0]:
        system_messages.append({
            "role": "system",
            "content": doc
        })

    messages = system_messages + [{
        "role":"user",
        "content": query
    }]

    response = ollama.chat(
        model="llama3.2",
        messages=messages
    )

    print(response["message"]["content"])
else:
    chroma_client = chromadb.Client()
    collection = chroma_client.get_or_create_collection("RestaurantCollection")


    documents = []
    ids = []

    id = 0
    for file in dining_file_paths:
        text = get_text(file)
        documents.append(text)
        ids.append(f"doc_{id}")

        id += 1

    collection.add(
        documents=documents,
        ids=ids
    )

    query = input("What are your nutrition goals for today?\n>>>")

    closestPages = collection.query(
        query_texts=[query],
        n_results=4
    )

    system_messages = []
    for doc in closestPages["documents"][0]:
        system_messages.append({
            "role": "system",
            "content": doc
        })

    messages = system_messages + [{
        "role":"user",
        "content": query
    }]

    response = ollama.chat(
        model="llama3.2",
        messages=messages
    )

    print(response["message"]["content"])
