import sys
import os
from flask import Flask, request, jsonify, render_template
from pdf_parser import extract_text_from_pdf, save_extracted_text
from sentence_transformers import SentenceTransformer
import numpy as np

# Add parent directory to the path to avoid module import errors
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Define folder paths
UPLOAD_FOLDER = "data/raw/"
PROCESSED_FOLDER = "data/processed/"

# Check if the directory exists and is a directory
if not os.path.isdir(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

if not os.path.isdir(PROCESSED_FOLDER):
    os.makedirs(PROCESSED_FOLDER, exist_ok=True)

# Initialize Flask app
app = Flask(__name__)

# Configure the template folder
app.template_folder = "templates"

# Load the pre-trained Sentence-BERT model for embedding queries and documents
model = SentenceTransformer('all-MiniLM-L6-v2')

# Helper function: Convert text into vectors using Sentence-BERT
def get_text_vector(text):
    """Converts text into a vector using Sentence-BERT"""
    return model.encode(text)

# Helper function: Compare cosine similarity between query and document
def compare_similarity(query_vector, document_vector):
    """Compute cosine similarity between query and document"""
    cosine_sim = np.dot(query_vector, document_vector) / (np.linalg.norm(query_vector) * np.linalg.norm(document_vector))
    return cosine_sim

@app.route('/')
def index():
    """
    Serve the main HTML page.
    """
    return render_template("index.html")

@app.route('/upload', methods=['POST'])
def upload_pdf():
    """
    Endpoint to upload a PDF and extract its text.
    """
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    pdf_file = request.files['file']
    if not pdf_file.filename.endswith('.pdf'):
        return jsonify({"error": "Only PDF files are allowed"}), 400

    # Define the file path
    file_path = os.path.join(UPLOAD_FOLDER, pdf_file.filename)

    # If the file already exists, delete it
    if os.path.exists(file_path):
        os.remove(file_path)

    # Save the new uploaded file
    pdf_file.save(file_path)
    
    # Extract text from the saved PDF
    try:
        extracted_text = extract_text_from_pdf(file_path)
        output_path = os.path.join(PROCESSED_FOLDER, f"{os.path.splitext(pdf_file.filename)[0]}.txt")
        save_extracted_text(extracted_text, output_path)
        return jsonify({"message": "PDF processed successfully", "text_file": output_path}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/query', methods=['POST'])
def query_pdf():
    """
    Endpoint to query the extracted text from the uploaded PDF using cosine similarity and Sentence-BERT.
    """
    query = request.json.get('query')
    if not query:
        return jsonify({"error": "No query provided"}), 400

    # Path to the extracted text file (use the same filename as the uploaded PDF)
    text_file_path = os.path.join(PROCESSED_FOLDER, "FL.txt")

    # Check if the text file exists
    if not os.path.exists(text_file_path):
        return jsonify({"error": "No extracted text found for this PDF"}), 404

    # Load the extracted text
    with open(text_file_path, 'r', encoding='utf-8') as file:
        extracted_text = file.read()

    # Split text into chunks or lines
    text_chunks = extracted_text.split('\n')

    # Convert query and document chunks into vectors
    query_vector = get_text_vector(query)
    text_vectors = [get_text_vector(chunk) for chunk in text_chunks]

    # Compute cosine similarity for each chunk
    similarities = [compare_similarity(query_vector, text_vector) for text_vector in text_vectors]

    # Find the chunk with the highest similarity
    max_similarity_index = np.argmax(similarities)
    max_similarity = similarities[max_similarity_index]

    # If the similarity is above a certain threshold, return the response
    if max_similarity > 0.7:
        return jsonify({
            "query": query,
            "response": text_chunks[max_similarity_index],
            "similarity": max_similarity
        }), 200
    else:
        return jsonify({"error": "No relevant information found for your query."}), 404

if __name__ == "__main__":
    app.run(debug=True)
