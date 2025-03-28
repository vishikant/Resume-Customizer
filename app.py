import streamlit as st
import pandas as pd
from resume_processor import ResumeProcessor
import os
from dotenv import load_dotenv
import openai
from datetime import datetime

processor=ResumeProcessor()
st.title("AI RESUME CUSTOMIZER")
st.write("This app uses AI to customize your resume based on a job description.")

jd_file=st.file_uploader("Upload a job description (PDF)", type=["pdf"])
resume_file=st.file_uploader("Upload your resume (LaTeX)", type=["tex"])

if jd_file and resume_file:
    jd_path=f"job_description_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    resume_path=f"resume_{datetime.now().strftime('%Y%m%d%H%M%S')}.tex"

    with open(jd_path, "wb") as f:
        f.write(jd_file.getbuffer())
    with open(resume_path, "wb") as f:
        f.write(resume_file.getbuffer())

    with st.spinner("Processing job description..."): #st.spinner() displays a loading spinner while the job description is being processed.
        jd_text=processor.extract_text_from_pdf(jd_path)
        key_skills=processor.extract_key_skills(jd_text)
        modified_resume=processor.modify_latex_resume(resume_path, key_skills)

    st.subheader("Key Skills Identified:")
    st.write(", ".join(key_skills))

    st.subheader("Modified Resume:")
    st.download_button("Download", modified_resume, f"{datetime.now().strftime('%Y%m%d%H%M%S')}_modified_resume.tex", "text/plain")
    os.remove(jd_path)
    os.remove(resume_path)
    