import streamlit as st
from functions import extract_text_by_page, extract_fields

st.set_page_config(page_title="PDF Data Extractor", layout="wide")

st.title("PDF Data Extractor")

uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file:
    st.success("File uploaded successfully!")

    st.write("Filename:", uploaded_file.name)
    st.write("File size:", uploaded_file.size, "bytes")

    text = extract_text_by_page(uploaded_file)

    st.subheader("Extracted Text")
    with st.expander("View Extracted Text"):
        for page in text:
            st.write(f"Page {page['page']}")
            st.text(page["raw_text"])

    st.subheader("Data Table")
    data = extract_fields(text)
    with st.expander("Extracted Data"):
        st.json(data)

    st.subheader("Graphs")
    st.info("Graphs will appear here...")

