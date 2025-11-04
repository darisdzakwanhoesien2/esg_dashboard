import os
import pandas as pd

DATA_DIR = "data/extracted_text"
PDF_DIR = "data/documents"

def list_available_documents():
    pdfs = [f for f in os.listdir(PDF_DIR) if f.endswith(".pdf")]
    csvs = [f.replace("_text.csv", ".pdf") for f in os.listdir(DATA_DIR)]
    matched = [p for p in pdfs if p in csvs]
    return matched

def load_document_data(pdf_name):
    base_name = pdf_name.replace(".pdf", "")
    csv_path = os.path.join(DATA_DIR, f"{base_name}_text.csv")
    pdf_path = os.path.join(PDF_DIR, pdf_name)

    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"No matching CSV found for {pdf_name}")
    
    df = pd.read_csv(csv_path)
    return pdf_path, df
