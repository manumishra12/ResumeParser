# ResumeParser

This is a **basic resume parser** that extracts structured data from `.pdf`, `.docx`, and `.txt` resumes using the **Google Gemini API**. It outputs the parsed resume in **JSON format**.

---

### 🧩 Features

- Supports `.pdf`, `.docx`, and `.txt` resume files
- Uses **Google Gemini API** for intelligent parsing
- Outputs structured JSON with:
  - Name, Email, Phone
  - Skills
  - Summary
  - Education & Work History
- Saves output to a JSON file
- No `textract` used (uses `PyMuPDF`, `python-docx`)

---

### 📦 Requirements

Install dependencies:
```bash
pip install google-generativeai pymupdf python-docx
```

### 📁 File Structure
resume_parser/
│
├── resume_parser.py     # Main script
├── requirements.txt     # Python dependencies
├── sample_resume.pdf    # Sample input file
└── README.md            # This file

### 🔧 Setup Instructions

Step 1: Clone or create the project:

```bash
git clone https://github.com/your-username/resume-parser.git 
cd resume-parser
```

Step 2: Install dependencies
```bash
pip install -r requirements.txt
```

Step 3: Set up your Gemini API key
```bash
GEMINI_API_KEY = "YOUR_API_KEY_HERE"
```

Or use environment variables:
```bash
export GEMINI_API_KEY="YOUR_API_KEY_HERE"
```

### ▶️ How to Run
```bash
python parser.py
Streamlit run Streamlit_app.py
```
