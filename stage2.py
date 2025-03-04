import streamlit as st
import PyPDF2

st.set_page_config(page_title="Resume Analyzer", page_icon="📄")
st.title("📄 Resume Analyzer")
st.write("Upload your resume and get insights")

uploaded_file = st.file_uploader("Upload Resume (PDF)", type="pdf")

if uploaded_file:
    st.write("File uploaded successfully!")
    # Read the PDF file using PyPDF2
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    resume_text = " ".join(page.extract_text() for page in pdf_reader.pages)
    st.text_area("Resume Text Preview", resume_text, height=250)
