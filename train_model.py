import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score, classification_report


def load_data():
    fake_df = pd.read_csv("data/news_dataset/Fake.csv")
    true_df = pd.read_csv("data/news_dataset/True.csv")

    fake_df["label"] = 0
    true_df["label"] = 1

    return pd.concat([fake_df, true_df], ignore_index=True)


def preprocess_data(df):
    df["title"] = df["title"].fillna("")
    df["text"] = df["text"].fillna("")

    df["content"] = df["title"] + " " + df["text"]

    return df


def split_data(df):
    X = df["content"]
    y = df["label"]

    return train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )


def vectorize_data(X_train, X_test):
    vectorizer = TfidfVectorizer(
        stop_words="english",
        max_features=20000
    )

    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)

    return vectorizer, X_train_tfidf, X_test_tfidf


def train_model(X_train_tfidf, y_train):
    model = LinearSVC()

    model.fit(X_train_tfidf, y_train)

    return model


def evaluate_model(model, X_test_tfidf, y_test):
    predictions = model.predict(X_test_tfidf)

    accuracy = accuracy_score(y_test, predictions)

    print(f"\nAccuracy: {accuracy:.4f}")

    print("\nClassification Report:")
    print(classification_report(y_test, predictions))


def save_artifacts(model, vectorizer):
    joblib.dump(model, "models/svm_model.pkl")
    joblib.dump(vectorizer, "models/tfidf_vectorizer.pkl")

    print("\nArtifacts saved successfully.")


def main():
    print("Loading dataset...")

    df = load_data()

    print(f"Dataset Shape: {df.shape}")

    df = preprocess_data(df)

    X_train, X_test, y_train, y_test = split_data(df)

    vectorizer, X_train_tfidf, X_test_tfidf = vectorize_data(
        X_train,
        X_test
    )

    model = train_model(
        X_train_tfidf,
        y_train
    )

    evaluate_model(
        model,
        X_test_tfidf,
        y_test
    )

    save_artifacts(
        model,
        vectorizer
    )


if __name__ == "__main__":
    main()