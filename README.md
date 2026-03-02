# 🕌 Zakat Calculator

A comprehensive Zakat calculator with live gold & silver prices in INR.

## Features
- Live gold & silver prices (INR) via free API
- All asset categories: cash, gold, silver, investments, business
- Nisab check (Gold & Silver standards)
- Visual charts + CSV export
- FAQ & Islamic guidance

## Local Setup
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Free Deployment (Streamlit Cloud)
See deployment guide below.
```

---

## 🚀 FREE Deployment — Step by Step
```
STEP 1 — Create GitHub Repo
─────────────────────────────
1. Go to github.com → New Repository
2. Name it: zakat-calculator
3. Set to Public
4. Create repository

STEP 2 — Upload Files
─────────────────────────────
Upload these 3 files:
  • app.py
  • requirements.txt
  • README.md

STEP 3 — Deploy on Streamlit Cloud
─────────────────────────────
1. Go to → share.streamlit.io
2. Sign in with GitHub
3. Click "New app"
4. Select your repo → Branch: main → File: app.py
5. Click "Deploy!"

STEP 4 — Add Your API Key (Optional)
─────────────────────────────
In Streamlit Cloud → App Settings → Secrets:
Add:  GOLD_API_KEY = "your_goldapi_key_here"

STEP 5 — Share Your URL
─────────────────────────────
Your app will be live at:
https://your-name-zakat-calculator.streamlit.app