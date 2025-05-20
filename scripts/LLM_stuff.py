import ollama
from datetime import date

def query_func(query, collection, n_results=5):
    #print(f"collection is {collection}")

    closestPages = collection.query(
        query_texts = [query],
        n_results = n_results,
        include=["documents", "metadatas"]
    )
    #print(f"closestPages = {closestPages}")


    context = "Available Menu Items: \n"
    

    for doc, m in zip(closestPages["documents"][0], closestPages["metadatas"][0]):
        context += (
            f"Menu Item: {doc}\n"
            f"Hall: {m["Location"]}\n"
            f"Calories: {m["Calories"]}\n"
            f"Protein: {m["Protein"]}\n"
            f"Ingredients: {m["Ingredients"]}"
        )

    response = ollama.generate(
        model="llama3.2",
        prompt=(
            f"Context:\n{context}\n\n"
            f"Query: {query}\n\n"
            "Instructions:\n"
            "1. Answer using only the provided context\n"
            "2. Be specific about hall names and ingredients\n"
            "3. If unsure, request clarification\n"
            "4. Mention calorie counts and protein values when relevant\n"
            "5. If any float values have more than 2 decimal points, round it back down to 2 decimal points.\n"
            "Answer:"
        )
    )

    return response["response"]

def process_data(collection, item_dict, current_id, ticker=""):

    if len(item_dict) <= 0:
        return current_id
    
    og_documents = list(item_dict.keys())

    enriched_documents = []

    for doc in og_documents:
        new_doc = enrich_doc_text(doc, item_dict[doc])
        enriched_documents.append(new_doc)

    metadata = []

    for data in item_dict.values():
        metadata.append(data)
    
    ids = []

    for item in enriched_documents:
        ids.append(f"doc_{ticker}" + date.today().strftime("%Y-%m-%d") + f"_{current_id}")
        current_id += 1
    
    collection.upsert(
        documents=enriched_documents,
        metadatas=metadata,
        ids=ids
    )

    return current_id

# using this for compatibility with Modal deployment
def query_func_messages(query, collection, n_results=5):

    closestPages = collection.query(
        query_texts = [query],
        n_results = n_results,
        include=["documents", "metadatas"]
    )
    #print(f"closestPages = {closestPages}")


    context = "Available Menu Items: \n"
    

    for doc, m in zip(closestPages["documents"][0], closestPages["metadatas"][0]):
        context += (
            f"Menu Item: {doc}\n"
            f"Hall: {m["Location"]}\n"
            f"Calories: {m["Calories"]}\n"
            f"Protein: {m["Protein"]}\n"
            f"Ingredients: {m["Ingredients"]}"
        )
    
    fields = [query, context]
    return fields

# enriching document for better search within ChromaDB
def enrich_doc_text(doc, meta):

    return f"Menu Item: {doc} | Location: {meta["Location"]} | Calories: {meta["Calories"]} | Protein: {meta["Protein"]} | Ingredients: {meta["Ingredients"]}"
