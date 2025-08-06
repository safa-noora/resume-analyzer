import fitz  # PyMuPDF
import re
import spacy
from spacy.lang.en.stop_words import STOP_WORDS

# STEP 1: Extract text from PDF
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# STEP 2: Preprocess the extracted text
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)  # Remove punctuation and numbers
    doc = nlp(text)
    tokens = [token.lemma_ for token in doc if token.text not in STOP_WORDS and not token.is_punct]
    return tokens

# STEP 3: Match skills from a predefined list
def match_skills(tokens, skill_list):
    matched = []
    token_text = " ".join(tokens)  # For multi-word skills
    for skill in skill_list:
        if " " in skill:
            if skill in token_text:
                matched.append(skill)
        else:
            if skill in tokens:
                matched.append(skill)
    return matched

# STEP 4: Generate a resume score and summary
def generate_summary(matched_skills, total_skills):
    score = (len(matched_skills) / len(total_skills)) * 100
    print("\n📊 Resume Analysis Summary")
    print("----------------------------")
    print(f"Total Skills Matched: {len(matched_skills)} / {len(total_skills)}")
    print(f"Matched Skills: {', '.join(matched_skills) if matched_skills else 'None'}")
    print(f"Resume Score: {score:.2f}%")
    
    if score >= 80:
        print("✅ Excellent! Your resume is highly relevant.")
    elif score >= 50:
        print("⚠️ Good. But consider adding more relevant skills.")
    else:
        print("❌ Resume needs improvement for this job role.")

# STEP 5: Main Execution
if __name__ == "__main__":
    nlp = spacy.load("en_core_web_sm")  # Load spaCy model

    # 📄 Path to your resume
    path = "sample_resume.pdf"  # Replace with your actual file name

    # 🔍 Extract and process
    extracted = extract_text_from_pdf(path)
    print("📄 Extracted Resume Text:\n", extracted)

    preprocessed = preprocess_text(extracted)
    print("\n🧹 Preprocessed Tokens:\n", preprocessed)

    # 🧠 Skills to match against
    desired_skills = [
        "python", "java", "c", "c++", "html", "css", "javascript",
        "machine learning", "deep learning", "sql", "data analysis",
        "communication", "teamwork", "leadership", "problem solving"
    ]

    # ✅ Skill Matching and Summary
    matched_skills = match_skills(preprocessed, desired_skills)
    print("\n✅ Matched Skills from Resume:\n", matched_skills)

    generate_summary(matched_skills, desired_skills)
