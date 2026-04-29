import streamlit as st
import re
import os
from utils.ai_email_generator import generate_personalized_email
from utils.email_generator import generate_email
from utils.email_sender import send_email
import shutil
import time
import uuid
from utils.email_db_supabase import can_send_email, log_email, cleanup_old_records
from utils.logger import log_event

def cleanup_old_sessions(base_dir="resumes", max_age_hours=6):
    now = time.time()

    for folder in os.listdir(base_dir):
        path = os.path.join(base_dir, folder)

        if os.path.isdir(path):
            if now - os.path.getmtime(path) > max_age_hours * 3600:
                shutil.rmtree(path)

# ---------------- FUNCTIONS ----------------

def extract_email(text):
    match = re.search(r"[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+", text)
    return match.group(0) if match else None

# ---------------- RESUME FOLDER ----------------

# Root resumes folder
BASE_RESUME_DIR = "resumes"

# ---------------- SESSION ----------------

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
    st.caption(f"Created Session ID: {st.session_state.session_id}")
    cleanup_old_records()

# Email counter
if "email_sent_count" not in st.session_state:
    st.session_state.email_sent_count = 0

if "ready_to_send" not in st.session_state:
    st.session_state.ready_to_send = False

# Reset trigger
if "reset_form" not in st.session_state:
    st.session_state.reset_form = False

SESSION_DIR = os.path.join(BASE_RESUME_DIR, st.session_state.session_id)

# Create session-specific folder
os.makedirs(SESSION_DIR, exist_ok=True)
log_event(SESSION_DIR, "Session started")

expected_path = os.path.join(SESSION_DIR, "default_resume.pdf")

if st.session_state.get("default_resume_path") != expected_path:
    st.session_state.default_resume_path = expected_path

def santize_email(email):
    """Sanitize email by removing leading/trailing whitespace and converting to lowercase."""
    if email[-1] == ".":
        email = email[:-1]
    if " " in email:
        email = email.replace(" ", "")
    return email.strip().lower()

# ---------------- UI ----------------

if st.session_state.get("reset_form"):
    st.session_state.linkedin_input = ""
    st.session_state.reset_form = False

st.title("🚀 LinkedIn Job Post → Auto Apply")
st.metric("📤 Emails Sent This Session", st.session_state.email_sent_count)

linkedin_text = st.text_area(
    "Paste LinkedIn Job Post",
    key="linkedin_input"
)

personalize = st.checkbox("✨ Personalize Email (AI - Optional)")

if os.path.exists(st.session_state.default_resume_path):
    st.info("📄 Default resume is set and will be used if no file is uploaded.")
else:
    st.warning("⚠️ No default resume found. Please upload and set one.")

uploaded_resume = st.file_uploader("Attach Resume (Optional)", type=["pdf"])

if uploaded_resume:
    # Save temp file
    temp_path = os.path.join(SESSION_DIR, "temp_uploaded_resume.pdf")
    with open(temp_path, "wb") as f:
        f.write(uploaded_resume.read())

    log_event(SESSION_DIR, "Resume uploaded")
    st.success("Resume uploaded successfully ✅")

    # Make Default Button
    if st.button("⭐ Make this Default Resume"):
        with open(st.session_state.default_resume_path, "wb") as f:
            with open(temp_path, "rb") as temp_file:
                f.write(temp_file.read())

        log_event(SESSION_DIR, "Default resume updated")
        st.success("🎯 This resume is now set as default!")

if st.button("Submit"):
    log_event(SESSION_DIR, "LinkedIn post received")
    if not linkedin_text:
        st.error("Please paste the LinkedIn post")
    else:
        email = extract_email(linkedin_text)

        if not email:
            log_event(SESSION_DIR, "No email found in post")
            st.error("No email found in post")
        else:
            log_event(SESSION_DIR, f"Email extracted: {email}")
            email = santize_email(email)
            st.success(f"Email Found: {email}")

            st.session_state.recipient_email = email

            st.session_state.ready_to_send = True
            # else:
            #     st.error("❌ Unable to fetch details!")

if st.session_state.get("ready_to_send"):

    email = st.session_state.recipient_email

    # email_content = generate_email()
    if personalize:
        email_content = generate_personalized_email(linkedin_text)
    else:
        email_content = generate_email()
    subject = email_content["subject"]
    html_body = email_content["html_body"]

    st.subheader("📧 Email Preview")
    st.iframe(html_body, height=400)

    # Resume logic
    if uploaded_resume:
        resume_path = os.path.join(SESSION_DIR, "temp_uploaded_resume.pdf")
    else:
        resume_path = st.session_state.default_resume_path

    if not can_send_email(email):
        log_event(SESSION_DIR, f"Blocked: Email already sent in last 48h → {email}")
        st.error("❌ Email already sent in last 48 hours")
    else:
        log_event(SESSION_DIR, f"Attempting to send email to {email}")
        success, message = send_email(
            to_email=email,
            subject=subject,
            body=html_body,
            resume_path=resume_path
        )

        if success:
            log_event(SESSION_DIR, f"Email sent successfully to {email}")
            st.session_state.email_sent_count += 1
            st.success(f"{message} | Total Sent: {st.session_state.email_sent_count}")
            log_email(email)
            st.toast("Email sent 🚀")

            st.session_state.reset_form = True
            st.session_state.ready_to_send = False

            time.sleep(2)
            st.rerun()
        else:
            log_event(SESSION_DIR, f"Email failed to {email} | Error: {message}")
            st.error(f"Failed: {message}")

if st.button("❌ Exit Session"):
    # try:
    #     shutil.rmtree(SESSION_DIR)
    # except Exception as e:
    #     st.error(f"Error deleting session: {e}")

    # Clear session state
    for key in list(st.session_state.keys()):
        del st.session_state[key]

    log_event(SESSION_DIR, "Session cleared and exited")
    st.success("Session cleared successfully ✅")
    time.sleep(2)
    st.rerun()