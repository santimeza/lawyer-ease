import pdfplumber
import os

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file using pdfplumber."""
    text = ''
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            page_text = page.extract_text()
            if page_text:
                print(f"[✓] Page {i+1} extracted.")
                text += page_text + "\n"
            else:
                print(f"[!] Page {i+1} has no extractable text.")
    return text

def main():
    # Path to the PDF file
    pdf_path = 'test1.pdf'
    print(f"Reading PDF from: {pdf_path}")

    # Extract text from the PDF
    text = extract_text_from_pdf(pdf_path)

    print("---- Extracted Text ----")
    print(text)

if __name__ == "__main__":
    main()
