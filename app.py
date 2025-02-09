import os
from flask import Flask, request, jsonify, send_from_directory
import tempfile
import shutil

from PyPDF2 import PdfReader
from PIL import Image
import easyocr

# Gemini API integration
from google import genai

app = Flask(__name__, static_url_path='', static_folder='static')

# (Optional) If you're on Windows, set the Tesseract executable path:
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_from_pdf(file_path):
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
        return text
    except Exception as e:
        return f"Error extracting text from PDF: {e}"

def extract_text_from_image(file_path):
    try:
        # Initialize the reader with the language(s) you need (e.g., English)
        reader = easyocr.Reader(['en'])
        # Read text from the image without bounding box details
        result = reader.readtext(file_path, detail=0)
        # Join the returned list of text lines into one string
        extracted_text = "\n".join(result)
        return extracted_text
    except Exception as e:
        return f"Error extracting text from image with EasyOCR: {e}"

def generate_with_gemini(prompt: str) -> str:
    try:
        # Either set the GEMINI_API_KEY environment variable or replace the string below.
        api_key = os.environ.get("GEMINI_API_KEY", "AIzaSyAilvGFzQPS6zi1VYLtLHCNyJuNPuncmfg")
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Error generating content: {e}"

def parse_flashcards(flashcards_text: str):
    """
    Parses the flashcards text into an array of objects.
    Expected format:
      "Q: What is the main topic?\nA: Answer text\n\nQ: What is an important detail?\nA: Answer text"
    """
    cards = []
    flashcard_blocks = flashcards_text.strip().split("\n\n")
    for block in flashcard_blocks:
        lines = block.split("\n")
        if len(lines) >= 2:
            question = lines[0].replace("Q:", "").strip()
            answer = lines[1].replace("A:", "").strip()
            cards.append({"question": question, "answer": answer})
    return cards

@app.route('/')
def index():
    # Serve the index.html file from the static folder.
    return send_from_directory('static', 'index.html')

@app.route('/analyze-notes', methods=['POST'])
def analyze_notes():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    # Save the uploaded file to a temporary directory.
    temp_dir = tempfile.mkdtemp()
    file_path = os.path.join(temp_dir, file.filename)
    file.save(file_path)

    extracted_text = ""
    if file.filename.lower().endswith('.pdf'):
        extracted_text = extract_text_from_pdf(file_path)
    elif file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
        extracted_text = extract_text_from_image(file_path)
    else:
        extracted_text = "Unsupported file type."

    # Check that some text was extracted.
    if not extracted_text.strip():
        shutil.rmtree(temp_dir)
        return jsonify({"error": "No text could be extracted from the file."}), 400

    # Prepare Gemini API prompts with improved instructions.
    summary_prompt = (
        f"Analyze the following text carefully and provide a comprehensive, detailed summary. "
        f"Your summary should include:\n"
        f"- An overview of the main topics and key points.\n"
        f"- Clear definitions of important terms and concepts.\n"
        f"- Any relevant formulas or equations (if applicable) with brief explanations.\n"
        f"- Examples or illustrative details to clarify the content.\n\n"
        f"Please present the summary in plain text, structured into clear, well-organized paragraphs, "
        f"and avoid using any markdown formatting (such as asterisks, underscores, or bullet points).\n\n"
        f"Text:\n{extracted_text}"
    )

    flashcards_prompt = (
        f"From the following text, generate a list of flashcards to aid in studying the material. "
        f"For each flashcard, provide a concise question and a clear, informative answer. "
        f"Each flashcard should follow this exact format:\n"
        f"Q: [Question]\nA: [Answer]\n\n"
        f"Ensure that your output is in plain text without any markdown formatting or extra symbols. "
        f"Focus on key concepts, definitions, and details that are critical to understanding the text.\n\n"
        f"Text:\n{extracted_text}"
    )

    exam_questions_prompt = (
        f"Review the following text and generate a set of exam questions that comprehensively assess the reader's understanding. "
        f"The questions should cover key definitions, core concepts, examples, and any formulas mentioned in the text. "
        f"Present each question on a new line in plain text without using markdown formatting or bullet points. "
        f"Make sure the questions are clear, challenging, and directly relevant to the content provided.\n\n"
        f"Text:\n{extracted_text}"
    )

    # Generate content using Gemini.
    summary = generate_with_gemini(summary_prompt)
    flashcards_text = generate_with_gemini(flashcards_prompt)
    exam_questions = generate_with_gemini(exam_questions_prompt)

    # Parse the flashcards into a structured list.
    flashcards = parse_flashcards(flashcards_text)

    # Clean up temporary files.
    shutil.rmtree(temp_dir)

    return jsonify({
        "extracted_text": extracted_text,
        "summary": summary,
        "flashcards": flashcards,
        "questions": exam_questions
    })

if __name__ == '__main__':
    app.run(debug=True)
