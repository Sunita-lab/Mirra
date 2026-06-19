import os
import json
import re

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel("gemini-2.5-flash")


def analyze_with_gemini(text, local_results):

    prompt = f"""
You are Mirra, an AI trust analysis assistant.

Your task is to analyze the text and explain the results of Mirra's trust signals.

TEXT:
{text}

LOCAL ANALYSIS RESULTS:
{local_results}

METRIC DEFINITIONS:

Credibility Confidence:
Represents how confident the ML model is in its prediction.
It does NOT represent truthfulness.

Emotion Score:
Measures emotional intensity in language.
Higher scores indicate more emotionally charged wording.

Clickbait Score:
Measures presence of sensational or attention-grabbing language.
Higher scores indicate stronger clickbait patterns.

Evidence Score:
Measures presence of evidence indicators such as:
study, report, research, survey, data, according to.
Higher scores indicate stronger evidence signals.

TASKS:

1. Determine whether the text contains a factual claim.
2. Determine whether verification is recommended.
3. Estimate cherry-picking risk (0-100).
4. Create a short user-friendly summary.
5. Create a detailed analysis using the provided signals.

Return ONLY valid JSON.

Required format:

{{
  "summary": "",

  "claim_detected": true,

  "verification_needed": false,

  "cherry_picking_risk": 0,

  "sections": {{
      "claim_detection": "",
      "evidence_analysis": "",
      "clickbait_analysis": "",
      "cherry_picking_analysis": "",
      "verification_recommendation": ""
  }}
}}

Rules:

- summary must be 2-3 sentences.
- Use the local analysis values.
- Do not invent scores.
- cherry_picking_risk must be between 0 and 100.
- Keep section explanations concise.
- Return ONLY JSON.
"""

    response = model.generate_content(prompt)

    raw_text = response.text.strip()

    raw_text = re.sub(r"^```json", "", raw_text)
    raw_text = re.sub(r"^```", "", raw_text)
    raw_text = re.sub(r"```$", "", raw_text)

    raw_text = raw_text.strip()

    try:
        return json.loads(raw_text)

    except Exception:
        return {
            "summary": "Failed to generate analysis.",

            "claim_detected": None,

            "verification_needed": None,

            "cherry_picking_risk": None,

            "sections": {
                "claim_detection": "",
                "evidence_analysis": "",
                "clickbait_analysis": "",
                "cherry_picking_analysis": "",
                "verification_recommendation": ""
            }
        }
if __name__ == "__main__":

    sample_text = """
    Crime increased by 20% this year.
    """

    local_results = {
        "assessment": "Potentially Misleading",
        "confidence": 78,
        "emotion_score": 61,
        "clickbait_score": 40,
        "evidence_score": 20
    }

    result = analyze_with_gemini(
        sample_text,
        local_results
    )

    print(json.dumps(result, indent=4))