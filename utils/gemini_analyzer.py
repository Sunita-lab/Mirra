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

TEXT:
{text}

LOCAL ANALYSIS RESULTS:
{local_results}

Tasks:

1. Explain the local analysis results.
2. Detect whether the text contains a factual claim.
3. Estimate cherry-picking risk (0-100).
4. Decide whether verification is needed.
5. Explain your reasoning.

Return ONLY valid JSON.

Required format:

{{
    "claim_detected": true,
    "cherry_picking_risk": 0,
    "cherry_picking_reason": "",
    "verification_needed": false,

    "signal_explanation": {{
        "credibility": "",
        "emotion": "",
        "clickbait": "",
        "evidence": ""
    }}
}}

Rules:
- Do NOT invent scores.
- Use the provided local analysis values.
- cherry_picking_risk must be an integer between 0 and 100.
- claim_detected must be true only if a factual claim is present.
- verification_needed should be true if the claim can be checked against evidence or authoritative sources.
- Keep explanations short and clear (1-2 sentences).
- Return ONLY valid JSON.
"""

    response = model.generate_content(prompt)

    raw_text = response.text.strip()

    # Remove markdown code fences if Gemini adds them
    raw_text = re.sub(r"^```json", "", raw_text)
    raw_text = re.sub(r"^```", "", raw_text)
    raw_text = re.sub(r"```$", "", raw_text)

    raw_text = raw_text.strip()

    try:
        return json.loads(raw_text)

    except Exception:
        return {
            "claim_detected": None,
            "cherry_picking_risk": None,
            "cherry_picking_reason": "Failed to parse Gemini response.",
            "verification_needed": None,
            "signal_explanation": {
                "credibility": "",
                "emotion": "",
                "clickbait": "",
                "evidence": ""
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

    print(result)