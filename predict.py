import joblib
import numpy as np

model = joblib.load("models/svm_model.pkl")
vectorizer = joblib.load("models/tfidf_vectorizer.pkl")


def analyze_text(text):
    text_vector = vectorizer.transform([text])

    prediction = model.predict(text_vector)

    decision_score = model.decision_function(text_vector)

    confidence = 1 / (1 + np.exp(-abs(decision_score[0])))
    confidence = confidence * 100

    assessment = (
        "Likely Reliable"
        if prediction[0] == 1
        else "Potentially Misleading"
    )

    return {
        "assessment": assessment,
        "confidence": round(confidence, 2)
    }


if __name__ == "__main__":
    sample_text = """
    Scientists have discovered a new renewable energy source that could reduce global emissions by 40 percent over the next decade.
    """

    report = analyze_text(sample_text)

    print(report)