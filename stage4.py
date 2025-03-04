import streamlit as st
from langchain_ollama import OllamaLLM
import PyPDF2

st.set_page_config(page_title="Resume Analyzer", page_icon="📄")
st.title("📄 Resume Analyzer")
st.write("Upload your resume and get insights")
uploaded_file = st.file_uploader("Upload Resume (PDF)", type="pdf")

# Basic styling - just a few essential elements
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

if uploaded_file:
    st.write("File uploaded successfully!")
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    resume_text = " ".join(page.extract_text() for page in pdf_reader.pages)
    st.text_area("Resume Text Preview", resume_text, height=250)

    prompt = """
        List technical, soft skills, and projects from the given resume in the following structured and concise format with bullet points in new lines.
        • Technical Skills: \n
        • Soft Skills: \n
        • Projects: Problem statement, Technologies used, Key contributions \n
        Resume: \n
    """ + resume_text

    llm = OllamaLLM(model="deepseek-coder", temperature=0.2, timeout=45)
    if st.button("Analyze Resume"):
        with st.spinner("Analyzing..."):
            response = llm.invoke(prompt)
            st.header("🚀 Skills and Projects Analysis")
            st.write(response)
            st.info(f"Analysis completed.")
