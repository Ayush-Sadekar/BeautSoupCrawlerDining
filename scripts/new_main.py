import chromadb
from sentence_transformers import SentenceTransformer
from datetime import date
import os
from scraper import scrape_vt_dining_locations, get_item_and_metadata
from LLM_stuff import query_func, process_data
from flask import Flask, request, jsonify, render_template

# directories
dir_path = "/Users/ayush/Desktop/BeautSoupCrawlerDining/scripts"
date_path = os.path.join(dir_path, "date.txt")
chroma_path = os.path.join(dir_path, "ChromaClient")

chroma_client = chromadb.PersistentClient(path=chroma_path)
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

dateText = ""

try:
    with open(date_path, 'r', encoding='utf-8') as file:
        dateText = file.read()
except FileNotFoundError:
    dateText = ""

today = date.today()
date_string = today.strftime("%Y-%m-%d")

collection = None

if (date_string != dateText):

    with open(date_path, 'w') as date_file:
        date_file.write(date_string)
    
    try:

        dining_halls = scrape_vt_dining_locations("https://foodpro.students.vt.edu/menus/")

        chroma_client = chromadb.PersistentClient(path=chroma_path)
        collection = chroma_client.get_or_create_collection("Dining_Collection")

        current_id = 0

        for hall in dining_halls:
            hall_dict = get_item_and_metadata(hall)
            current_id = process_data(collection, hall_dict, current_id)
        
        query = input("What are your nutrition goals for today?\n>>>")
        query_func(query, collection)

    except Exception as e:
        print(f"Error updating dining information: {e}")
else:
    chroma_client = chromadb.PersistentClient(path=chroma_path)
    collection = chroma_client.get_collection("Dining_Collection")
app = Flask(__name__)

@app.route('/')

def home():
    return render_template('index.html')

@app.route('/api/query', methods = ['POST'])
def query():
    data = request.json
    query_text = data.get('query', '')

    if not query_text:
        return jsonify({'response':'Please enter a query'}), 400
    else:
        return jsonify({'response': query_func(query_text, collection)})

if __name__ == '__main__':

    port = int(os.environ.get('PORT', 5000))

    app.run(host='0.0.0.0', port=port, debug=False)


#query = input("What are your nutrition goals for today? (Enter 'q' to quit)\n>>>")

#while query.lower() != 'q':

    #query_func(query, collection)
    #query = input("\nAny further questions? (Enter 'q' to quit)\n>>>")

#print("I hope this information helped!")