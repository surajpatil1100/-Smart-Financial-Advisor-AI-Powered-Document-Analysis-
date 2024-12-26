import os
from PyPDF2 import PdfReader
import spacy

# Load spaCy model for NLP tasks
nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(file_path):
    """
    Extracts text from a PDF file.
    
    Args:
        file_path (str): Path to the PDF file.
    
    Returns:
        str: Extracted text from the PDF.
    """
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        raise RuntimeError(f"Failed to parse PDF: {str(e)}")

def save_extracted_text(text, output_path):
    """
    Saves the extracted text to a file.
    
    Args:
        text (str): Extracted text.
        output_path (str): Path to save the text file.
    """
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(text)

def process_query(query, text):
    """
    Function to process the user's query and find the most relevant part of the extracted text.
    
    Args:
        query (str): The user's query.
        text (str): The extracted text from the PDF.
    
    Returns:
        str: The most relevant portion of the extracted text.
    """
    # Process both the query and the extracted text
    query_doc = nlp(query)
    text_doc = nlp(text)

    # We'll use a simple similarity score (cosine similarity) between the query and text
    max_similarity = 0
    best_match = None

    # Compare the query with each sentence in the text
    for sent in text_doc.sents:
        similarity = query_doc.similarity(sent)
        if similarity > max_similarity:
            max_similarity = similarity
            best_match = sent.text

    return best_match if best_match else "Sorry, no relevant information found."
