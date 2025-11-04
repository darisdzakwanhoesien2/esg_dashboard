import streamlit as st
import base64
# import tempfile # Removed as no longer needed
# import os # Removed as no longer needed

def render(pdf_file):
    if pdf_file:
        # Read the PDF file content as bytes
        pdf_bytes = pdf_file.read()

        # Encode the PDF bytes to base64
        base64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')

        # Check if the base64 string is excessively long (e.g., > 5MB equivalent)
        # This is a heuristic; actual limits vary by browser and system.
        if len(base64_pdf) > 5 * 1024 * 1024:
            st.warning("The PDF file is very large. Embedding it directly might cause performance issues or be blocked by browser limits. Consider offering a download option instead.")
            st.download_button(
                label="Download PDF",
                data=pdf_bytes,
                file_name=pdf_file.name,
                mime="application/pdf"
            )
        else:
            # Create the iframe HTML with the base64 data URI
            pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800" type="application/pdf"></iframe>'
            
            # Display the iframe using st.markdown with unsafe_allow_html=True
            # This is the standard way to embed custom HTML in Streamlit.
            st.markdown(pdf_display, unsafe_allow_html=True)