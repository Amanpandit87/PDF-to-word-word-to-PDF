import streamlit as st
from pdf2docx import Converter
from docx2pdf import convert
import pikepdf
from pikepdf import Pdf
from glob import glob
import os
import shutil

st.set_page_config(page_title="Ultimate PDF Tool", layout="centered")
st.title("📂 Ultimate PDF Tool")

# Sidebar options
option = st.sidebar.selectbox("Choose Operation", (
    "PDF to Word",
    "Word to PDF",
    "Rotate PDF (180°)",
    "Add Password to PDF",
    "Split PDF into Pages",
    "Merge Multiple PDFs",
    "Reverse PDF Pages",
    "Delete Pages from PDF",
    "Replace PDF Page"
))

st.markdown("---")

# 1. PDF to Word
if option == "PDF to Word":
    file = st.file_uploader("Upload PDF file", type=["pdf"])
    if file and st.button("Convert to Word"):
        with open("input.pdf", "wb") as f:
            f.write(file.read())
        cv = Converter("input.pdf")
        cv.convert("output.docx")
        cv.close()
        with open("output.docx", "rb") as f:
            st.download_button("Download Word File", f, "converted.docx")

# 2. Word to PDF
elif option == "Word to PDF":
    file = st.file_uploader("Upload Word file", type=["docx"])
    if file and st.button("Convert to PDF"):
        with open("input.docx", "wb") as f:
            f.write(file.read())
        convert("input.docx", "output.pdf")
        with open("output.pdf", "rb") as f:
            st.download_button("Download PDF File", f, "converted.pdf")

# 3. Rotate PDF
elif option == "Rotate PDF (180°)":
    file = st.file_uploader("Upload PDF to Rotate", type=["pdf"])
    if file and st.button("Rotate and Download"):
        with open("rotate.pdf", "wb") as f:
            f.write(file.read())
        pdf = pikepdf.Pdf.open("rotate.pdf")
        for page in pdf.pages:
            page.Rotate = 180
        pdf.save("rotated.pdf")
        with open("rotated.pdf", "rb") as f:
            st.download_button("Download Rotated PDF", f, "rotated.pdf")

# 4. Password Protect PDF
elif option == "Add Password to PDF":
    file = st.file_uploader("Upload PDF", type=["pdf"])
    user_pwd = st.text_input("Set User Password", type="password")
    owner_pwd = st.text_input("Set Owner Password", type="password")
    if file and st.button("Encrypt PDF"):
        with open("protect.pdf", "wb") as f:
            f.write(file.read())
        pdf = pikepdf.Pdf.open("protect.pdf")
        perms = pikepdf.Permissions(extract=False)
        pdf.save("protected.pdf", encryption=pikepdf.Encryption(
            user=user_pwd, owner=owner_pwd, allow=perms
        ))
        with open("protected.pdf", "rb") as f:
            st.download_button("Download Protected PDF", f, "protected.pdf")

# 5. Split PDF into Pages
elif option == "Split PDF into Pages":
    file = st.file_uploader("Upload PDF to Split", type=["pdf"])
    if file and st.button("Split PDF"):
        with open("split.pdf", "wb") as f:
            f.write(file.read())
        pdf = pikepdf.Pdf.open("split.pdf")
        filenames = []
        for i, page in enumerate(pdf.pages):
            new_pdf = pikepdf.Pdf.new()
            new_pdf.pages.append(page)
            filename = f"page_{i+1}.pdf"
            new_pdf.save(filename)
            filenames.append(filename)
        for fname in filenames:
            with open(fname, "rb") as f:
                st.download_button(f"Download {fname}", f, fname)

# 6. Merge PDFs
elif option == "Merge Multiple PDFs":
    uploaded_files = st.file_uploader("Upload PDFs to Merge", type=["pdf"], accept_multiple_files=True)
    if uploaded_files and st.button("Merge PDFs"):
        merge_dir = "merge_temp"
        os.makedirs(merge_dir, exist_ok=True)
        for i, file in enumerate(uploaded_files):
            with open(f"{merge_dir}/file_{i}.pdf", "wb") as f:
                f.write(file.read())
        pdfs = glob(f"{merge_dir}/*.pdf")
        merged = pikepdf.Pdf.new()
        for pdf in pdfs:
            merged.pages.extend(pikepdf.Pdf.open(pdf).pages)
        merged.save("merged.pdf")
        shutil.rmtree(merge_dir)
        with open("merged.pdf", "rb") as f:
            st.download_button("Download Merged PDF", f, "merged.pdf")

# 7. Reverse PDF
elif option == "Reverse PDF Pages":
    file = st.file_uploader("Upload PDF to Reverse", type=["pdf"])
    if file and st.button("Reverse and Download"):
        with open("reverse.pdf", "wb") as f:
            f.write(file.read())
        pdf = Pdf.open("reverse.pdf")
        pdf.pages.reverse()
        pdf.save("reversed.pdf")
        with open("reversed.pdf", "rb") as f:
            st.download_button("Download Reversed PDF", f, "reversed.pdf")

# 8. Delete Specific Pages
elif option == "Delete Pages from PDF":
    file = st.file_uploader("Upload PDF", type=["pdf"])
    pages_to_delete = st.text_input("Enter page numbers to delete (e.g. 1,2)", value="1")
    if file and st.button("Delete Pages"):
        with open("del.pdf", "wb") as f:
            f.write(file.read())
        pdf = pikepdf.Pdf.open("del.pdf")
        pages = list(map(int, pages_to_delete.split(',')))
        for p in sorted(pages, reverse=True):
            del pdf.pages[p-1]
        pdf.save("deleted.pdf")
        with open("deleted.pdf", "rb") as f:
            st.download_button("Download Modified PDF", f, "deleted.pdf")

# 9. Replace Page in PDF
elif option == "Replace PDF Page":
    file = st.file_uploader("Upload PDF", type=["pdf"])
    replace_index = st.number_input("Replace Page Number (e.g. 3)", min_value=1, step=1)
    source_index = st.number_input("With Content of Page Number (e.g. 1)", min_value=1, step=1)
    if file and st.button("Replace and Download"):
        with open("rep.pdf", "wb") as f:
            f.write(file.read())
        pdf = pikepdf.Pdf.open("rep.pdf")
        if replace_index <= len(pdf.pages) and source_index <= len(pdf.pages):
            pdf.pages[replace_index-1] = pdf.pages[source_index-1]
            pdf.save("replaced.pdf")
            with open("replaced.pdf", "rb") as f:
                st.download_button("Download Replaced PDF", f, "replaced.pdf")
        else:
            st.error("Invalid page numbers.")
