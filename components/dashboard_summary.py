import streamlit as st
from components import extraction_quality, keyword_visuals, wordcloud_visuals

def render(csv_file):
    st.subheader("📊 Analytics Dashboard")
    tabs = st.tabs(["Extraction Quality", "Keywords", "Word Cloud"])
    
    with tabs[0]:
        extraction_quality.render(csv_file)
    with tabs[1]:
        keyword_visuals.render(csv_file)
    with tabs[2]:
        wordcloud_visuals.render(csv_file)
