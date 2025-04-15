import pdfplumber
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
import difflib
import os

nltk.download('punkt')

def extract_text_from_pdf(pdf_path):
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

def normalize(text):
    return ' '.join(text.strip().split())

def group_word_diffs(words1, words2):
    """Group together adjacent changes as single diff chunks."""
    matcher = difflib.SequenceMatcher(None, words1, words2)
    result = []

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'equal':
            result.extend(words1[i1:i2])
        elif tag in ('replace', 'delete', 'insert'):
            removed = words1[i1:i2]
            added = words2[j1:j2]
            chunk = ''
            if removed and added:
                chunk = f"(-{' '.join(removed)} +{' '.join(added)})"
            elif removed:
                chunk = f"(-{' '.join(removed)})"
            elif added:
                chunk = f"(+{' '.join(added)})"
            result.append(chunk)

    return ' '.join(result)

def diff_sentences(sent1, sent2):
    """Compare two sentences word-by-word and group diffs."""
    words1 = word_tokenize(sent1)
    words2 = word_tokenize(sent2)
    return group_word_diffs(words1, words2)

def diff_text(file1, file2):
    text1 = extract_text_from_pdf(file1)
    text2 = extract_text_from_pdf(file2)

    sentences1 = [normalize(s) for s in sent_tokenize(text1)]
    sentences2 = [normalize(s) for s in sent_tokenize(text2)]

    matcher = difflib.SequenceMatcher(None, sentences1, sentences2)
    diffs = []
    structure_warning = False

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'equal':
            diffs.extend(sentences1[i1:i2])
        elif tag in ('replace', 'delete', 'insert'):
            for i in range(max(i2 - i1, j2 - j1)):
                s1 = sentences1[i1 + i] if i1 + i < i2 else ""
                s2 = sentences2[j1 + i] if j1 + i < j2 else ""
                if s1 and s2:
                    diffs.append(diff_sentences(s1, s2))
                elif s1:
                    structure_warning = True
                    diffs.append(f"[-] {s1}")
                elif s2:
                    structure_warning = True
                    diffs.append(f"[+] {s2}")

    return structure_warning, diffs

def main():
    # pdf_path_1 is the original PDF
    pdf_path_1 = 'rf-1.pdf'
    pdf_path_2 = 'rf-2.pdf'
    pdf_path_3 = 'rf-3.pdf'
    pdf_path_4 = 'rf-4.pdf'    

    structure_warning, diffs = diff_text(pdf_path_1, pdf_path_2)

    print("\n--- Sentence-Level Differences with Grouped Word Changes ---\n")
    # havent gotten this to happen yet. Consider removing
    if structure_warning:
        print("⚠️ WARNING: The documents aren't similar enough.\nPlease check that both PDFs are the same form.\n")

    for line in diffs:
        print(line)

if __name__ == "__main__":
    main()
