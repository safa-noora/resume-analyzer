import fitz  # PyMuPDF
import re
import spacy
import streamlit as st
from spacy.lang.en.stop_words import STOP_WORDS

# ---------------- Page Config ----------------
st.set_page_config(page_title="Resume Skill Analyzer", layout="centered")

# ---------------- NLP Model ----------------
nlp = spacy.load("en_core_web_sm")

# ---------------- Extract Text ----------------
def extract_text_from_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# ---------------- Preprocess ----------------
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    doc = nlp(text)
    tokens = [
        token.lemma_ for token in doc
        if token.text not in STOP_WORDS and not token.is_punct
    ]
    return tokens

# ---------------- Skill Matching ----------------
def match_skills(tokens, skill_list):
    matched = []
    token_text = " ".join(tokens)
    for skill in skill_list:
        if " " in skill:
            if skill in token_text:
                matched.append(skill)
        else:
            if skill in tokens:
                matched.append(skill)
    return matched

# ---------------- Summary ----------------
def generate_summary(matched, total_skills):
    score = (len(matched) / len(total_skills)) * 100
    st.subheader("Skill Match Report")
    st.write(f"**Skills Matched:** {', '.join(matched) if matched else 'None'}")
    st.write(f"**Match Score:** `{len(matched)} / {len(total_skills)}` ({score:.1f}%)")

    if score >= 80:
        st.success("Great alignment with industry-relevant skills.")
    elif score >= 50:
        st.warning("Fair alignment. Consider highlighting more relevant skills.")
    else:
        st.info("Low match. You might want to update your resume with more role-specific keywords.")

# ---------------- UI Layout ----------------
st.markdown(
    """
    <style>
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        .stButton>button {
            background-color: #34568B;
            color: white;
            border-radius: 6px;
            height: 3em;
            width: 100%;
        }
        .stFileUploader label {
            font-weight: 600;
        }
        .stMarkdown h1 {
            font-size: 2rem;
            font-weight: 700;
            margin-bottom: 1rem;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Resume Skill Analyzer")
st.write("Evaluate how well your resume aligns with common technical and soft skills.")

with st.sidebar:
    st.header("Upload Your Resume")
    uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

# ---------- Process ----------
if uploaded_file:
    with st.spinner("Analyzing..."):
        resume_text = extract_text_from_pdf(uploaded_file)
        tokens = preprocess_text(resume_text)

        desired_skills = [
            "python", "java", "c", "c++", "html", "css", "javascript",
            "machine learning", "deep learning", "sql", "data analysis",
            "communication", "teamwork", "leadership", "problem solving"
        ]

        matched_skills = match_skills(tokens, desired_skills)

        st.markdown("### Analysis Result")
        generate_summary(matched_skills, desired_skills)

        with st.expander("View Extracted Resume Text"):
            st.text_area(label="Raw Resume Text", value=resume_text[:3000], height=300)

    st.markdown("---")
    st.caption("Built with Python and Streamlit | Developed by Safa Noora")
