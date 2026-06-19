from pypdf import PdfReader
import os


def load_all_pdfs(folder_path):

    all_pages =[]

    for file_name in os.listdir(folder_path):

        if file_name.endswith(".pdf"):

            pdf_path = os.path.join(
                folder_path,
                file_name
            )


            reader = PdfReader(pdf_path)

            for page_num, page in enumerate(reader.pages):

                text = page.extract_text()

                if text:

                    all_pages.append({
                        "text":text,
                        "page": page_num +1,
                        "pdf_name": file_name,
                        "author": "Unknown"
                    })
    return all_pages