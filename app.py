import streamlit as st
from components import upload_panel, pdf_viewer, text_viewer, pagination_controls
from components import dashboard_summary

def main():
    st.set_page_config(page_title="PDF Text Analytics", layout="wide")

    st.sidebar.title("Controls")
    pdf_file, csv_file = upload_panel.render()

    if pdf_file and csv_file:
        # Derive total pages from the CSV so navigation reflects real content.
        # This also protects against a hard-coded total page count.
        try:
            csv_bytes = csv_file.getvalue()
            df = text_viewer._load_csv(csv_bytes)
            total_pages = int(df["page_number"].max()) if not df.empty else 1
        except Exception:
            total_pages = 1

        pagination_controls.render(total_pages=total_pages)
        col1, col2 = st.columns([1, 1])
        with col1:
            pdf_viewer.render(pdf_file)
        with col2:
            text_viewer.render(csv_file)

        st.markdown("---")
        dashboard_summary.render(csv_file)

if __name__ == "__main__":
    main()
