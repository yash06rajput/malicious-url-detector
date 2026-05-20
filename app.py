from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np
from scipy.sparse import hstack
from feature_extractor import extract_url_features
from urllib.parse import urlparse
import os

app = Flask(__name__)

# ============================
# Load trained artifacts
# ============================
MODEL_PATH = "artifacts/model.pkl"
VECTORIZER_PATH = "artifacts/tfidf_vectorizer.pkl"
LABEL_ENCODER_PATH = "artifacts/label_encoder.pkl"

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(
        "Model not found. Please run train_model.py first."
    )

model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)
label_encoder = joblib.load(LABEL_ENCODER_PATH)

# ============================
# Trusted domains
# ============================
TRUSTED_DOMAINS = [
    "google.com",
    "youtube.com",
    "amazon.in",
    "amazon.com",
    "microsoft.com",
    "openai.com",
    "github.com",
    "linkedin.com",
    "apple.com",
    "upsc.gov.in",
    "upsconline.nic.in",
    "nic.in"
]

TRUSTED_SUFFIXES = [
    ".gov.in",
    ".nic.in",
    ".edu",
    ".ac.in"
]

# ============================
# Threat explanations
# ============================
THREAT_INFO = {
    "benign": {
        "severity": "safe",
        "message": "This URL appears legitimate and safe."
    },
    "phishing": {
        "severity": "critical",
        "message": "This URL shows phishing indicators and may attempt credential theft."
    },
    "malware": {
        "severity": "danger",
        "message": "This URL may host malware or malicious payloads."
    },
    "defacement": {
        "severity": "warning",
        "message": "This URL resembles defacement-related suspicious patterns."
    },
    "suspicious": {
        "severity": "warning",
        "message": "This URL needs manual verification."
    }
}

# ============================
# Helper functions
# ============================
def normalize_domain(url):
    try:
        parsed = urlparse(url)
        domain = parsed.netloc.lower()

        if domain.startswith("www."):
            domain = domain[4:]

        return domain
    except:
        return ""


def is_trusted_domain(url):
    domain = normalize_domain(url)

    if domain in TRUSTED_DOMAINS:
        return True

    for suffix in TRUSTED_SUFFIXES:
        if domain.endswith(suffix):
            return True

    return False


# ============================
# Routes
# ============================
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()

        if not data or "url" not in data:
            return jsonify({
                "error": "URL is required."
            }), 400

        url = data["url"].strip()

        if not url:
            return jsonify({
                "error": "Empty URL provided."
            }), 400

        # Add protocol if missing
        if not url.startswith(("http://", "https://")):
            url = "http://" + url

        # TRUSTED DOMAIN OVERRIDE
        if is_trusted_domain(url):
            threat_meta = THREAT_INFO["benign"]

            return jsonify({
                "url": url,
                "prediction": "BENIGN",
                "confidence": 99.0,
                "severity": threat_meta["severity"],
                "message": threat_meta["message"]
            })

        # TF-IDF features
        tfidf_features = vectorizer.transform([url])

        # Numeric engineered features
        numeric_features = extract_url_features(url)

        # Combine
        combined_features = hstack([
            tfidf_features,
            numeric_features
        ])

        # Predict
        prediction_encoded = model.predict(combined_features)[0]
        probabilities = model.predict_proba(combined_features)[0]

        prediction_label = label_encoder.inverse_transform(
            [prediction_encoded]
        )[0].lower()

        confidence = float(np.max(probabilities) * 100)

        # UNCERTAINTY LOGIC
        if prediction_label != "benign" and confidence < 98:
            prediction_label = "suspicious"

        threat_meta = THREAT_INFO.get(
            prediction_label,
            {
                "severity": "unknown",
                "message": "Threat type unknown."
            }
        )

        return jsonify({
            "url": url,
            "prediction": prediction_label.upper(),
            "confidence": round(confidence, 2),
            "severity": threat_meta["severity"],
            "message": threat_meta["message"]
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


@app.route("/health")
def health():
    return jsonify({
        "status": "ok",
        "service": "ThreatShield AI"
    })


# ============================
# Run server
# ============================
if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0",
        port=5001
    )