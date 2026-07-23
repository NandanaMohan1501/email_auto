import json
import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def classify_email(subject: str, body: str):

    prompt = f"""
You are an email classification assistant.

Analyze the email below.

Return ONLY valid JSON.

Categories:
- Job Application
- Technical Support
- Sales Inquiry
- Complaint
- Billing
- HR
- General Inquiry
- Other

Priorities:
- High
- Medium
- Low

Subject:
{subject}

Body:
{body}

Return exactly this JSON:

{{
  "category": "",
  "priority": "",
  "summary": ""
}}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    text = response.text.strip()

    # Remove markdown fences if present
    text = text.replace("```json", "").replace("```", "").strip()

    return json.loads(text)