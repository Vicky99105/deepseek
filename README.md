# Resume Analyzer

An AI-powered resume analysis tool that provides detailed insights about skills, experience, education, and ATS compatibility.

## 🚀 Features
- Skills Analysis
- Experience Evaluation
- Education Assessment
- Improvement Suggestions
- ATS Compatibility Check
- Response Time Tracking
- Downloadable Reports

## 📋 Prerequisites

1. **Install Ollama**
   - For Mac/Linux: Download from [Ollama.ai](https://ollama.ai)
   - After installation, ensure Ollama is running (check for the icon in menu bar)

2. **Install Required Model**
   ```bash
   # Pull the Deepseek Coder model (recommended)
   ollama pull deepseek-coder
   
   # OR pull the Deepseek R1 1.5B model (larger but more comprehensive)
   ollama pull deepseek-r1:1.5b
   ```

## 🛠️ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/resume-analyzer.git
   cd resume-analyzer
   ```

2. Install required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   streamlit run resume_analyzer.py
   ```

## 💻 Usage

1. Ensure Ollama is running
2. Start the Streamlit app
3. Upload a PDF resume
4. Select desired analysis aspects
5. Get detailed analysis with response times
6. Download complete report if needed

## ⚙️ Models
- **Deepseek Coder**: Faster, lighter model (recommended)
- **Deepseek R1 1.5B**: More comprehensive but slower

## 📝 Note
- Ensure your resume is in PDF format
- Analysis time may vary based on the model selected and resume length
- Keep Ollama running while using the application

## 🤝 Contributing
Pull requests are welcome! For major changes, please open an issue first.

## 📄 License
[MIT](https://choosealicense.com/licenses/mit/) 