import streamlit as st
from langchain_ollama import OllamaLLM
import PyPDF2
import time

# Simple page config
st.set_page_config(page_title="Resume Analyzer", page_icon="📄", layout="wide")

# Just the essential styling for larger text
st.markdown("""
    <style>
    h1 {font-size: 3rem}
    h2 {font-size: 2rem}
    .stButton>button {width: 100%}
    </style>
""", unsafe_allow_html=True)

# Main title
st.markdown("# 📄 Resume Analyzer")
st.write("Upload your resume and get AI-powered analysis")

# Model selection
model_options = {
    "Deepseek Coder (Fast)": "deepseek-coder",
    "Deepseek R1 1.5B (Detailed)": "deepseek-r1:1.5b",
}
selected_model = st.selectbox("Choose Model", options=list(model_options.keys()))

# File upload
uploaded_file = st.file_uploader("Upload Resume (PDF)", type="pdf")

# Analysis sections
SECTIONS = {
    "skills": {
        "title": "Skills Analysis",
        "icon": "🎯",
        "prompt": """Analyze the following resume for skills. 
First, think through the analysis (wrap your thinking in <think> tags). 
Then, provide a clean, bullet-pointed list of:
- Technical Skills
- Soft Skills

Resume:\n"""
    },
    "experience": {
        "title": "Experience Analysis",
        "icon": "💼",
        "prompt": """Analyze the work experience in this resume.
First, think through the analysis (wrap your thinking in <think> tags).
Then, provide a clear summary of:
- Key roles
- Achievements
- Career progression

Resume:\n"""
    },
    "education": {
        "title": "Education Analysis",
        "icon": "🎓",
        "prompt": """Analyze the educational background.
First, think through the analysis (wrap your thinking in <think> tags).
Then, summarize:
- Degrees
- Institutions
- Academic achievements

Resume:\n"""
    },
    "improvements": {
        "title": "Suggested Improvements",
        "icon": "📈",
        "prompt": """Suggest improvements for this resume.
First, think through the analysis (wrap your thinking in <think> tags).
Then, list 3-5 specific improvements.

Resume:\n"""
    },
    "ats": {
        "title": "ATS Compatibility",
        "icon": "🤖",
        "prompt": """Check if this resume is ATS-friendly.
First, think through the analysis (wrap your thinking in <think> tags).
Then, list:
- ATS compatibility score
- Main issues
- Quick fixes

Resume:\n"""
    }
}

def analyze_resume(text, aspect, model_name):
    """Analyze resume and track response time"""
    llm = OllamaLLM(
        model=model_name,
        temperature=0.7,
        timeout=60,
    )
    
    try:
        # Truncate long text
        text = text[:2000] + "..." if len(text) > 2000 else text
        
        with st.spinner(f"Analyzing {aspect}..."):
            start_time = time.time()
            response = llm.invoke(SECTIONS[aspect]["prompt"] + text)
            resp_time = round(time.time() - start_time, 2)
            
            # Handle thinking process
            if "<think>" in response:
                thinking, result = response.split("</think>")
                with st.expander("Show Analysis Process"):
                    st.write(thinking.replace("<think>", "").strip())
                return result.strip(), resp_time
            
            return response.strip(), resp_time
            
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return f"Analysis failed: {str(e)}", 0

if uploaded_file:
    # Read PDF
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    resume_text = " ".join(page.extract_text() for page in pdf_reader.pages)
    
    # Create tabs
    tabs = st.tabs([f"{s['icon']} {s['title']}" for s in SECTIONS.values()])
    results = {}
    
    for tab, (key, section) in zip(tabs, SECTIONS.items()):
        with tab:
            st.markdown(f"## {section['icon']} {section['title']}")
            if st.button(f"Analyze {section['title']}", key=key):
                response, time_taken = analyze_resume(
                    resume_text, 
                    key, 
                    model_options[selected_model]
                )
                results[key] = (response, time_taken)
                st.write(response)
                st.info(f"⚡ Time taken: {time_taken} seconds")
    
    # Complete report button
    if st.button("Generate Complete Report"):
        st.markdown("## 📊 Complete Analysis")
        
        for key, section in SECTIONS.items():
            if key not in results:
                response, time_taken = analyze_resume(
                    resume_text, 
                    key, 
                    model_options[selected_model]
                )
                results[key] = (response, time_taken)
            
            st.markdown(f"## {section['icon']} {section['title']}")
            st.write(results[key][0])
            st.info(f"⚡ Time taken: {results[key][1]} seconds")
            st.divider()
        
        total_time = sum(time for _, time in results.values())
        st.success(f"Total analysis time: {round(total_time, 2)} seconds")
