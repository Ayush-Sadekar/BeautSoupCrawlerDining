import ollama
import chromadb
from sentence_transformers import SentenceTransformer

def query_func(query, n_results=3):
    return