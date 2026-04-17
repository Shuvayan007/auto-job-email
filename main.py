import streamlit as st
import re
import requests
import smtplib
from email.message import EmailMessage
import os

# ---------------- SESSION ----------------
if "default_resume_path" not in st.session_state:
    st.session_state.default_resume_path = "default_resume.pdf"

# ---------------- CONFIG ----------------
AZURE_OPENAI_ENDPOINT = "YOUR_ENDPOINT"
AZURE_OPENAI_KEY = "YOUR_KEY"
DEPLOYMENT_NAME = "gpt-4o-mini"

GMAIL_EMAIL = "your_email@gmail.com"
GMAIL_APP_PASSWORD = "your_app_password"  # NOT your real password

DEFAULT_RESUME_PATH = "default_resume.pdf"

# ---------------- FUNCTIONS ----------------

def extract_email(text):
    match = re.search(r"[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+", text)
    return match.group(0) if match else None


def call_azure_openai(text):
    url = f"{AZURE_OPENAI_ENDPOINT}/openai/deployments/{DEPLOYMENT_NAME}/chat/completions?api-version=2024-02-15-preview"
    
    headers = {
        "Content-Type": "application/json",
        "api-key": AZURE_OPENAI_KEY
    }

    prompt = f"""
    Extract the recruiter's FIRST NAME and COMPANY NAME from the following text.
    Return strictly in JSON format:
    {{
        "first_name": "",
        "company": ""
    }}

    TEXT:
    {text}
    """

    data = {
        "messages": [
            {"role": "system", "content": "You are an information extractor."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0
    }

    response = requests.post(url, headers=headers, json=data)
    result = response.json()

    content = result['choices'][0]['message']['content']
    return eval(content)  # ideally use json.loads()


def generate_email(first_name, company):
    return f"""
Dear {first_name},

Thank you for sharing the details and the opportunity with {company}.

Please find my updated resume attached along with the requested information below:

* Name: Shuvayan Pal
* Current Company: EY Global Delivery Services
* Current CTC: 6.5 LPA
* Expected CTC: 13–17 LPA
* Location: Kolkata
* Total Experience in Data Science: 3+ years
* Any Offers: No
* LinkedIn URL: https://www.linkedin.com/in/shuvayanpal/

I am currently serving my notice period, with my last working day on 8th June 2026.

A recent digital photograph has also been attached as requested.

Please let me know if any further information is required. I look forward to your response.

Warm regards,  
Shuvayan Pal  
📞 +91 8910227437  
📧 shuvayanpal2000@gmail.com
"""


def send_email(to_email, subject, body, resume_path):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = GMAIL_EMAIL
    msg['To'] = to_email
    msg.set_content(body)

    # Attach resume
    with open(resume_path, 'rb') as f:
        msg.add_attachment(
            f.read(),
            maintype='application',
            subtype='pdf',
            filename='Resume.pdf'
        )

    # Send email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(GMAIL_EMAIL, GMAIL_APP_PASSWORD)
        smtp.send_message(msg)


# ---------------- UI ----------------

st.title("🚀 LinkedIn Job Post → Auto Apply")

linkedin_text = st.text_area("Paste LinkedIn Job Post")

if os.path.exists(st.session_state.default_resume_path):
    st.info("📄 Default resume is set and will be used if no file is uploaded.")
else:
    st.warning("⚠️ No default resume found. Please upload and set one.")

uploaded_resume = st.file_uploader("Attach Resume (Optional)", type=["pdf"])

if uploaded_resume:
    # Save temp file
    temp_path = "temp_uploaded_resume.pdf"
    with open(temp_path, "wb") as f:
        f.write(uploaded_resume.read())

    st.success("Resume uploaded successfully ✅")

    # Make Default Button
    if st.button("⭐ Make this Default Resume"):
        with open(st.session_state.default_resume_path, "wb") as f:
            with open(temp_path, "rb") as temp_file:
                f.write(temp_file.read())

        st.success("🎯 This resume is now set as default!")

if st.button("Submit"):
    if not linkedin_text:
        st.error("Please paste the LinkedIn post")
    else:
        email = extract_email(linkedin_text)

        if not email:
            st.error("No email found in post")
        else:
            st.success(f"Email Found: {email}")

            data = call_azure_openai(linkedin_text)
            first_name = data.get("first_name", "Recruiter")
            company = data.get("company", "the company")

            st.write(f"Detected: {first_name} from {company}")

            email_body = generate_email(first_name, company)

            # Resume selection logic
            if uploaded_resume:
                resume_path = "temp_uploaded_resume.pdf"
            else:
                resume_path = st.session_state.default_resume_path

            subject = f"Application for Opportunity at {company}"

            send_email(email, subject, email_body, resume_path)

            st.success("✅ Email Sent Successfully!")