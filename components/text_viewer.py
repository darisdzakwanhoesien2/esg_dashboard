import streamlit as st
import pandas as pd

@st.cache_data(show_spinner=False)
def _load_csv(csv_bytes: bytes) -> pd.DataFrame:
    # Cache by file bytes to avoid re-parsing on every rerun.
    # Streamlit reruns the script frequently; without caching, reading CSVs
    # becomes the dominant latency in the UI.
    return pd.read_csv(pd.io.common.BytesIO(csv_bytes))

def render(csv_file):
    csv_bytes = csv_file.getvalue()
    df = _load_csv(csv_bytes)
    current_page = st.session_state.get("current_page", 1)
    if "page_number" not in df.columns or "extracted_text" not in df.columns:
        st.error("CSV must include 'page_number' and 'extracted_text' columns.")
        return

    page_data = df[df["page_number"] == current_page]

    st.subheader(f"Page {current_page}")
    if not page_data.empty:
        st.text_area(
            "Extracted Text",
            str(page_data["extracted_text"].iloc[0]),
            height=700,
        )
    else:
        st.warning("No text available for this page.")
