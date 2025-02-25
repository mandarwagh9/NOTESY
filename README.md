
# NOTESY

NOTESY is a modern, minimalist web application that analyzes your notes (from PDFs and images) and leverages the Gemini 2.0 Flash API to generate detailed summaries, interactive flashcards, and exam-style questions. Built with a Flask backend and a pure HTML, CSS, and JavaScript frontend, NOTESY offers downloadable outputs for convenient study and review.

## Features

- **Text Extraction:**  
  Extracts text from PDFs and image files using PyPDF2, Pillow, and pytesseract.
  
- **Detailed Summaries:**  
  Uses the Gemini 2.0 Flash API to generate comprehensive summaries that include important definitions, formulas, examples, and key points—all formatted as clear, plain text.

- **Interactive Flashcards:**  
  Generates flashcards in a Q&A format with a smooth flip animation for an engaging study experience.

- **Exam Questions:**  
  Creates exam-style questions covering key concepts, definitions, and examples to help test your understanding.

- **Downloadable Outputs:**  
  Easily download the generated summary, flashcards, and exam questions as well-formatted PDF files.

## Technologies Used

- **Backend:** Flask, PyPDF2, Pillow, pytesseract, google-genai  
- **Frontend:** HTML, CSS, JavaScript, jsPDF (for PDF generation)  
- **AI Integration:** Gemini 2.0 Flash API

## Getting Started

### Prerequisites

- **Python 3.9+**  
- **Tesseract OCR:**  
  - **Windows:** [Download Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki)  
  - **macOS:** Install via Homebrew: `brew install tesseract`  
  - **Linux:** Install via your package manager (e.g., `sudo apt-get install tesseract-ocr`)

### Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/mandarwagh9/NOTESY.git
   cd NOTESY
   ```

2. **Create and Activate a Virtual Environment (optional but recommended):**

   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install the Required Dependencies:**

   ```bash
   pip install Flask PyPDF2 Pillow pytesseract google-genai
   ```

4. **Set Up Your Gemini API Key:**

   Either export your API key as an environment variable:

   ```bash
   export GEMINI_API_KEY="your_gemini_api_key_here"
   ```

   Or (for testing only) replace `"YOUR_GEMINI_API_KEY"` in `app.py` with your actual API key.

### Running the Application

1. **Start the Flask Backend:**

   ```bash
   python app.py
   ```

   The app will run on [http://127.0.0.1:5000](http://127.0.0.1:5000).

2. **Open Your Web Browser:**

   Navigate to [http://127.0.0.1:5000](http://127.0.0.1:5000).

3. **Upload and Analyze:**

   - Select a PDF or image file containing your notes.
   - Click **"Upload and Analyze"**.
   - View the generated detailed summary, interactive flashcards, and exam questions.
   - Download each section as a PDF if desired.

## Project Structure

```
NOTESY/
├── app.py            # Flask backend code
└── static/
    ├── index.html    # Main HTML file
    ├── style.css     # CSS for modern, minimalist styling
    ├── script.js     # JavaScript for interactions and PDF downloads
    └── logo.png      # OpenLabs logo for branding
```

## Contributing

Contributions are welcome! If you'd like to improve NOTESY, please fork the repository, make your changes, and submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgements

- [Gemini 2.0 Flash API](https://developers.google.com/genai)
- [Flask](https://flask.palletsprojects.com/)
- [PyPDF2](https://pypi.org/project/PyPDF2/)
- [Pillow](https://pillow.readthedocs.io/)
- [pytesseract](https://pypi.org/project/pytesseract/)
- [jsPDF](https://github.com/parallax/jsPDF)
- Thanks to OpenAI for the inspiration and branding.
