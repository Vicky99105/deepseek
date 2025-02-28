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
st.write("Upload your resume and get AI-powered analysis")

# Model selection - simplified options
model_options = {
    "Deepseek Coder (Fast)": "deepseek-coder",
    "Deepseek R1 1.5B (Detailed)": "deepseek-r1:1.5b",
}
selected_model = st.selectbox("Choose Model", options=list(model_options.keys()))

# File upload
uploaded_file = st.file_uploader("Upload Resume (PDF)", type="pdf")

# Updated SECTIONS with more direct prompts
SECTIONS = {
    "skills": {
        "title": "Skills Analysis",
        "icon": "🎯",
        "prompt": """List skills from this resume:
• Technical Skills: Programming languages, frameworks, tools, etc.
• Soft Skills: Communication, teamwork, problem-solving, etc.

Resume:\n"""
    },
    "experience": {
        "title": "Experience Analysis",
        "icon": "💼",
        "prompt": """List for each job:
• Role & Company 
• Key Achievements

Resume:\n"""
    },
    "education": {
        "title": "Education Analysis",
        "icon": "🎓",
        "prompt": """List education:
• Degrees
• Institutions
• Years & Grades

Resume:\n"""
    },
    "improvements": {
        "title": "Suggested Improvements",
        "icon": "📈",
        "prompt": """List 3 quick improvements:
• Content:
• Format:
• Impact:

Resume:\n"""
    },
    "ats": {
        "title": "ATS Compatibility",
        "icon": "🤖",
        "prompt": """Quick ATS check:
• Issues:
• Fixes:

Resume:\n"""
    }
}

def analyze_resume(text, aspect, model_name):
    """Analyze resume with optimized settings"""
    llm = OllamaLLM(
        model=model_name,
        temperature=0.2,  # Reduced temperature for faster, more focused responses
        timeout=45,  # Reduced timeout
    )
    
    try:
        # Reduce text length more aggressively
        text = text[:1500] + "..." if len(text) > 1500 else text
        
        with st.spinner(f"Analyzing {aspect}..."):
            start_time = time.time()
            response = llm.invoke(SECTIONS[aspect]["prompt"] + text)
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
    
    # Create tabs and analyze
    tabs = st.tabs([f"{s['icon']} {s['title']}" for s in SECTIONS.values()])
    results = {}
    
    for tab, (key, section) in zip(tabs, SECTIONS.items()):
        with tab:
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
        st.header("📊 Complete Analysis")
        
        # Analyze missing sections
        for key, section in SECTIONS.items():
            if key not in results:
                response, time_taken = analyze_resume(
                    resume_text, 
                    key, 
                    model_options[selected_model]
                )
                results[key] = (response, time_taken)
            
            # Display results
            st.subheader(f"{section['icon']} {section['title']}")
            st.write(results[key][0])
            st.info(f"⚡ Time taken: {results[key][1]} seconds")
            st.divider()
        
        # Total time
        total_time = sum(time for _, time in results.values())
        st.success(f"Total analysis time: {round(total_time, 2)} seconds")