

# Resume Analyzer

A web application built with **Python** and **Streamlit** that analyzes resumes, extracts skills, and compares them against a provided job description or a common skill list.
This project is ideal for recruiters, job seekers, and career coaches to quickly assess skill matches.

## Features

* 📄 Upload your resume (PDF format)
* 🧠 Extracts skills using **Natural Language Processing (NLP)**
* 📊 Compares extracted skills with:

  * Provided job description (if available)
  * Common industry skill list (fallback)
* 📈 Displays matching and missing skills
* 🌐 Simple, clean web interface using **Streamlit**

## Tech Stack

* **Python 3**
* **Streamlit** (Web UI)
* **spaCy** (NLP processing)
* **PyPDF2** (PDF reading)
* **re** (Regex for pattern matching)

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/safa-noora/resume-analyzer.git
   cd resume-analyzer
   ```

2. **Create and activate a virtual environment**

   ```bash
   python -m venv venv
   venv\Scripts\activate   # For Windows
   source venv/bin/activate  # For Mac/Linux
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Download spaCy model**

   ```bash
   python -m spacy download en_core_web_sm
   ```

## Usage

Run the Streamlit app:

```bash
streamlit run app.py
```

Open your browser and go to:

```
http://localhost:8501
```

## Deployment

You can host this app for free on **Streamlit Cloud**:

1. Push your code to GitHub.
2. Go to [Streamlit Cloud](https://streamlit.io/cloud) and sign in.
3. Create a new app and link your GitHub repo.
4. Select `app.py` as the entry point.
5. Deploy and share your app URL.

## Example

**Input:** Resume PDF + Job Description (optional)
**Output:** List of matched skills & missing skills.

## License

This project is open-source. You are free to use and modify it.

---

