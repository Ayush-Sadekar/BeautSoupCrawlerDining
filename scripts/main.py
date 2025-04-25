from bs4 import BeautifulSoup
import requests
import urllib
import time
import os
import ollama
import chromadb
from sentence_transformers import SentenceTransformer

from scraper import scrape_vt_dining_locations, write_dining_file, get_hours

dining_halls = scrape_vt_dining_locations("https://foodpro.students.vt.edu/menus/")
dir_path = "/Users/ayush/Desktop/BeautSoupCrawlerDining/scripts"

file_paths = []

for hall in dining_halls:
    file_paths.append(write_dining_file(hall, dir_path))


