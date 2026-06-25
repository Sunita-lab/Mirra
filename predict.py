import joblib
import numpy as np

from utils.emotion import get_emotion_score
from utils.clickbait import get_clickbait_score
from utils.evidence import get_evidence_score
from utils.gemini_analyzer import analyze_with_gemini

model = joblib.load("models/svm_model.pkl")
vectorizer = joblib.load("models/tfidf_vectorizer.pkl")


def analyze_text(text):

    text_vector = vectorizer.transform([text])

    prediction = model.predict(text_vector)

    decision_score = model.decision_function(text_vector)

    confidence = 1 / (1 + np.exp(-abs(decision_score[0])))
    confidence = confidence * 100

    confidence = round(confidence, 2)

    if confidence < 60:
        assessment = "Uncertain"

    elif prediction[0] == 1:
        assessment = "Likely Reliable"

    else:
        assessment = "Potentially Misleading"

    # ------------------------
    # Local Analysis
    # ------------------------

    local_results = {
        "assessment": assessment,
        "confidence": confidence,
        "emotion_score": get_emotion_score(text),
        "clickbait_score": get_clickbait_score(text),
        "evidence_score": get_evidence_score(text)
    }

    # ------------------------
    # Gemini Analysis
    # ------------------------

    ai_results = analyze_with_gemini(
        text,
        local_results
    )

    return {
        "local_analysis": local_results,
        "ai_analysis": ai_results
    }


if __name__ == "__main__":

    sample_text = """
    Scientists have discovered a new renewable energy source that could reduce global emissions by 40 percent over the next decade.
    """

    report = analyze_text(sample_text)

    print(report)