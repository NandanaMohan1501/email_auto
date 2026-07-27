import json

from app.llm import get_llm


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

    llm = get_llm()

    response = llm.invoke(prompt)

    text = response.content.strip()

    return json.loads(text)