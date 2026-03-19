# Malicious URL Detector

A machine learning-based system that detects whether a URL is **safe or malicious** using vectorization techniques and classification models.

---

## Features

✅ Detects phishing / malicious URLs  
✅ Uses vectorization (CountVectorizer / TF-IDF)  
✅ Trained ML classification model  
✅ Fast prediction system  
✅ Lightweight and efficient  

---

## How It Works

1. URLs are preprocessed and cleaned  
2. Text features are extracted using vectorization  
3. A trained ML model classifies the URL  
4. Output: **Safe** or **Malicious**

---

## Tech Stack

| Component        | Technology              |
|-----------------|------------------------|
| Language        | Python                 |
| ML Library      | Scikit-learn           |
| Vectorization   | CountVectorizer / TF-IDF |
| Model           | Logistic Regression / Naive Bayes |
| Dataset         | URL dataset (phishing + benign) |

---

## Model Pipeline

```text
URL → Preprocessing → Vectorizer → ML Model → Prediction

Input:  http://secure-login-paypal.verify-user.ru
Output: Malicious

Input:  https://www.google.com
Output: Safe

## project structure

malicious-url-detector/
│
├── app.py               # Main prediction script
├── train.py             # Model training script
├── model.pkl            # Trained ML model
├── vectorizer.pkl       # Saved vectorizer
├── dataset.csv          # Dataset (malicious + safe URLs)
├── requirements.txt     # Dependencies
└── README.md
