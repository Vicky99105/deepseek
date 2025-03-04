import streamlit as st
from langchain_ollama import OllamaLLM
import PyPDF2
import time

# Simple page config
st.set_page_config(page_title="Resume Analyzer", page_icon="📄")

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

# Simple header
st.title("📄 Resume Analyzer")
st.write("### Upload your resume and get AI-powered analysis")

# Model selection - only one option available
model_option = "deepseek-coder"

# File upload
uploaded_file = st.file_uploader("Upload Resume (PDF)", type="pdf")

# Define section for Skills and Projects together
SECTION = {
    "Skills and Projects": {
        "title": "Skills and Projects Analysis",
        "icon": "🚀",
        "prompt": """List technical, soft skills, and projects from the given resume in the following structured and concise format with bullet points in new lines.
• Technical Skills:
• Soft Skills:
• Projects: Problem statement, Technologies used, Key contributions \n
Resume: \n """ 
    }
}

def analyze_resume(text, aspect, model_name):
    """Analyze resume with optimized settings"""
    llm = OllamaLLM(
        model=model_name,
        temperature=0.2,
        timeout=45,
    )
    
    try:
        text = text[:1000] + "..." if len(text) > 1500 else text
        
        with st.spinner(f"Analyzing {aspect}..."):
            start_time = time.time()
            response = llm.invoke(SECTION[aspect]["prompt"] + text)
            resp_time = round(time.time() - start_time, 2)
            
            if not response or len(response) < 10:
                return "Analysis failed. Please try again.", 0
                
            return response.strip(), resp_time
            
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return f"Analysis failed: {str(e)}", 0

if uploaded_file:
    # Read PDF
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    resume_text = " ".join(page.extract_text() for page in pdf_reader.pages)
    
    # Analyze on button click
    if st.button("Analyze Resume"):
        response, time_taken = analyze_resume(resume_text, "Skills and Projects", model_option)
        st.header("🚀 Skills and Projects Analysis")
        st.write(response)
        st.info(f"⚡ Time taken: {time_taken} seconds")