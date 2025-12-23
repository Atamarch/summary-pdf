# PDF Summarizer

Simple PDF summarizer using Streamlit and Google Gemini AI.

## Requirements
- Python 3.14+
- Gemini API Key

## Installation
```bash
Salin kode

git clone <repo-url>
cd pdf-summarizer
pip install -r requirements.txt
```

Environment Variable
Create .env:
```bash
Salin kode

GEMINI_API_KEY=your_api_key_here
```

Run
```bash
Salin kode
streamlit run main.py
Open: http://localhost:8501

Notes
Only works for text-based PDFs (not scanned images)
Uses gemini-2.5-flash

