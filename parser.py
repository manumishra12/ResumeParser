import google.generativeai as genai
import fitz  
from docx import Document  
import json
import os
from dotenv import load_dotenv


load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

def extract_text_from_file(file_path):
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()

    if ext == ".pdf":
        with fitz.open(file_path) as doc:
            text = ""
            for page in doc:
                text += page.get_text()
            return text

    elif ext == ".docx":
        doc = Document(file_path)
        full_text = []
        for para in doc.paragraphs:
            full_text.append(para.text)
        return '\n'.join(full_text)

    elif ext == ".txt":
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    else:
        raise ValueError(f"Unsupported file format: {ext}. Only .pdf, .docx, and .txt are supported.")



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
        # Remove markdown code block if any
        if "```json" in gemini_output:
            gemini_output = gemini_output.split("```json")[1].split("```")[0]
        return json.loads(gemini_output)
    except Exception as e:
        print("Error parsing JSON:", e)
        return {"raw_output": gemini_output}


def save_json_to_file(data, output_file="parsed_resume_output.json"):
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    print(f"✅ Parsed resume saved to '{output_file}'")


def main(file_path):
    resume_text = extract_text_from_file(file_path)
    gemini_output = parse_resume_with_gemini(resume_text)
    structured_resume = clean_gemini_output(gemini_output)

    print("Parsed Resume (JSON Format):")
    print(json.dumps(structured_resume, indent=4))

    save_json_to_file(structured_resume)

if __name__ == "__main__":
    file_path = "sample_resume.pdf"  
    main(file_path)