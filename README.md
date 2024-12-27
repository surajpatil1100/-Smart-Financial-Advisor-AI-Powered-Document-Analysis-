# Financial Advisor Chatbot

Overview

The Financial Advisor Chatbot is an intelligent tool designed to analyze uploaded financial documents, such as PDFs of balance sheets, income statements, or market analyses, and answer user queries based on the extracted content. The chatbot leverages Natural Language Processing (NLP) and machine learning to provide precise, context-aware responses, making financial data more accessible and actionable.

## Key Features

PDF Upload and Parsing: Users can upload financial documents in PDF format for automated text extraction.

Query System: An intuitive interface to ask questions related to the uploaded document.

Advanced NLP: Powered by Sentence-BERT for semantic understanding and context-aware answers.

Cosine Similarity Matching: Ensures relevant and accurate query responses based on document content.

Technologies Used

Backend: Flask (Python)

Frontend: HTML, CSS

Machine Learning Model: Sentence-BERT (all-MiniLM-L6-v2)

PDF Parsing: PyPDF2 (or equivalent)

Development Tools: Jupyter Notebook, VS Code

Installation

Prerequisites

Python 3.8+

Virtual Environment (optional but recommended)

Steps

## Clone the repository:

## git clone https://github.com/surajpatil1100/financial-advisor-chatbot.git
cd financial-advisor-chatbot

## Create and activate a virtual environment:

python -m venv finance_bot_venv
source finance_bot_venv/bin/activate  # On Windows: finance_bot_venv\Scripts\activate

## Install required dependencies:

pip install -r requirements.txt

## Run the Flask application:

python app/main.py

## Open the application in your browser:

http://127.0.0.1:5000

Usage

Upload a PDF: Use the provided button on the homepage to upload a financial PDF document.

Ask Queries: Once the document is processed, use the query window to ask questions about the document's content.

Get Answers: The chatbot will analyze your query and return the most relevant information from the document.

Folder Structure

## financial-advisor-chatbot/
|
|-- app/
|   |-- main.py        # Main application script
|   |-- templates/     # HTML templates for Flask
|   |-- static/        # CSS, JS, and other static assets
|-- data/
|   |-- raw/           # Uploaded PDF files
|   |-- processed/     # Extracted text files
|-- requirements.txt   # Python dependencies
|-- README.md          # Project documentation

## Future Enhancements

Support for Multiple Document Formats: Extend support for Excel, Word, and CSV files.

Improved Answer Accuracy: Integrate advanced models like GPT for more nuanced responses.

Data Visualization: Add charts and graphs to represent extracted financial metrics visually.

Authentication: Secure the application with user authentication.

Contribution

Contributions are welcome! To contribute:

## Fork the repository.

 Create a new branch for your feature or bug fix.

 Submit a pull request with a detailed description of your changes.

License

This project is licensed under the MIT License.

Contact

For any questions or feedback, feel free to reach out:

Name: Suraj Patil


Note: This chatbot is for educational purposes and not intended for production deployment without further enhancements.


