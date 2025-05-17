import modal
import subprocess
import time
from modal import build, enter, method

app = modal.App("VT-Dining-Assistant")
image = modal.Image.debian_slim().apt_install(
    "curl"
).pip_install(
    "flask",
    "chromadb",
    "datetime",
    "beautifulsoup4",
    "ollama"
).add_local_python_source(
    "scraper",
    "LLM_stuff",
    copy=True
).add_local_dir("/Users/ayush/Desktop/BeautSoupCrawlerDining/scripts", remote_path="/root", copy=True
    ).run_commands(
    "curl -fsSL https://ollama.com/install.sh | sh",
    "ollama serve &"
)

@app.function(image=image)
@modal.concurrent(max_inputs=100)
@modal.wsgi_app()
def flask_app():
    import chromadb
    from datetime import date
    import os
    from scraper import scrape_vt_dining_locations, get_item_and_metadata
    from LLM_stuff import query_func, process_data
    from flask import Flask, request, jsonify, render_template

    dir_path = "/Users/ayush/Desktop/BeautSoupCrawlerDining/scripts"
    date_path = os.path.join(dir_path, "date.txt")
    chroma_path = os.path.join(dir_path, "ChromaClient")

    chroma_client = chromadb.PersistentClient(path=chroma_path)

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
            
            #query = input("What are your nutrition goals for today?\n>>>")
            #query_func(query, collection)

        except Exception as e:
            print(f"Error updating dining information: {e}")
    else:
        chroma_client = chromadb.PersistentClient(path=chroma_path)
        collection = chroma_client.get_collection("Dining_Collection")
    
    web_app = Flask(__name__)

    @web_app.route('/')
    def home():
        print(f"The current directory is {os.getcwd()}")
        print(f"{os.listdir()}")        
        return render_template('index.html')

    @web_app.route('/api/query', methods = ['POST'])
    def query():
        data = request.json
        query_text = data.get('query', '')

        if not query_text:
            return jsonify({'response':'Please enter a query'}), 400
        else:
            return jsonify({'response': query_func(query_text, collection)})

    
    return web_app
    #if __name__ == '__main__':

        #port = int(os.environ.get('PORT', 5050))

        #app.run(host='0.0.0.0', port=port, debug=False)

        
