import streamlit as st
from langchain_ollama import OllamaLLM
import PyPDF2
import io
import time

# Set page config
st.set_page_config(
    page_title="Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# Initialize Ollama with specific parameters
@st.cache_resource
def load_model(model_name="deepseek-coder"):
    """Load the specified model. Defaults to deepseek-coder if not specified"""
    return OllamaLLM(
        model=model_name,
        temperature=0.7,
        timeout=60,
        stop=["</s>", "Human:", "Assistant:"]
    )

def extract_text_from_pdf(pdf_file):
    """Extract text from uploaded PDF file"""
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text.strip()

def analyze_resume(text, aspect, model_name="deepseek-coder"):
    """Analyze resume with specified model and track response time"""
    llm = load_model(model_name)
    
    prompts = {
        "skills": "Analyze the following resume and list all technical and soft skills mentioned. Format the output in bullet points:\n\nResume:\n",
        "experience": "Analyze the following resume and evaluate the work experience. Provide insights about career progression and key achievements:\n\nResume:\n",
        "education": "Analyze the following resume and evaluate the educational background. Comment on the relevance and strength of the education:\n\nResume:\n",
        "improvements": "Analyze the following resume and suggest specific improvements. Format suggestions in bullet points:\n\nResume:\n",
        "ats": "Analyze if this resume is ATS (Applicant Tracking System) friendly and provide specific suggestions for improvement:\n\nResume:\n"
    }
    
    try:
        max_length = 2000
        if len(text) > max_length:
            text = text[:max_length] + "..."
        
        prompt = prompts[aspect] + text
        
        with st.spinner(f"Analyzing {aspect}..."):
            start_time = time.time()  # Start timing
            response = llm.invoke(prompt)
            end_time = time.time()  # End timing
            
            if not response:
                return "Analysis failed. Please try again.", 0
            
            response_time = round(end_time - start_time, 2)  # Calculate response time
            return response.strip(), response_time
            
    except Exception as e:
        st.error(f"Error during analysis: {str(e)}")
        return f"Error during analysis: {str(e)}", 0

def format_report(analysis_results):
    """Format the analysis results in a nice looking report"""
    st.markdown("## 📊 Detailed Analysis Report")
    
    # Skills Section
    st.markdown("### 🎯 Skills")
    st.markdown(analysis_results["skills"][0])  # [0] is the response text
    st.caption(f"⚡ Response time: {analysis_results['skills'][1]} seconds")
    st.divider()
    
    # Experience Section
    st.markdown("### 💼 Work Experience")
    st.markdown(analysis_results["experience"][0])
    st.caption(f"⚡ Response time: {analysis_results['experience'][1]} seconds")
    st.divider()
    
    # Education Section
    st.markdown("### 🎓 Education")
    st.markdown(analysis_results["education"][0])
    st.caption(f"⚡ Response time: {analysis_results['education'][1]} seconds")
    st.divider()
    
    # Improvements Section
    st.markdown("### 📈 Suggested Improvements")
    st.markdown(analysis_results["improvements"][0])
    st.caption(f"⚡ Response time: {analysis_results['improvements'][1]} seconds")
    st.divider()
    
    # ATS Compatibility Section
    st.markdown("### 🤖 ATS Compatibility")
    st.markdown(analysis_results["ats"][0])
    st.caption(f"⚡ Response time: {analysis_results['ats'][1]} seconds")
    
    # Total time calculation
    total_time = sum(result[1] for result in analysis_results.values())
    st.markdown(f"### ⏱️ Total Analysis Time: {round(total_time, 2)} seconds")

# Main UI
st.title("📄 Resume Analyzer")
st.write("Upload your resume and get detailed analysis on various aspects")

# Model selection
model_options = {
    "Deepseek Coder (Recommended)": "deepseek-coder",
    "Deepseek R1 1.5B": "deepseek-r1:1.5b",
}
selected_model = st.selectbox(
    "Select Model",
    options=list(model_options.keys()),
    index=0
)

uploaded_file = st.file_uploader("Upload your resume (PDF format)", type="pdf")

if uploaded_file is not None:
    # Extract text from PDF
    with st.spinner("Extracting text from PDF..."):
        resume_text = extract_text_from_pdf(uploaded_file)
    
    # Create tabs for different analyses
    tabs = st.tabs(["Skills", "Experience", "Education", "Improvements", "ATS Compatibility"])
    
    # Dictionary to store analysis results
    analysis_results = {}
    
    with tabs[0]:
        st.header("Skills Analysis")
        if st.button("Analyze Skills"):
            response, resp_time = analyze_resume(resume_text, "skills", model_options[selected_model])
            analysis_results["skills"] = (response, resp_time)
            st.write(response)
            st.caption(f"⚡ Response time: {resp_time} seconds")
    
    with tabs[1]:
        st.header("Experience Analysis")
        if st.button("Analyze Experience"):
            response, resp_time = analyze_resume(resume_text, "experience", model_options[selected_model])
            analysis_results["experience"] = (response, resp_time)
            st.write(response)
            st.caption(f"⚡ Response time: {resp_time} seconds")
    
    with tabs[2]:
        st.header("Education Analysis")
        if st.button("Analyze Education"):
            response, resp_time = analyze_resume(resume_text, "education", model_options[selected_model])
            analysis_results["education"] = (response, resp_time)
            st.write(response)
            st.caption(f"⚡ Response time: {resp_time} seconds")
    
    with tabs[3]:
        st.header("Suggested Improvements")
        if st.button("Get Improvements"):
            response, resp_time = analyze_resume(resume_text, "improvements", model_options[selected_model])
            analysis_results["improvements"] = (response, resp_time)
            st.write(response)
            st.caption(f"⚡ Response time: {resp_time} seconds")
    
    with tabs[4]:
        st.header("ATS Compatibility")
        if st.button("Check ATS Compatibility"):
            response, resp_time = analyze_resume(resume_text, "ats", model_options[selected_model])
            analysis_results["ats"] = (response, resp_time)
            st.write(response)
            st.caption(f"⚡ Response time: {resp_time} seconds")

    # Generate Complete Report
    if st.button("Generate Complete Report"):
        with st.spinner("Generating complete report..."):
            # Analyze any missing sections
            for aspect in ["skills", "experience", "education", "improvements", "ats"]:
                if aspect not in analysis_results:
                    response, resp_time = analyze_resume(resume_text, aspect, model_options[selected_model])
                    analysis_results[aspect] = (response, resp_time)
            
            # Format and display the report
            format_report(analysis_results)
            
            # Create downloadable report
            report_text = f"""Resume Analysis Report

🎯 Skills: (Response time: {analysis_results["skills"][1]} seconds)
{analysis_results["skills"][0]}

💼 Work Experience: (Response time: {analysis_results["experience"][1]} seconds)
{analysis_results["experience"][0]}

🎓 Education: (Response time: {analysis_results["education"][1]} seconds)
{analysis_results["education"][0]}

📈 Suggested Improvements: (Response time: {analysis_results["improvements"][1]} seconds)
{analysis_results["improvements"][0]}

🤖 ATS Compatibility: (Response time: {analysis_results["ats"][1]} seconds)
{analysis_results["ats"][0]}

⏱️ Total Analysis Time: {round(sum(result[1] for result in analysis_results.values()), 2)} seconds
"""
            
            st.download_button(
                label="Download Analysis Report",
                data=report_text,
                file_name="resume_analysis.txt",
                mime="text/plain"
            )
