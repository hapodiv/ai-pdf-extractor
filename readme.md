# AI PDF Extractor

This project is a Flask-based web application that allows users to upload PDF files, extract financial information from specific pages, and process the text using either OpenAI's GPT model or an Ollama server. The extracted information is returned as structured data in JSON format.

## Features

- Upload PDF files and specify page ranges for text extraction.
- Extract structured financial information using OpenAI's GPT-3.5-turbo model.
- Option to use an Ollama server for text processing.
- Securely load API keys from a `.env` file.
- Detailed logging for easy debugging.

## Prerequisites

- Python 3.6 or higher
- Pip (Python package installer)
- OpenAI API key
- Ollama server

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/hapodiv/ai-pdf-extractor.git
    cd ai-pdf-extractor
    ```

2. **Create and activate a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Create a `.env` file in the project root directory and add your OpenAI API key:**

    ```plaintext
    OPENAI_API_KEY=your-openai-api-key
    OLLAMA_BASE_URL="http://ollama.local:11434"
    ```

## Usage

1. **Start the Flask application:**

    ```bash
    python app.py
    ```

2. **Access the application:**

    Open your web browser and navigate to `http://<your_server_ip>:5000/`.

3. **Upload a PDF file:**

    - Choose a PDF file from your local machine.
    - Specify the page range to extract text from.
    - Select the API for processing (OpenAI or Ollama).
    - Click the "Upload" button.

4. **View the extracted data:**

    The application will process the PDF and return the extracted financial information as a structured JSON response.

## Project Structure

- `app.py`: Main Flask application code.
- `requirements.txt`: Python dependencies.
- `.env`: Environment variables file (not included in the repository, create it manually).
- `templates/`: HTML templates for the web interface.
- `static/`: Static files (CSS, JS).

## Logging

The application logs detailed information to `app.log` and the console. This includes debug information about PDF text extraction, API requests, and responses.


## Acknowledgments

- [OpenAI](https://www.openai.com/) for the GPT model.
- [LangChain](https://github.com/langchain/langchain) for the text processing tools.
- [Flask](https://flask.palletsprojects.com/) for the web framework.
- [PyMuPDF](https://pymupdf.readthedocs.io/) for PDF text extraction.
- [python-dotenv](https://github.com/theskumar/python-dotenv) for managing environment variables.
