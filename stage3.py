import streamlit as st
from langchain_ollama import OllamaLLM
import PyPDF2

st.set_page_config(page_title="Resume Analyzer", page_icon="📄")
st.title("📄 Resume Analyzer")
st.write("Upload your resume and get insights")
uploaded_file = st.file_uploader("Upload Resume (PDF)", type="pdf")

if uploaded_file:
    st.write("File uploaded successfully!")
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    resume_text = " ".join(page.extract_text() for page in pdf_reader.pages)
    st.text_area("Resume Text Preview", resume_text, height=250)

    # Analyze the resume text using OllamaLLM
    llm = OllamaLLM(model="deepseek-coder", temperature=0.2, timeout=45)
    if st.button("Analyze Resume"):
        with st.spinner("Analyzing..."):
            response = llm.invoke("Analyze this resume: " + resume_text)
            st.write("Analysis Result:")
            st.write(response)
