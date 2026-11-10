import json
import time
from google import genai
from utils import dynamic_local_audit

def analyze_with_gemini(contract_text: str, api_key: str) -> dict:
    if not api_key or not api_key.strip():
        time.sleep(0.8)
        return dynamic_local_audit(contract_text)

    client = genai.Client(api_key=api_key.strip(), http_options={"timeout": 6000})

    prompt = f"""You are a legal contract auditor. Analyze the following contract text and identify the top 3 highest risk or predatory clauses.
Return ONLY valid JSON matching this exact structure:
{{
  "risk_score": 85,
  "verdict": "Critical Risk - Do Not Sign Unmodified",
  "summary": "Two sentence overview of key risks.",
  "clauses": [
    {{"title": "Clause Title", "risk_level": "High", "issue": "Why it is dangerous", "recommendation": "How to negotiate or revise"}}
  ]
}}

Contract Text:
{contract_text[:3500]}"""

    models = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-3.8-flash"]
    for model_name in models:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config={
                    "response_mime_type": "application/json",
                    "temperature": 0.1,
                },
            )
            raw = response.text.strip().replace("```json", "").replace("```", "").strip()
            parsed = json.loads(raw)
            if "risk_score" in parsed and "clauses" in parsed:
                return parsed
        except Exception:
            continue

    return dynamic_local_audit(contract_text)
