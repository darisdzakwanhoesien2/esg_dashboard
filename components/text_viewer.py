import streamlit as st
import pandas as pd

def render(csv_file):
    df = pd.read_csv(csv_file)
    current_page = st.session_state.get("current_page", 1)
    page_data = df[df["page_number"] == current_page]

    st.subheader(f"Page {current_page}")
    if not page_data.empty:
        st.text_area("Extracted Text", page_data["extracted_text"].iloc[0], height=700)
    else:
        st.warning("No text available for this page.")
