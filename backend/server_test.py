from flask import Flask, request, jsonify, render_template
from langchain_community.vectorstores.chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.schema import Document
from flask_cors import CORS
import chardet
import os

app = Flask(__name__)
CORS(app)

# Initialize embeddings
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Database path and vector store initialization
db_dir = "./database"
processed_file = os.path.join(db_dir, "processed_data.txt")
vectorstore = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_data():
    global vectorstore
    file = request.files['file']
    file_path = os.path.join(db_dir, file.filename)
    file.save(file_path)

    # Detect file encoding and read the content
    with open(file_path, "rb") as f:
        raw_data = f.read()
        detected = chardet.detect(raw_data)
    encoding = detected["encoding"]

    # Read the file content
    with open(file_path, "r", encoding=encoding) as f:
        data = f.read().strip()

    # Split the content by lines
    lines = data.splitlines()

    # Save the processed data into the file
    with open(processed_file, "w", encoding="utf-8") as output_file:
        for line in lines:
            if line.strip():
                output_file.write(line.strip() + "\n")

    # Create Document objects
    documents = [Document(page_content=line.strip(), metadata={}) for line in lines if line.strip()]

    # Create the Chroma vector store (specifying the database directory)
    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=db_dir  # Specify the directory to save the vector store
    )
    vectorstore.persist()  # Save the vector store database to a file
    return jsonify({"message": "File uploaded successfully."})


@app.route('/search', methods=['POST'])
def search_data():
    global vectorstore
    if vectorstore is None:
        return jsonify({"error": "The vector store is not initialized. Please upload data first."})

    query_text = request.json.get('query', '')
    if not query_text:
        return jsonify({"error": "The query is empty."})

    print(f"Received query: {query_text}")  # Print query value (for debugging)

    # Create query embedding and perform search
    query_embedding = embeddings.embed_query(query_text)
    results = vectorstore.similarity_search_by_vector(embedding=query_embedding, k=5)

    # Filter search results
    unique_results = {}
    for result in results:
        content = result.page_content.strip()
        if content not in unique_results and content:
            unique_results[content] = result.metadata

    # Generate response
    if not unique_results:
        return jsonify({"message": "No search results found."})
    return jsonify({"results": [{"content": k, "metadata": v} for k, v in unique_results.items()]})

if __name__ == '__main__':
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)
    app.run(host='0.0.0.0', port=5000)
