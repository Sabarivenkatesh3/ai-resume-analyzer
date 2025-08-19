import streamlit as st
import PyPDF2
import time
import json
import re
from resume_workflow import run_resume_workflow

st.set_page_config(page_title="AI Resume Analyzer", layout="wide")
st.title("📄 AI Resume Analyzer")

uploaded_file = st.file_uploader("Upload Resume (PDF)", type="pdf")
job_desc = st.text_area("Paste Job Description Here")

form = st.form("analyze_form")
submit = form.form_submit_button("Analyze Resume")

# --- Safe JSON parser ---
def safe_json_parse(text):
    try:
        return json.loads(text)
    except:
        match = re.search(r"\{.*\}", text, re.DOTALL)  # extract JSON-like block
        if match:
            try:
                return json.loads(match.group(0))
            except:
                return {"error": "Extracted JSON invalid."}
        return {"error": "Could not parse JSON."}

if submit and uploaded_file and job_desc:
    with st.spinner("Analyzing your resume..."):
        t0 = time.time()
        
        resume_text = ""
        try:
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    resume_text += page_text + "\n"
            if not resume_text.strip():
                st.error("Could not extract text from the PDF. Please ensure it's not an image-only PDF.")
                st.stop()
        except Exception as e:
            st.error(f"Error reading PDF: {e}")
            st.stop()

        results = run_resume_workflow(
            resume_text,
            job_desc,
            tasks_to_run=["parse", "keywords", "ats_score", "improvements"]
        )
        st.write(f"⏱ Analysis took: {time.time() - t0:.1f}s")

    if "error" in results:
        st.error(f"An error occurred during analysis: {results['error']}")
    else:
        st.success("Analysis Complete!")

        # Match keys with agents.py roles
        parsed_resume_output = results.get("resume_parser_output", "{}")
        jd_keywords_output = results.get("jd_keyword_extractor_output", "{}")
        ats_evaluation_output = results.get("ats_evaluator_output", "{}")
        improvement_suggestions_output = results.get("resume_improvement_coach_output", "{}")

        # Parse safely
        parsed_resume = safe_json_parse(parsed_resume_output)
        jd_keywords = safe_json_parse(jd_keywords_output)
        ats_details = safe_json_parse(ats_evaluation_output)
        improvement_suggestions = improvement_suggestions_output

        ats_score = ats_details.get("score", "N/A")
        st.metric("ATS Score", f'{ats_score}/100')

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("ATS Details")
            st.json(ats_details)
        with col2:
            st.subheader("Improvement Suggestions")
            st.markdown(improvement_suggestions)

        st.subheader("Extracted Resume Structure")
        st.json(parsed_resume)

        st.subheader("Extracted JD Keywords")
        st.json(jd_keywords)
