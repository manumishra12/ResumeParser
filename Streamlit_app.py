import streamlit as st
import google.generativeai as genai
import fitz 
from docx import Document
import json
import os
from dotenv import load_dotenv


load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)


st.set_page_config(page_title="Resume Parser", layout="wide")
st.title("📄 Resume Parser")

# Helper: Extract text from uploaded file
def extract_text_from_file(file):
    file_type = os.path.splitext(file.name)[1].lower()

    if file_type == ".pdf":
        with fitz.open(stream=file.read(), filetype="pdf") as doc:
            text = ""
            for page in doc:
                text += page.get_text()
            return text

    elif file_type == ".docx":
        doc = Document(file)
        full_text = []
        for para in doc.paragraphs:
            full_text.append(para.text)
        return "\n".join(full_text)

    elif file_type == ".txt":
        return str(file.read(), "utf-8")

    else:
        raise ValueError("Unsupported file format.")


def parse_resume_with_gemini(resume_text):
    prompt = """
You are a resume parser AI. Given the following resume text, extract and structure the information into the JSON format specified below.
Parse every type of document properly eacch spelling and spacing and give in right format. Also give summary in the summary field.

Only return the JSON output without any extra explanation.

JSON Schema:
{
    "address": {
        "city": "",
        "country": ""
        "state": "",
    },
    ],
    "education_history": [
        {
            "degree": "",
            "from_date": "",
            "name": "",
            "to_date": ""
        }
    ],
    "email": "",
    "first_name": "",
    "last_name": "",
    "phone": "",
    "skills": [
        {"skill": ""}
    ],
    "summary": "",
    "work_history": [
        {
            "company": "",
            "description": ""
            "from_date": "",
            "title": "",
            "to_date": "",

        }
    ]
}

Resume Text:
"""

    prompt += resume_text[:30000]  # Limit input length

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text


def clean_gemini_output(gemini_output):
    try:
        if "```json" in gemini_output:
            gemini_output = gemini_output.split("```json")[1].split("```")[0]
        return json.loads(gemini_output)
    except Exception as e:
        st.error(f"Error parsing JSON: {e}")
        return {"raw_output": gemini_output}


def save_json_to_download(data):
    return json.dumps(data, indent=4).encode("utf-8")


st.markdown("Upload a resume (PDF, DOCX, or TXT)")

uploaded_file = st.file_uploader("📂 Choose a resume file", type=["pdf", "docx", "txt"])

if uploaded_file:
    st.info("🔄 Parsing resume... Please wait.")
    resume_text = extract_text_from_file(uploaded_file)

    with st.expander("📄 Raw Resume Text"):
        st.text_area("", resume_text[:20000], height=300)
 
    gemini_output = parse_resume_with_gemini(resume_text)
    parsed_resume = clean_gemini_output(gemini_output)
   
    st.success("✅ Parsed Resume (JSON Format):")
    st.json(parsed_resume)

    json_data = save_json_to_download(parsed_resume)
    st.download_button(
        label="💾 Download JSON",
        data=json_data,
        file_name="parsed_resume.json",
        mime="application/json"
    )