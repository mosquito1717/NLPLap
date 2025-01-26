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

    import re
    # 시간 정규식
    time_pattern = re.compile(r'\[(\d{2}:\d{2})\]')

    # 결과 저장용 딕셔너리
    time_based_data = {}

    # 시간 태그로 데이터 분리
    segments = time_pattern.split(data)

    for i in range(1, len(segments), 2):
        time = segments[i]  # [hh:mm] 시간 값
        text = segments[i + 1].strip('"; ')  # 텍스트 정리 (앞뒤 불필요한 문자 제거)

        if time in time_based_data:
            time_based_data[time].append(text)
        else:
            time_based_data[time] = [text]

    # Save the processed data into the file
    with open(processed_file, "w", encoding="utf-8") as output_file:
        for time, texts in time_based_data.items():
            output_file.write(f"[{time}] " + " ".join(texts) + "\n")

    # Create Document objects
    documents = [Document(page_content=text.strip(), metadata={"time": time}) 
                 for time, texts in time_based_data.items() for text in texts if text.strip()]

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

    # 쿼리 텍스트를 임베딩 변환
    query_embedding = embeddings.embed_query(query_text)

    # 벡터 기반 유사도 검색 (유사한 상위 5개 문서 검색)
    search_results = vectorstore.similarity_search_by_vector(embedding=query_embedding, k=5)

    # 결과 처리 (타임스탬프 단위로 그룹화)
    grouped_results = {}
    for result in search_results:
        content = result.page_content.strip()
        metadata = result.metadata

        time = metadata.get("time", "Unknown Time")  # 메타데이터에서 시간 추출
        if time not in grouped_results:
            grouped_results[time] = []
        
        grouped_results[time].append(content)

    # 중복 제거 및 응답 생성
    response_data = []
    for time, texts in grouped_results.items():
        combined_text = " ".join(texts)  # 동일 타임스탬프의 내용을 결합
        list(set(combined_text))
        response_data.append({
            "timestamp": time,
            "content": combined_text
        })

    # 검색 결과가 없을 경우 처리
    if not response_data:
        return jsonify({"message": "No search results found."})
    
    print(f"Number of search results: {len(response_data)}")
    return jsonify({"results": response_data})

if __name__ == '__main__':
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)
    app.run(host='0.0.0.0', port=5000)
