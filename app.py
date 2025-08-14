import fitz  # PyMuPDF
import re
import spacy
import streamlit as st
from spacy.lang.en.stop_words import STOP_WORDS

# ---------------- Page Config ----------------
st.set_page_config(page_title="Resume Skill Analyzer", layout="centered")

# ---------------- NLP Model ----------------
nlp = spacy.load("en_core_web_sm")

# ---------------- Utils ----------------
def extract_text_from_pdf(file):
    """Read all text from a PDF-like stream."""
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def preprocess_text(text: str):
    """Lowercase, remove punctuation, lemmatize, and drop stopwords."""
    text = text.lower()
    text = re.sub(r'[^a-z\s]', ' ', text)  # keep only letters and spaces
    doc = nlp(text)
    tokens = [
        token.lemma_
        for token in doc
        if token.text not in STOP_WORDS and not token.is_punct and token.lemma_.strip()
    ]
    return tokens

def match_skills(tokens, skill_list):
    """Return skills from skill_list found in the processed tokens/phrases."""
    matched = []
    token_text = " ".join(tokens)
    for skill in skill_list:
        sk = skill.lower().strip()
        if " " in sk:
            if sk in token_text:
                matched.append(skill)
        else:
            if sk in tokens:
                matched.append(skill)
    # keep order from skill_list, remove dups
    seen = set()
    ordered = []
    for s in matched:
        if s not in seen:
            seen.add(s)
            ordered.append(s)
    return ordered

def summarize_match(matched, required):
    score = 0.0 if not required else (len(matched) / len(required)) * 100
    missing = [s for s in required if s not in matched]
    return round(score, 1), missing

# A broader catalog (no punctuation; keep simple aliases that work with our preprocessing)
SKILL_CATALOG = [
    # Programming / Data
    "python","java","c","c++","c sharp","go","ruby","php","r","scala","kotlin","swift","matlab",
    "javascript","typescript","html","css","sql","nosql",
    # Data / ML
    "data analysis","data visualization","statistics","excel","power bi","tableau",
    "machine learning","deep learning","nlp","computer vision","pandas","numpy","scikit learn","tensorflow","pytorch",
    # Web / Backend
    "django","flask","fastapi","node","express","react","angular","vue","next js","rest api","graphql",
    # Cloud / DevOps
    "docker","kubernetes","ci cd","git","github","gitlab","jenkins","aws","azure","gcp","linux","bash",
    # Databases / Big Data
    "postgresql","mysql","sqlite","mongodb","redis","snowflake","hive","spark","hadoop",
    # Testing
    "unit testing","pytest","selenium",
    # Soft skills
    "communication","teamwork","leadership","problem solving","time management","adaptability",
]

def find_required_skills_from_text(text, catalog):
    """
    Derive required skills from JD text by matching against the catalog.
    Uses simple phrase/word presence on a preprocessed view.
    """
    tokens = preprocess_text(text)
    token_text = " ".join(tokens)
    found = []
    for skill in catalog:
        sk = skill.lower().strip()
        if " " in sk:
            if sk in token_text:
                found.append(skill)
        else:
            if sk in tokens:
                found.append(skill)
    # de-duplicate preserving order
    seen = set()
    ordered = []
    for s in found:
        if s not in seen:
            seen.add(s)
            ordered.append(s)
    return ordered

# ---------------- UI Layout ----------------
st.title("Resume Skill Analyzer")
st.write("Evaluate alignment between your resume and a set of required skills. "
         "You can paste a job description or use a common skill list.")

with st.sidebar:
    st.header("1) Upload Your Resume")
    resume_file = st.file_uploader("Choose a PDF file", type=["pdf"])

st.markdown("### 2) Choose Comparison Mode")
mode = st.radio(
    label="How should we derive the required skills?",
    options=["Compare with Job Description (Recommended)", "Compare with Common Skills"],
    index=0,
)

jd_text_input = ""
jd_file = None
required_skills = []

if mode == "Compare with Job Description (Recommended)":
    st.subheader("Paste Job Description or Upload JD PDF")
    jd_text_input = st.text_area(
        label="Paste job description text",
        help="Paste the job posting/responsibilities/requirements here.",
        height=180,
        placeholder="Paste the JD here..."
    )
    jd_file = st.file_uploader("Or upload a JD PDF", type=["pdf"], key="jd_pdf")

    # Build required skills from JD
    combined_jd_text = ""
    if jd_text_input:
        combined_jd_text += jd_text_input + "\n"
    if jd_file:
        try:
            combined_jd_text += extract_text_from_pdf(jd_file)
        except Exception:
            st.warning("Could not read the uploaded JD PDF. Please paste the JD text instead.")

    if combined_jd_text.strip():
        required_skills = find_required_skills_from_text(combined_jd_text, SKILL_CATALOG)
        if not required_skills:
            st.info("No recognizable skills found in the job description. "
                    "We’ll fall back to the common skill list below.")
else:
    st.subheader("Using Common Skill List")
    st.caption("If you prefer, you can edit this list in the code (SKILL_CATALOG).")
    # No extra inputs

# Fallback: if JD mode found nothing, use a sensible common set
COMMON_SKILLS = [
    "python","java","c","html","css","javascript",
    "sql","data analysis","machine learning","deep learning",
    "communication","teamwork","leadership","problem solving"
]

if not required_skills:
    # In JD mode with no extraction, or in Common Skills mode
    required_skills = COMMON_SKILLS

# ---------- Process ----------
st.markdown("---")
run_btn = st.button("Analyze Resume", use_container_width=True)

if run_btn:
    if not resume_file:
        st.warning("Please upload your resume PDF in the sidebar before analyzing.")
    else:
        with st.spinner("Analyzing..."):
            try:
                resume_text = extract_text_from_pdf(resume_file)
            except Exception as e:
                st.error(f"Could not read your resume PDF. Details: {e}")
                st.stop()

            tokens = preprocess_text(resume_text)
            matched = match_skills(tokens, required_skills)
            score, missing = summarize_match(matched, required_skills)

        # ---- Results ----
        st.markdown("### Analysis Result")
        st.subheader("Skill Match Report")
        st.write(f"**Required skills considered:** {len(required_skills)}")
        st.write(f"**Matched skills ({len(matched)}):** {', '.join(matched) if matched else 'None'}")
        st.write(f"**Missing skills ({len(missing)}):** {', '.join(missing) if missing else 'None'}")
        st.write(f"**Fit Score:** `{score}%`")

        with st.expander("View Extracted Resume Text"):
            st.text_area(label="Raw Resume Text", value=resume_text[:3000], height=300)

st.markdown("---")
st.caption("Built with Python and Streamlit | Developed by Safa Noora")
