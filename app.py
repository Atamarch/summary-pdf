import os
import streamlit as st
import google.generativeai as genai
from pypdf import PdfReader
from dotenv import load_dotenv
import tempfile

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

st.set_page_config(
    page_title="PDF Summarizer",
    page_icon="📄",
    layout="centered"
)

def extract_text_from_pdf(pdf_file) -> str:
    """Extract text from uploaded PDF file"""
    reader = PdfReader(pdf_file)
    text = ""
    
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    
    return text

def summarize_text(text: str) -> str:
    """Generate summary using Gemini AI"""
    prompt = f"""
    Please summarize the following document in clear, concise paragraphs.
    Highlight key ideas and structure the summary for readability.

    Document content:
    {text[:15000]}
    """
    
    response = model.generate_content(prompt)
    return response.text

st.title("📄 PDF Summarizer")
st.markdown("Upload a PDF document and get an AI-powered summary in seconds!")

uploaded_file = st.file_uploader(
    "Choose a PDF file",
    type="pdf",
    help="Upload a PDF document to summarize"
)

if uploaded_file is not None:
    st.success(f"File uploaded: {uploaded_file.name}")
    file_size = uploaded_file.size / 1024 
    st.caption(f"File size: {file_size:.2f} KB")
    
    if st.button("Generate Summary", type="primary", use_container_width=True):
        try:
            with st.spinner("🔄 Extracting text from PDF..."):
                pdf_text = extract_text_from_pdf(uploaded_file)
            
            if not pdf_text.strip():
                st.error("❌ Could not extract text from PDF. Make sure it's not a scanned image.")
            else:
                st.success(f"Extracted {len(pdf_text)} characters")
                
                with st.spinner("Generating summary with AI..."):
                    summary = summarize_text(pdf_text)
                
                st.markdown("---")
                st.subheader("📋 Summary")
                st.markdown(summary)
                
                st.download_button(
                    label="Download Summary",
                    data=summary,
                    file_name=f"{uploaded_file.name.replace('.pdf', '')}_summary.pdf",
                    mime="text/plain"
                )
                
        except Exception as e:
            st.error(f" An error occurred: {str(e)}")
            st.info("Please check your API key and try again.")

else:
    st.info("Please upload a PDF file to get started")
