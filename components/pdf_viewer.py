import streamlit as st
import base64

# Optional dependency for better PDF rendering in deployed apps
try:
    from streamlit_pdf_viewer import pdf_viewer
    HAS_PDF_VIEWER = True
except ImportError:
    HAS_PDF_VIEWER = False


def render(pdf_file):
    if not pdf_file:
        st.info("Please upload a PDF file to view.")
        return

    # Read the PDF file bytes
    pdf_bytes = pdf_file.read()

    # Always provide a download option
    st.download_button(
        label="📄 Download PDF",
        data=pdf_bytes,
        file_name=pdf_file.name if hasattr(pdf_file, "name") else "document.pdf",
        mime="application/pdf",
        use_container_width=True
    )

    # --- Option 1: Use Streamlit PDF Viewer if available ---
    if HAS_PDF_VIEWER:
        st.caption("Using Streamlit PDF Viewer (recommended for hosted apps)")
        pdf_viewer(pdf_bytes)
        return

    # --- Option 2: Try inline iframe (local base64 rendering) ---
    try:
        base64_pdf = base64.b64encode(pdf_bytes).decode("utf-8")

        # Warn if file is too large for data URI
        if len(base64_pdf) > 5 * 1024 * 1024:
            st.warning("PDF too large to embed directly in browser. Use the download button above instead.")
            return

        # Embed PDF inline
        pdf_display = f"""
        <iframe 
            src="data:application/pdf;base64,{base64_pdf}" 
            width="100%" 
            height="800" 
            type="application/pdf"
            style="border:none;"
        ></iframe>
        """
        st.markdown(pdf_display, unsafe_allow_html=True)

    except Exception as e:
        # --- Option 3: Fallback message ---
        st.error(f"Unable to render PDF inline. Reason: {str(e)}")
        st.info("Click 'Download PDF' above to open it locally.")
