from dotenv import load_dotenv

load_dotenv()
import base64
import streamlit as st
import os
import io
from PIL import Image
import pdf2image
import google.generativeai as genai
import PyPDF2 as pdf 
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# def get_gemini_response(input, pdf_content, prompt):
#     model = genai.GenerativeModel("gemini-1.5-flash")
    
#     # Combine input and prompt text for the model's input
#     response = model.generate_content(input + prompt)
    
#     # Extract the text from the first candidate in the response
#     if response.candidates:
#         generated_text = response.candidates[0].content.parts[0].text
#     else:
#         generated_text = "No response generated"
    
#     return generated_text

# def input_pdf_setup(uploaded_file):
#     if uploaded_file is not None:
#         # Convert the PDF to image
#         images = pdf2image.convert_from_bytes(uploaded_file.read())
#         first_page = images[0]

#         # Convert to bytes
#         img_byte_arr = io.BytesIO()
#         first_page.save(img_byte_arr, format='JPEG')
#         img_byte_arr = img_byte_arr.getvalue()

#         pdf_parts = [
#             {
#                 "mime_type": "image/jpeg",
#                 "data": base64.b64encode(img_byte_arr).decode()  # encode to base64
#             }
#         ]
#         return pdf_parts
#     else:
#         raise FileNotFoundError("No file uploaded")

# ## Streamlit App

# st.set_page_config(page_title="ATS Resume Expert")
# st.header("ATS Tracking System")
# input_text = st.text_area("Job Description:", key="input")
# uploaded_file = st.file_uploader("Upload your resume (PDF)...", type=["pdf"])

# if uploaded_file is not None:
#     st.write("PDF uploaded successfully")

# submit1 = st.button("Tell me about my Resume")
# submit3 = st.button("Percentage match")

# prompt1 = """
# You are experienced HR with Technical experiences in the field of any one job role from Data science or full stack software development or full stack web development or DEVOPS or big data engineering or Data analyst, your task is to review the provided job description against the uploaded resume.
# Please share your professional evaluation on whether the candidate's profile aligns with the role. Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
# """
# prompt3 = """
# You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
# your task is to evaluate the resume against the provided job description. Give me the percentage of match if the resume matches
# the job description. First, the output should come as a percentage and then keywords missing and last final thoughts.
# """

# if submit1:
#     if uploaded_file is not None:
#         pdf_content = input_pdf_setup(uploaded_file)
#         response = get_gemini_response(input_text, pdf_content, prompt1)
#         st.subheader("The Response is")
#         st.write(response)
#     else:
#         st.write("Please upload the resume")

# elif submit3:
#     if uploaded_file is not None:
#         pdf_content = input_pdf_setup(uploaded_file)
#         response = get_gemini_response(input_text, pdf_content, prompt3)
#         st.subheader("The Response is")
#         st.write(response)
#     else:
#         st.write("Please upload the resume")


def get_gemini_response(input):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input)
    return response.candidates[0].content.parts[0].text  # Extracting the text from the response

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:  # Loop over reader.pages directly
        text += page.extract_text()  # Extract text from each page and concatenate
    return text

# Input prompt for ATS evaluation
input_prompt = """
Hey act like a skilled or very experienced ATS (Applicant Tracking System) with a deep understanding of the tech field, software engineering, data science, data analysis, and big data engineering. Your task is to evaluate the resume based on the given job description. You must consider that the job market is very competitive, and you should provide the best assistance for improving the resumes. Assign the percentage matching based on JD and the missing keywords with high accuracy.

Resume: {text}
Description: {jd}

I want the responses in one single string having the structure:
{{"JD Match":"%","MissingKeywords:[]","Profile summary":""}}
"""

st.title("Smart ATS")
st.text("Improve Your Resume ATS")
jd = st.text_area("Paste the job description")
uploaded_file = st.file_uploader("Upload Your Resume", type="pdf", help="Please upload the PDF")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        # Extract text from uploaded resume PDF
        resume_text = input_pdf_text(uploaded_file)
        
        # Format the input for the generative model
        formatted_prompt = input_prompt.format(text=resume_text, jd=jd)
        
        # Get response from generative model
        response = get_gemini_response(formatted_prompt)
        
        st.subheader("ATS Evaluation")
        st.write(response)
    else:
        st.write("Please upload your resume.")