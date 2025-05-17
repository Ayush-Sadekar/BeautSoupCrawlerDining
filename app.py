from flask import Flask, request, jsonify, render_template
import chromadb
import os
from dotenv import load_dotenv
import ollama


def scrape_locations():
    pass


def get_info_per_hall():
    pass

def process_query(query, collection, n_results=3):
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

    return response["message"]["content"]

def process_data(collection, item_dict, current_id):
    documents = list(item_dict.keys())

    metadata = []

    for data in item_dict.values():
        metadata.append(data)
    
    ids = []

    for item in documents:
        ids.append(f"doc_{current_id}")
        current_id += 1
    
    collection.upsert(
        documents=documents,
        metadatas=metadata,
        ids=ids
    )

    return current_id
