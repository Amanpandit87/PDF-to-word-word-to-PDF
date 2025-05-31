import streamlit as st
from pdf2docx import Converter
from docx2pdf import convert
import os

st.set_page_config(page_title="PDF ↔ Word Converter", layout="centered")
st.title("📄 PDF ↔ Word Converter Tool")

# Option selector
option = st.selectbox("Select Conversion Type", ("PDF to Word", "Word to PDF"))

# File uploader based on selected option
if option == "PDF to Word":
    uploaded_file = st.file_uploader("Upload PDF file", type=["pdf"])
    if uploaded_file:
        with open("input.pdf", "wb") as f:
            f.write(uploaded_file.read())

        if st.button("Convert to Word"):
            st.info("Converting PDF to Word...")
            pdf_file = "input.pdf"
            word_file = "output.docx"
            try:
                cv = Converter(pdf_file)
                cv.convert(word_file)
                cv.close()

                with open(word_file, "rb") as f:
                    st.success("Conversion Successful!")
                    st.download_button("Download Word File", f, file_name="converted.docx")
            except Exception as e:
                st.error(f"Error: {e}")

elif option == "Word to PDF":
    uploaded_file = st.file_uploader("Upload Word file", type=["docx"])
    if uploaded_file:
        with open("input.docx", "wb") as f:
            f.write(uploaded_file.read())

        if st.button("Convert to PDF"):
            st.info("Converting Word to PDF...")
            word_file = "input.docx"
            pdf_file = "output.pdf"
            try:
                convert(word_file, pdf_file)

                with open(pdf_file, "rb") as f:
                    st.success("Conversion Successful!")
                    st.download_button("Download PDF File", f, file_name="converted.pdf")
            except Exception as e:
                st.error(f"Error: {e}")

# Cleanup after app stops (Optional)
if st.button("Clear Temp Files"):
    try:
        os.remove("input.pdf")
        os.remove("input.docx")
        os.remove("output.docx")
        os.remove("output.pdf")
        st.success("Temporary files cleared.")
    except:
        st.warning("Some files were not found or already deleted.")
