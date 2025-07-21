````markdown
# JSONExtract: Invoice Data Extractor

JSONExtract is a powerful tool designed to automate the extraction of key information from invoice documents. It takes invoices in image or PDF format and returns structured data, such as invoice numbers, dates, and total amounts, in a clean and ready-to-use JSON format.

The application features two distinct extraction pipelines: a traditional OCR approach using Tesseract and an advanced method leveraging a Large Language Model (LLM) for higher accuracy. The entire system is exposed through a REST API built with FastAPI and includes a simple React frontend for easy interaction and demonstration.

## ✨ Features

* **Dual Extraction Engines**: Choose between a fast Tesseract-based engine and a highly accurate LLM-based engine (Llama 3.2 Vision).
* **Multi-Format Support**: Process both image files (JPG, PNG) and multi-page PDF documents.
* **Structured JSON Output**: All extracted data is formatted into clean, predictable JSON, perfect for downstream processing.
* **REST API**: A robust FastAPI backend provides endpoints for seamless integration into other applications or workflows.
* **Interactive Frontend**: A user-friendly React web interface allows for easy uploading and visualization of extraction results.
* **Database Integration**: Save extracted invoice data directly to a SQLite database for persistence and management.

---

## 🛠️ Technology Stack

* **Backend**: Python, FastAPI
* **LLM Engine**: Ollama, Llama 3.2 Vision
* **OCR Engine**: Tesseract, Pytesseract
* **Database**: SQLite, SQLAlchemy
* **PDF Processing**: pdf2image
* **Frontend**: React
* **Data Processing**: OpenCV, spaCy

---

## ⚙️ How It Works

The application offers two methods for data extraction:

### Tesseract Based Extraction
This method uses a traditional OCR pipeline.
1.  **Image Preprocessing**: The input image undergoes several preprocessing steps to improve OCR accuracy, including grayscaling, thresholding to convert to black and white, automatic rotation correction, resizing, and noise reduction.
2.  **Text Recognition**: `pytesseract` is then used to perform OCR on the cleaned image, converting it into raw text.
3.  **Information Extraction**: The resulting text is parsed using regular expressions and the `spaCy` NLP library to identify and extract the `invoice_number`, `invoice_date`, and `amount`.

### LLM Based Extraction (Recommended)
This method leverages a vision-capable Large Language Model for more robust and accurate extraction, noted for its higher accuracy at the cost of higher latency.
1.  **Model Interaction**: The application uses **Ollama** to serve a local instance of the `llama3.2-vision` model.
2.  **Prompt Engineering**: A specific prompt is sent to the model along with the invoice image. This prompt instructs the LLM to act as a data extraction expert and return only the `invoice_number`, `invoice_date`, and `amount` in a raw JSON format.
3.  **JSON Parsing**: The model's response, which is the clean JSON string, is parsed and sent back to the user.

---

## 🚀 Installation and Setup

To get the project running locally, please follow these steps.

### Prerequisites
Ensure you have the following installed on your system and added to your system's PATH.
* **Python 3.8+**
* **Node.js and npm**
* **Tesseract OCR**: Download and install from the [official repository](https://github.com/tesseract-ocr/tesseract). Remember to add the installation directory to your system's PATH.
* **Poppler**: Required for PDF processing.
    * **Windows**: Download the latest release and add the `\bin` folder to your PATH.
    * **macOS (via Homebrew)**: `brew install poppler`
    * **Linux (Debian/Ubuntu)**: `sudo apt-get install poppler-utils`
* **Ollama**: Required for the LLM-based extraction. [Download and install Ollama](https://ollama.com/).

### Backend Setup
1.  **Clone the repository**:
    ```bash
    git clone <your-repo-url>
    cd <your-repo-directory>
    ```
2.  **Set up a Python virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```
3.  **Install Python dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Pull the LLM model using Ollama**:
    ```bash
    ollama pull llama3.2-vision:latest
    ```

### Frontend Setup
1.  **Navigate to the frontend directory**:
    ```bash
    cd frontend  # Or your frontend app's directory name
    ```
2.  **Install npm packages**:
    ```bash
    npm install
    ```

---

## ▶️ Usage

### Running the Application
1.  **Start the Backend API**: From the project's root directory, run the FastAPI server.
    ```bash
    uvicorn api:app --host 0.0.0.0 --port 8000 --reload
    ```
2.  **Start the Frontend App**: In the frontend directory, run the React development server.
    ```bash
    npm start
    ```
3.  **Access the Application**: Open your web browser and navigate to `http://localhost:3000`.

### Using the Interface
1.  Select either the **Tesseract** or **LLM (Recommended)** extraction method.
2.  Click **"Browse..."** to upload an invoice image or PDF file.
3.  Click the **"Extract"** button to begin processing.
4.  The extracted data will appear in the **JSON** output box.
5.  You can then **"Download JSON"** or **"Save JSON To Database"**.

### API Endpoints
The API is available at `http://localhost:8000` and provides the following endpoints:

* `POST /tesseract/extract`: Upload a file for extraction using the Tesseract engine.
* `POST /llm/extract`: Upload a file for extraction using the LLM engine.
* `POST /invoices/`: Save a list of extracted invoices to the database.
* `GET /invoices/`: Retrieve a list of all saved invoices.
* `DELETE /invoices/{invoice_id}`: Delete a specific invoice from the database by its ID.

````
