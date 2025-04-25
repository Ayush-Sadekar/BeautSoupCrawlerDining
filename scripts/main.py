from bs4 import BeautifulSoup
import requests
import urllib
import time
import os
import ollama
import chromadb
from sentence_transformers import SentenceTransformer

from scraper import scrape_vt_dining_locations, write_dining_file, get_hours