import ollama
import chromadb
from sentence_transformers import SentenceTransformer

def query_func(query, collection, n_results=3):

    closestPages = collection.query(
        query_texts = [query],
        n_results = n_results
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