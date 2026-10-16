# Lexi — Legal document classifier

Lexi is a responsive Streamlit app that classifies common legal documents using a transparent, local keyword-scoring system. It can identify non-disclosure agreements, court filings, affidavits, legal notices, employment documents, leases, privacy policies, and general contracts.

The app shows the most likely category, a plain-language match-strength label, matched phrases, and up to three alternative matches. It accepts pasted text or UTF-8 `.txt` / `.md` files and can download a classification report.

## How classification works

The classifier adds weights for phrases associated with each document type and ranks the categories. It is a heuristic, not a trained model; its match strength is not a probability. Results can be incomplete or wrong and should not replace professional legal review.

No AI API key or external AI service is used. For local runs, text is processed on your computer. When hosted on Streamlit Community Cloud, text is sent to the app server for processing and is not intentionally saved by the app.

## Run locally (Windows PowerShell)

1. Install Python 3.10 or newer.
2. Open PowerShell in this folder and create an environment:

   ```powershell
   python -m venv .venv
   ```

3. Install dependencies:

   ```powershell
   .\.venv\Scripts\python.exe -m pip install -r requirements.txt
   ```

4. Launch Lexi:

   ```powershell
   .\.venv\Scripts\python.exe -m streamlit run app.py
   ```

## Push to GitHub and deploy on Streamlit Community Cloud

1. Create a GitHub repository and push this project. The `.venv` folder is excluded by `.gitignore`.
2. In Streamlit Community Cloud, choose **Create app**, connect the repository, and set the main file to `app.py`.
3. Deploy. Community Cloud installs the packages listed in `requirements.txt`; no secrets or API keys are needed.

The `.streamlit/config.toml` file provides the app theme and headless server setting.
