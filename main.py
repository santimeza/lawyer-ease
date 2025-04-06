import pdfplumber
import re
from difflib import SequenceMatcher
from reportlab.pdfgen import canvas
import os

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file using pdfplumber."""
    with pdfplumber.open(pdf_path) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text()
    return text