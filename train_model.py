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