from pypdf import PdfReader
import os

def load_pdf(pdf_path):
    reader = PdfReader(pdf_path)

    pages =[]

    for page_num, page in enumerate(reader.pages):

        text = page.extract_text()

        if text:

            pages.append({
                "text": text,
                "page": page_num+1
            })

    pdf_name = os.path.basename(pdf_path)

    metadata = reader.metadata

    author = "Unknown"

    if metadata and metadata.author:
        author = metadata.author

    return {
        "pdf_name": pdf_name,
        "author": author,
        "pages":pages
    }