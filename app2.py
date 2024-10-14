import streamlit as st
import google.generativeai as genai
import PyPDF2 as pdf
import spacy
import re
from dotenv import load_dotenv
import os
# Load environment variables and spaCy model
load_dotenv()
nlp = spacy.load("en_core_web_sm")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to extract text from uploaded PDF resume
def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Function to extract keywords from text using spaCy
def extract_keywords(text):
    doc = nlp(text)
    keywords = [chunk.text.lower() for chunk in doc.noun_chunks if len(chunk.text.split()) < 3]
    return keywords

# Improved function to get response from Gemini model with a more specific and structured prompt
def get_gemini_response(jd_text, resume_text):
    input_prompt = f"""
    You are an advanced ATS (Applicant Tracking System) with expertise in analyzing real resumes and job descriptions. 
    You must evaluate **only** the provided resume text and job description text. Do not create or imagine fictional candidates.

    Task:
    1. **Match Evaluation**: Based solely on the provided resume and job description, assign a percentage score representing how well the resume matches the job description. This score should be based strictly on relevant keywords, skills, and qualifications that appear in both the resume and the job description.
    
    2. **Missing Keywords**: Identify any important skills, tools, or qualifications mentioned in the job description that are missing from the resume. Do not invent any keywords.
    
    3. **Profile Summary**: Provide a concise summary of the candidate's strengths and weaknesses, but **only** based on the resume content. Do not imagine or create details not found in the resume text.

    The response must strictly follow this structure:
    {{
        "JD Match": "<match percentage>%",
        "MissingKeywords": ["<missing keyword 1>", "<missing keyword 2>", ...],
        "ProfileSummary": "<summary of the candidate's profile>"
    }}

    Here is the resume text:
    {resume_text}

    Here is the job description text:
    {jd_text}
    """

    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input_prompt)
    
    ats_response = response.candidates[0].content.parts[0].text
    return ats_response

# Function to find missing keywords from resume when compared to job description
def find_missing_keywords(jd_keywords, resume_keywords):
    # Use a set to find keywords in the JD that are missing in the resume
    missing_keywords = set(jd_keywords) - set(resume_keywords)
    return list(missing_keywords)

# Function to extract match percentage from the response
def extract_match_percentage(response_text):
    try:
        # Use regex to extract the JD Match percentage
        match = re.search(r'"JD Match":\s*"(\d+\.?\d*)%', response_text)
        if match:
            return float(match.group(1))
        else:
            return None  # Return None if no percentage is found
    except Exception as e:
        return None
    

# Function to display ATS evaluation response more clearly
def display_ats_response(ats_response):
    try:
        # Extract the components of the ATS response
        match_percentage = re.search(r'"JD Match":\s*"(\d+\.?\d*)%', ats_response).group(1)
        missing_keywords_match = re.search(r'"MissingKeywords":\s*\[(.*?)\]', ats_response)
        profile_summary_match = re.search(r'"ProfileSummary":\s*"(.*?)"', ats_response, re.DOTALL)
        
        missing_keywords = missing_keywords_match.group(1).split(",") if missing_keywords_match else []
        profile_summary = profile_summary_match.group(1).replace("\\n", "\n") if profile_summary_match else "No summary available."
        
        # Display the Match Percentage
        st.subheader("ATS Evaluation - Match Percentage")
        st.write(f"**Match Percentage**: {match_percentage}%")
        
        # Display the Missing Keywords
        st.subheader("ATS Evaluation - Missing Keywords")
        if missing_keywords:
            st.write("The following important skills or keywords from the job description are missing in your resume:")
            st.write(f"- {', '.join(missing_keywords)}")
        else:
            st.write("No missing keywords! Your resume covers all key areas mentioned in the job description.")
        
        # Display the Profile Summary
        st.subheader("ATS Evaluation - Profile Summary")
        st.write(profile_summary)
    
    except Exception as e:
        st.error(f"Error parsing ATS response: {str(e)}")

# Streamlit UI
st.title("Smart ATS")
st.text("Enhance Your Resume Using ATS Evaluation")

# Input fields for job description and resume
jd = st.text_area("Paste the job description here:")
uploaded_file = st.file_uploader("Upload your resume (PDF only)", type="pdf", help="Please upload your resume in PDF format.")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None and jd:
        # Extract text from uploaded resume
        resume_text = input_pdf_text(uploaded_file)
        
        # Extract keywords from both job description and resume
        jd_keywords = extract_keywords(jd)
        resume_keywords = extract_keywords(resume_text)
        
        # Get missing keywords in resume compared to job description
        missing_keywords = find_missing_keywords(jd_keywords, resume_keywords)
        
        # Get ATS evaluation response from Gemini model
        ats_response = get_gemini_response(jd, resume_text)
        
        # Display ATS evaluation in a clearer format
        display_ats_response(ats_response)
        
        # Display match percentage and progress bar
        match_percentage = extract_match_percentage(ats_response)
        if match_percentage is not None:
            st.subheader("Match Percentage (from ATS):")
            st.write(f"{match_percentage}%")
            st.progress(int(match_percentage))
        else:
            st.write("Could not extract match percentage from the response.")
    else:
        st.write("Please upload your resume and paste the job description.")