import pdfplumber

OCR_MIN_CHARS = 50

# Checks whether the file is scanned or digital
def check_pdf_type(file):
    for page in file.pages[:5]:
        text = (page.extract_test() or '').strip()
        if len(text) >= OCR_MIN_CHARS:
            return "digital"
    return "scanned"

def extract_text(file):
    pages = []

    for i, page in enumerate(file.pages):
        text = (page.extract_text() or "").strip()
        if text:
            pages.append({"page": i+1, "text": text})

    return pages