import ollama
import chromadb
from sentence_transformers import SentenceTransformer

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

chroma_client = chromadb.Client()
collection = chroma_client.create_collection("DiningCollection", embedding_function=embedding_model)

paths = []

## make function to get all paths and properly add information to collection 

documents = []
ids = []

query = input("What are your nutrition goals for today?\n>>>")

