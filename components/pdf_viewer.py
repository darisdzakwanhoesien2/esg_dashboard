import streamlit as st
import base64

def render(pdf_file):
    if pdf_file:
        base64_pdf = base64.b64encode(pdf_file.read()).decode('utf-8')
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)
