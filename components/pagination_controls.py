import streamlit as st

def render():
    st.sidebar.subheader("Navigation")

    # Initialize session state variables if they don't exist
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = 1
    if "total_pages" not in st.session_state:
        st.session_state["total_pages"] = 10 # Default or calculate based on content

    current_page = st.session_state["current_page"]
    total_pages = st.session_state["total_pages"]

    col1, col2, col3 = st.sidebar.columns([1, 2, 1])
    if col1.button("◀ Previous") and current_page > 1:
        st.session_state["current_page"] -= 1
    col2.markdown(f"**Page {current_page}/{total_pages}**")
    if col3.button("Next ▶") and current_page < total_pages:
        st.session_state["current_page"] += 1