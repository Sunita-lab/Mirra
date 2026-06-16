import joblib

# Load saved artifacts
model = joblib.load("models/svm_model.pkl")
vectorizer = joblib.load("models/tfidf_vectorizer.pkl")

# Sample input
text = """
Scientists have discovered a new renewable energy source that could reduce global emissions by 40 percent over the next decade.
"""

# Transform text
text_vector = vectorizer.transform([text])

# Predict
prediction = model.predict(text_vector)

if prediction[0] == 1:
    print("Likely Reliable")
else:
    print("Potentially Misleading")

decision_score = model.decision_function(text_vector)

print("Decision Score:", decision_score[0])

import numpy as np
confidence = 1 / (1 + np.exp(-abs(decision_score[0])))
confidence = confidence * 100

print(f"Confidence: {confidence:.2f}%")