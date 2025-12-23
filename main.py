import os
import google.generativeai as genai
from pypdf import PdfReader
from dotenv import load_dotenv

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel("gemini-2.5-flash")

def extract_text_from_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text

def summarize_text(text: str) -> str:
    prompt = f"""
    Please summarize the following document in clear, concise paragraphs.
    Highlight key ideas and structure the summary for readability.

    Document content:
    {text[:15000]}
    """

    response = model.generate_content(prompt)
    return response.text

if __name__ == "__main__":
    pdf_path = "sample.pdf"

    print("Reading PDF...")
    pdf_text = extract_text_from_pdf(pdf_path)

    print("Generating summary... ⏳")
    summary = summarize_text(pdf_text)

    print("\n===== SUMMARY =====\n")
    print(summary)
