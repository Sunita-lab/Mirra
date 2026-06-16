import pandas as pd

import os

print(os.path.exists("data/news_dataset/Fake.csv"))

print(os.getcwd())
print(os.listdir("."))
print(os.listdir("data"))

fake_df = pd.read_csv("data/news_dataset/Fake.csv")
true_df = pd.read_csv("data/news_dataset/True.csv")

print("Fake shape:", fake_df.shape)
print("True shape:", true_df.shape)

print("\nFake columns:")
print(fake_df.columns)

print("\nTrue columns:")
print(true_df.columns)

fake_df["label"] = 0
true_df["label"] = 1

df = pd.concat([fake_df, true_df], ignore_index=True)

print("Merged Shape:", df.shape)

print("\nLabel Distribution:")
print(df["label"].value_counts())

print("\nMissing Values:")
print(df.isnull().sum())

df["title"] = df["title"].fillna("")
df["text"] = df["text"].fillna("")

df["content"] = df["title"] + " " + df["text"]

print("\nSample Content:")
print(df["content"].iloc[0][:500])

from sklearn.model_selection import train_test_split
X = df["content"]
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("Train Size:", len(X_train))
print("Test Size:", len(X_test))

from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer(
    stop_words="english",
    max_features=20000
)

X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

print("TF-IDF Train Shape:", X_train_tfidf.shape)
print("TF-IDF Test Shape:", X_test_tfidf.shape)