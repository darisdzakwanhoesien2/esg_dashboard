import streamlit as st
import pandas as pd

def render():
    pdf_file = st.file_uploader("Upload PDF", type=["pdf"])
    csv_file = st.file_uploader("Upload Extracted Text (CSV)", type=["csv"])
    
    if csv_file:
        df = pd.read_csv(csv_file)
        if "page_number" not in df.columns or "extracted_text" not in df.columns:
            st.error("CSV must include 'page_number' and 'extracted_text' columns.")
            return None, None
    
    return pdf_file, csv_file
