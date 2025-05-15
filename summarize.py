import openai
import requests
from bs4 import BeautifulSoup
from PyPDF2 import PdfReader

# Replace this with your actual OpenAI API key
openai.api_key = "OPENAI_API_KEY_HERE"

def extract_text_from_pdf(path):
    reader = PdfReader(path)
    return "\n".join(page.extract_text() for page in reader.pages if page.extract_text())

def extract_text_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup.get_text()

def summarize_text(text):
    prompt = f"""
You are a policy analyst summarizing congressional hearings about internet and network policy. Your task is to produce summaries in plain, accessible English that follow this format:

1. Title
2. Committee, date, and meeting information
3. Hearing goal
4. Key points
5. Hearing outcome
6. Connection to Internet Policy

Here is the hearing transcript:
{text[:3000]}

Return a structured, concise summary (~300-350 words).
"""
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an expert policy analyst."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )
    return response.choices[0].message.content

def clarify_question(summary, question):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an assistant helping to explain a congressional hearing summary."},
            {"role": "user", "content": f"The user has a question: '{question}'\nBased on this summary:\n{summary}"}
        ],
        temperature=0.5
    )
    return response.choices[0].message.content
