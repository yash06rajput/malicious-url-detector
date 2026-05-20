# 🛡️ ThreatShield AI

<div align="center">

# AI-Powered Malicious URL Detection Engine

Detect phishing, malware, defacement, and suspicious URLs in real-time using machine learning.

🚀 **Live Demo:** https://threatshield-ai.onrender.com  
💻 **GitHub Repository:** https://github.com/yash06rajput/malicious-url-detector

</div>

---

## 📸 Demo Screenshots

### Threat Detection Interface
![ThreatShield UI](screenshots/homepage.png)

### Malicious URL Detection
![Malicious Detection](screenshots/malicious.png)

### Safe URL Detection
![Safe Detection](screenshots/safe.png)

> Replace these images with your screenshots inside a `/screenshots` folder.

---

## ✨ Features

✅ Real-time malicious URL scanning  
✅ Detects phishing and suspicious domains  
✅ Machine learning-powered classification engine  
✅ Confidence score prediction  
✅ Modern responsive cyber-themed UI  
✅ Public live deployment  
✅ Fast inference with pre-trained model  
✅ Clean Flask backend architecture  

---

## 🌐 Live Demo

Try the live product here:

### https://threatshield-ai.onrender.com

Test URLs:

**Malicious-like example**
```bash
http://secure-login-paypal.verify-user.ru
```

**Safe example**
```bash
https://google.com
```

---

## 🧠 How It Works

ThreatShield AI analyzes submitted URLs using a trained machine learning model.

Pipeline:

```text
User URL Input
      ↓
Feature Extraction
      ↓
Text Vectorization (TF-IDF)
      ↓
Machine Learning Classification
      ↓
Confidence Scoring
      ↓
Threat Verdict
```

The system determines whether the URL is:

- 🟢 BENIGN
- 🟠 SUSPICIOUS
- 🔴 MALICIOUS (future version)

---

## 🏗️ Architecture

### Frontend
- HTML5
- CSS3
- JavaScript

### Backend
- Flask
- Python

### Machine Learning
- Scikit-learn
- TF-IDF Vectorization
- Logistic Regression / Classification Model

### Deployment
- Render

---

## 📂 Project Structure

```bash
malicious-url-detector/
│
├── app.py                     # Flask application
├── train_model.py            # Model training script
├── feature_extractor.py      # Feature engineering
├── requirements.txt
├── README.md
│
├── artifacts/
│   ├── model.pkl
│   ├── tfidf_vectorizer.pkl
│   └── label_encoder.pkl
│
├── templates/
│   └── index.html
│
├── static/
│   ├── style.css
│   └── app.js
│
└── screenshots/
```

---

## ⚙️ Installation & Local Setup

Clone the repository:

```bash
git clone https://github.com/yash06rajput/malicious-url-detector.git
cd malicious-url-detector
```

Create virtual environment:

```bash
python -m venv venv
```

Activate environment:

### Mac/Linux
```bash
source venv/bin/activate
```

### Windows
```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run locally:

```bash
python app.py
```

Open:

```bash
http://127.0.0.1:5000
```

---

## 🔬 Machine Learning Details

ThreatShield AI uses:

### Feature Engineering
URL lexical analysis:
- URL length
- special characters
- suspicious keyword patterns
- domain structure
- token characteristics

### Vectorization
TF-IDF vectorization converts URLs into numerical representations for model prediction.

### Classification
Supervised classification model trained to distinguish:
- malicious URLs
- benign URLs

---

## 🎯 Example Results

### Example 1

Input:
```text
http://secure-login-paypal.verify-user.ru
```

Prediction:
```text
SUSPICIOUS
Confidence: 97.92%
```

---

### Example 2

Input:
```text
https://google.com
```

Prediction:
```text
BENIGN
Confidence: 99%
```

---

## 🚀 Future Improvements

Planned v2 upgrades:

- WHOIS domain intelligence
- DNS reputation analysis
- VirusTotal API integration
- XGBoost / LightGBM models
- Deep learning URL classification
- Browser extension integration
- REST API endpoint
- Threat history dashboard
- Dark/light mode switch
- User authentication

---

## 🛠 Deployment

ThreatShield AI is deployed on Render.

Build command:

```bash
pip install -r requirements.txt
```

Start command:

```bash
gunicorn app:app
```

---

## 👨‍💻 Author

**Yash Rajput**

B.Tech CSE | AI/ML Projects | Cybersecurity Enthusiast | Builder

GitHub:
https://github.com/yash06rajput

---

## ⭐ Support

If you like this project:

⭐ Star the repository  
🍴 Fork it  
🚀 Share it  

---

## 📜 License

This project is for educational and portfolio purposes.
