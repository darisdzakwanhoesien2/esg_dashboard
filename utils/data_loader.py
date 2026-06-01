import os
import pandas as pd

DATA_DIR = "data/extracted_text"
PDF_DIR = "data/documents"

def list_available_documents():
    """
    Return PDF filenames that have a corresponding extracted-text CSV.

    Expected convention:
      - PDF: <name>.pdf
      - CSV: <name>_text.csv
    """
    if not os.path.isdir(PDF_DIR) or not os.path.isdir(DATA_DIR):
        return []

    pdfs = {f for f in os.listdir(PDF_DIR) if f.lower().endswith(".pdf")}
    csv_bases = {
        f[: -len("_text.csv")]
        for f in os.listdir(DATA_DIR)
        if f.lower().endswith("_text.csv")
    }
    matched = sorted([pdf for pdf in pdfs if pdf[:-4] in csv_bases])
    return matched

def load_document_data(pdf_name):
    base_name = pdf_name.replace(".pdf", "")
    csv_path = os.path.join(DATA_DIR, f"{base_name}_text.csv")
    pdf_path = os.path.join(PDF_DIR, pdf_name)

    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"No matching CSV found for {pdf_name}")
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"Missing PDF file: {pdf_name}")
    
    df = pd.read_csv(csv_path)
    return pdf_path, df
