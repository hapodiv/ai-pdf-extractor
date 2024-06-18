import fitz  # PyMuPDF
import requests
from flask import Flask, request, jsonify
import logging

import openai
import markdown

from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()



# Initialize Flask app
app = Flask(__name__)

# Configure logging to log to a file and the console
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

# Ollama server details
OLLAMA_SERVER_URL = os.getenv("OLLAMA_BASE_URL")

# Get the OpenAI API key from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Define a prompt template for structured data extraction
prompt_template_text = """
Extract the following structured financial information from the provided text:
- Total GAAP Revenue
- Total Gross Profit
- Total Net Income (Loss)
- Total Adjusted EBITDA
- E-commerce Revenue
- Digital Financial Services Revenue
- Digital Entertainment Revenue
- E-commerce Gross Orders
- E-commerce GMV

Text: {text}

Structured Data:

### Fourth Quarter 2023 Highlights
| Metric                    | Q4 2022 (USD)     | Q4 2023 (USD)     | Year-on-Year Growth (%) |
| **Total GAAP Revenue**    |                   |                   |                         |

### Full Year 2023 Highlights
| Metric                    | FY 2022 (USD)     | FY 2023 (USD)     | Year-on-Year Growth (%) |
| **Total GAAP Revenue**    |                   |                   |                         |

### Segment-Specific Revenue and Adjusted EBITDA for Full Year 2023
| Segment                     | Revenue (USD)      | Adjusted EBITDA (USD) |
| **E-commerce**              |                    |                       |

"""

def extract_text_from_pdf(pdf_file, from_page, to_page):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""
    for page_num in range(from_page - 1, to_page):  # pages are zero-indexed in PyMuPDF
        page = doc.load_page(page_num)
        text += page.get_text()
    logging.debug(f"Extracted text from pages {from_page} to {to_page}: {text[:500]}...")  # Log the first 500 characters of the text
    return text


def query_ollama(text):
    payload = {
        "model": "codellama",  # or the model you are using
        "prompt": prompt_template_text.format(text=text),
        "stream": False
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(OLLAMA_SERVER_URL + "/api/generate", json=payload, headers=headers)
    response.raise_for_status()
    logging.debug(f"Ollama response: {response}")  # Log the response
    return response

def query_openai(text):
    openai.api_key = OPENAI_API_KEY
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt_template_text.format(text=text)},
        ],
        max_tokens=1000,
        temperature=0.7,
    )
    logging.debug(f"OpenAI response: {response.choices[0].message['content'].strip()}")  # Log the response
    return response.choices[0].message['content'].strip()

@app.route('/')
def upload_file():
    return '''
    <!doctype html>
    <title>Upload PDF</title>
    <h1>Upload PDF file</h1>
    <form method="post" action="/extract" enctype="multipart/form-data">
      <input type="file" name="file"><br><br>
      <label for="from_page">From page:</label>
      <input type="number" name="from_page" min="1" required><br><br>
      <label for="to_page">To page:</label>
      <input type="number" name="to_page" min="1" required><br><br>
    
      <label for="api_choice">Choose API:</label>
      <select name="api_choice" required>
        <option value="ollama">Ollama</option>
        <option value="openai">OpenAI</option>
      </select><br><br>
      <input type="submit" value="Upload">
    </form>
    '''

@app.route('/extract', methods=['POST'])
def extract_data():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    from_page = request.form.get('from_page', type=int)
    to_page = request.form.get('to_page', type=int)
    api_choice = request.form.get('api_choice')
    
    if from_page is None or to_page is None or from_page < 1 or to_page < 1:
        return jsonify({"error": "Invalid page range"}), 400

    logging.debug(f"Received file: {file.filename}, from page: {from_page}, to page: {to_page}, API choice: {api_choice}")

    if file:
        pdf_text = extract_text_from_pdf(file, from_page, to_page)
        if api_choice == 'ollama':
            response = query_ollama(pdf_text)
            return response, 200  # Render the response
        elif api_choice == 'openai':
            response = query_openai(pdf_text)
            return markdown.markdown(response), 200  # Render the response
        else:
            return jsonify({"error": "Invalid API choice"}), 400
    else:
        return jsonify({"error": "No file part"}), 400
       


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

