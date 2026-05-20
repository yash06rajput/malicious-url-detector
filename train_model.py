import os
import joblib
import pandas as pd
from scipy.sparse import hstack, vstack
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

from feature_extractor import extract_url_features


# =========================
# Config
# =========================
DATASET_PATH = "url_dataset.csv"
ARTIFACTS_DIR = "artifacts"

os.makedirs(ARTIFACTS_DIR, exist_ok=True)


# =========================
# Load dataset
# =========================
print("Loading dataset...")

df = pd.read_csv(DATASET_PATH)

required_columns = ["url", "type"]

for col in required_columns:
    if col not in df.columns:
        raise ValueError(f"Missing required column: {col}")

df = df.dropna(subset=["url", "type"])
df["url"] = df["url"].astype(str)
df["type"] = df["type"].astype(str).str.lower()

print(f"Dataset loaded: {len(df)} samples")


# =========================
# Encode labels
# =========================
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(df["type"])

print("Detected classes:")
print(label_encoder.classes_)


# =========================
# Train/Test Split
# =========================
X_train_urls, X_test_urls, y_train, y_test = train_test_split(
    df["url"],
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print(f"Train samples: {len(X_train_urls)}")
print(f"Test samples: {len(X_test_urls)}")


# =========================
# TF-IDF Vectorizer
# =========================
print("Training TF-IDF vectorizer...")

vectorizer = TfidfVectorizer(
    analyzer="char",
    ngram_range=(3, 5),
    max_features=5000
)

X_train_tfidf = vectorizer.fit_transform(X_train_urls)
X_test_tfidf = vectorizer.transform(X_test_urls)


# =========================
# Engineered Features
# =========================
print("Extracting engineered URL features...")

X_train_numeric = vstack([
    extract_url_features(url)
    for url in X_train_urls
])

X_test_numeric = vstack([
    extract_url_features(url)
    for url in X_test_urls
])


# =========================
# Combine Features
# =========================
X_train = hstack([X_train_tfidf, X_train_numeric])
X_test = hstack([X_test_tfidf, X_test_numeric])


# =========================
# Train Model
# =========================
print("Training classifier...")

model = LogisticRegression(
    max_iter=2000,
    n_jobs=-1
)

model.fit(X_train, y_train)


# =========================
# Evaluation
# =========================
print("\nEvaluating model...")

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print(f"\nAccuracy: {accuracy * 100:.2f}%")

print("\nClassification Report:")
print(
    classification_report(
        y_test,
        y_pred,
        target_names=label_encoder.classes_
    )
)

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))


# =========================
# Save Artifacts
# =========================
print("\nSaving artifacts...")

joblib.dump(model, os.path.join(ARTIFACTS_DIR, "model.pkl"))
joblib.dump(vectorizer, os.path.join(ARTIFACTS_DIR, "tfidf_vectorizer.pkl"))
joblib.dump(label_encoder, os.path.join(ARTIFACTS_DIR, "label_encoder.pkl"))

print("\nTraining complete.")
print("Saved:")
print("artifacts/model.pkl")
print("artifacts/tfidf_vectorizer.pkl")
print("artifacts/label_encoder.pkl")