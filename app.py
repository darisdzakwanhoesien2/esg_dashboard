import streamlit as st
from components import upload_panel, pdf_viewer, text_viewer, pagination_controls
from components import dashboard_summary

def main():
    st.set_page_config(page_title="PDF Text Analytics", layout="wide")

    st.sidebar.title("Controls")
    pdf_file, csv_file = upload_panel.render()

    if pdf_file and csv_file:
        pagination_controls.render()
        col1, col2 = st.columns([1, 1])
        with col1:
            pdf_viewer.render(pdf_file)
        with col2:
            csv_file.seek(0) # Reset file pointer
            text_viewer.render(csv_file)

        st.markdown("---")
        csv_file.seek(0) # Reset file pointer again for dashboard_summary
        dashboard_summary.render(csv_file)

if __name__ == "__main__":
    main()