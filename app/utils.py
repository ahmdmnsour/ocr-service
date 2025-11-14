import os
import pytesseract
from pdf2image import convert_from_path
from docx import Document
from PIL import Image

def process_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    text = ""

    if ext in [".jpg", ".jpeg", ".png", ".bmp"]:
        text = pytesseract.image_to_string(Image.open(file_path))
    elif ext == ".pdf":
        images = convert_from_path(file_path)
        for img in images:
            text += pytesseract.image_to_string(img) + "\n"
    elif ext == ".docx":
        doc = Document(file_path)
        text = "\n".join([p.text for p in doc.paragraphs])
    else:
        raise ValueError("Unsupported file type")

    return chunk_text(text)

def chunk_text(text, chunk_size=20):
    text = text.strip()
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]