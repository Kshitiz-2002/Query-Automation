import streamlit as st
import re
import PyPDF2
from io import StringIO
from docx import Document
import chardet  
import requests  

def preprocess_text(text):
    return re.sub(r'[",]', '', text)

def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def extract_text_from_word(word_file):
    doc = Document(word_file)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

def read_text_file(text_file):
    raw_data = text_file.read()
    result = chardet.detect(raw_data)
    encoding = result['encoding']

    try:
        text = raw_data.decode(encoding)
    except (UnicodeDecodeError, TypeError):
        text = raw_data.decode('utf-8', errors='ignore')  
    return text

st.title("Resume & Cover Letter Processor")

st.subheader("Upload Your Resume")
resume_file = st.file_uploader("Choose a file", type=["txt", "docx", "pdf"])
if resume_file:
    file_extension = resume_file.name.split('.')[-1].lower()

    if file_extension == "pdf":
        resume_text = extract_text_from_pdf(resume_file)
    elif file_extension == "docx":
        resume_text = extract_text_from_word(resume_file)
    elif file_extension == "txt":
        resume_text = read_text_file(resume_file)  
    
    resume = preprocess_text(resume_text)
    st.success("Resume uploaded and processed successfully!")

st.subheader("Upload or Write Your Cover Letter")
cover_letter_option = st.radio("How would you like to provide your cover letter?", 
                                ("Upload File", "Write Text"))

if cover_letter_option == "Upload File":
    cover_letter_file = st.file_uploader("Choose a file", type=["txt", "docx", "pdf"], key="cover_letter_file")
    if cover_letter_file:
        file_extension = cover_letter_file.name.split('.')[-1].lower()

        if file_extension == "pdf":
            cover_letter_text = extract_text_from_pdf(cover_letter_file)
        elif file_extension == "docx":
            cover_letter_text = extract_text_from_word(cover_letter_file)
        elif file_extension == "txt":
            cover_letter_text = read_text_file(cover_letter_file)  
        
        cover_letter = preprocess_text(cover_letter_text)
        st.success("Cover letter uploaded and processed successfully!")
elif cover_letter_option == "Write Text":
    cover_letter_text = st.text_area("Write your cover letter here")
    if cover_letter_text:
        cover_letter = preprocess_text(cover_letter_text)
        st.success("Cover letter processed successfully!")


st.subheader("Task Description")
task = st.text_input("Enter the task (e.g., Describe how I fit the role):")


st.subheader("Job Description URLs")
urls = st.text_area("Enter URLs (one per line):").splitlines()


if st.button("Get Results"):
    if resume_file and cover_letter_text and urls:
        payload = {
            "resume": resume,
            "cover_letter": cover_letter,
            "task": task,
            "urls": urls
        }
        
        try:
            response = requests.post("http://127.0.0.1:8000/query/", json=payload)
            
            if response.status_code == 200:
                resultList = response.json()
                st.subheader("Results")
                for url, result in resultList.items():
                    st.write(f"**Job URL**: {url}")
                    st.text_area("Generated Result", value=result, height=200, key=f"result_{url}")
                    st.download_button("Copy Result", result, file_name="response.txt")
            else:
                st.error("Failed to get a valid response from the server.")
        except requests.exceptions.RequestException as e:
            st.error(f"Error sending request: {e}")
    else:
        st.warning("Please complete all fields before submitting!")
