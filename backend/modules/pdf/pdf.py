import os
import fitz

def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as pdf_document:
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            text += page.get_text()
    return text

def extract_text_from_pdfs_in_folder(folder_path):
    folder_contents = os.listdir(folder_path)
    pdf_files = [file for file in folder_contents if file.endswith(".pdf")]
    all_texts = []
    for pdf_file in pdf_files:
        pdf_path = os.path.join(folder_path, pdf_file)
        text = extract_text_from_pdf(pdf_path)
        all_texts.append(text)
    return all_texts

# Replace "Data" with the path to your folder containing PDF files
folder_texts = extract_text_from_pdfs_in_folder("Data")

# Printing texts from all PDFs in the folder
for text in folder_texts:
    print(text)