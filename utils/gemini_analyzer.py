import os
import json

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file.")

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.5-flash")


def analyze_with_gemini(text, local_results):

    prompt = f"""
You are Mirra, an AI Trust Analysis Assistant.

Mirra is a trust analysis tool, not a fact-checking tool.

Your goal is NOT to determine absolute truth or falsehood.

Instead, help users evaluate:

- credibility signals
- evidence quality
- context completeness
- verification needs
- cherry-picking risk
- trustworthiness indicators

TEXT TO ANALYZE:

{text}

LOCAL ANALYSIS RESULTS:

{local_results}

METRIC DEFINITIONS

Credibility Confidence:
Represents how confident the ML model is in its prediction.
It DOES NOT represent truthfulness.

Confidence Interpretation:

- Below 60 → Uncertain prediction
- 60–75 → Moderately confident prediction
- Above 75 → Strong confidence prediction

Do not treat low-confidence predictions as strong evidence.

Emotion Score:
Measures emotional intensity in language.

Clickbait Score:
Measures presence of attention-grabbing or sensational language.

Evidence Score:
Measures evidence indicators such as:

- study
- report
- research
- survey
- data
- according to

IMPORTANT PHILOSOPHY

Mirra evaluates trust signals.

Mirra does NOT determine absolute truth.

The absence of a factual claim does NOT automatically imply low concern.

Even when no factual claim exists, discuss relevant trust signals such as:

- clickbait patterns
- emotional manipulation
- missing context
- unsupported implications
- sensational language

UNCERTAIN ASSESSMENT HANDLING

If the local assessment is "Uncertain":

- Do not make strong trustworthiness conclusions.
- Do not describe the content as reliable.
- Do not describe the content as misleading.
- Explain that available signals are insufficient for a confident assessment.
- Focus on evidence quality, context, and verification needs.
- Use cautious language.
- Avoid warning-style wording unless supported by clear signals.

TASKS

1. Determine whether the text contains a factual claim.
2. Determine whether verification is recommended.
3. Estimate cherry-picking risk from 0 to 100.
4. Write a short user-friendly summary.
5. Generate detailed reasoning for each analysis section.

SUMMARY RULES

The summary should:

- be 2–3 sentences
- be written for ordinary users
- avoid technical jargon
- avoid mentioning scores
- avoid mentioning raw model outputs
- avoid mentioning local analysis
- avoid mentioning model predictions
- focus on what the user should know

When assessment is "Uncertain":

- Clearly communicate uncertainty.
- Do not imply suspicion.
- Do not imply reliability.
- Explain that available signals are insufficient for a confident conclusion.

SECTION RULES

- Explain reasoning clearly.
- Focus on interpretation.
- Never mention raw numerical values.
- Never repeat percentages.
- Explain why each signal matters.

If assessment is "Uncertain":

- Avoid strong language.
- Avoid phrases suggesting the content is misleading.
- Avoid phrases suggesting the content is trustworthy.
- Focus on limitations of available evidence and context.

CLAIM DETECTION

Explain:

- whether a factual claim exists
- what the claim is
- whether it can be independently verified

EVIDENCE ANALYSIS

Explain:

- whether supporting evidence is present
- whether sources are cited
- whether evidence appears sufficient

CLICKBAIT ANALYSIS

Focus on:

- whether wording appears designed to attract attention
- whether curiosity, urgency, fear, outrage, or surprise are being used
- whether the phrasing encourages engagement more than understanding

CHERRY-PICKING ANALYSIS

If factual claims exist:

- discuss missing context
- discuss selective presentation
- discuss whether conclusions appear broader than the evidence

If no factual claim exists:

- evaluate whether the wording still creates a misleading impression
- evaluate whether important context is withheld
- discuss trust concerns when appropriate

Do not automatically assign zero risk simply because no factual claim exists.

VERIFICATION RECOMMENDATION

Verification is not limited to factual accuracy.

Consider whether users may benefit from seeking:

- additional context
- supporting evidence
- original sources
- fuller explanations

before accepting the message at face value.

If assessment is "Uncertain":

- explain that verification may be useful because there is insufficient information for a confident conclusion.
- do not imply that verification is needed because the content is suspicious.

OUTPUT FORMAT

Return ONLY valid JSON.

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
"""

    try:

        response = model.generate_content(prompt)

        raw_text = response.text.strip()

        print("\n========== RAW GEMINI RESPONSE ==========")
        print(raw_text)
        print("=========================================\n")

        raw_text = raw_text.replace("```json", "")
        raw_text = raw_text.replace("```", "")
        raw_text = raw_text.strip()

        start = raw_text.find("{")
        end = raw_text.rfind("}")

        if start != -1 and end != -1:
            raw_text = raw_text[start:end + 1]

        try:
            result = json.loads(raw_text)

        except json.JSONDecodeError:

            first = raw_text.find("{")
            last = raw_text.rfind("}")

            cleaned = raw_text[first:last + 1]

            result = json.loads(cleaned)

        result.setdefault(
            "summary",
            "Analysis could not be generated."
        )

        result.setdefault(
            "claim_detected",
            False
        )

        result.setdefault(
            "verification_needed",
            False
        )

        result.setdefault(
            "cherry_picking_risk",
            0
        )

        result.setdefault(
            "sections",
            {}
        )

        sections = result["sections"]

        sections.setdefault(
            "claim_detection",
            ""
        )

        sections.setdefault(
            "evidence_analysis",
            ""
        )

        sections.setdefault(
            "clickbait_analysis",
            ""
        )

        sections.setdefault(
            "cherry_picking_analysis",
            ""
        )

        sections.setdefault(
            "verification_recommendation",
            ""
        )

        return result

    except Exception as e:

        print("\n========== GEMINI ERROR ==========")
        print(type(e))
        print(e)
        print("==================================\n")

        return {
            "summary": "Analysis could not be generated at this time.",
            "claim_detected": False,
            "verification_needed": False,
            "cherry_picking_risk": 0,
            "sections": {
                "claim_detection": "",
                "evidence_analysis": "",
                "clickbait_analysis": "",
                "cherry_picking_analysis": "",
                "verification_recommendation": ""
            },
            "error": str(e)
        }


if __name__ == "__main__":

    sample_text = "Delhi is the capital of India."

    local_results = {
        "assessment": "Uncertain",
        "confidence": 54.08,
        "emotion_score": 0,
        "clickbait_score": 0,
        "evidence_score": 0
    }

    result = analyze_with_gemini(
        sample_text,
        local_results
    )

    print(
        json.dumps(
            result,
            indent=4
        )
    )