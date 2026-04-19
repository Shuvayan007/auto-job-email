import smtplib
from email.message import EmailMessage
from utils.config import load_config

config = load_config()


def send_email(to_email: str, subject: str, body: str, resume_path: str):
    try:
        sender_email = config["gmail_email"]
        app_password = config["gmail_app_password"]

        if not sender_email or not app_password:
            raise Exception("Gmail credentials missing in config")

        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = sender_email
        msg["To"] = to_email
        
        # Plain text fallback
        msg.set_content("This email requires an HTML-supported client.")

        # HTML content
        msg.add_alternative(body, subtype="html")

        # Attach Resume
        with open(resume_path, "rb") as f:
            msg.add_attachment(
                f.read(),
                maintype="application",
                subtype="pdf",
                filename="shuvayan_resume.pdf"
            )

        # Send Email
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(sender_email, app_password)
            smtp.send_message(msg)

        return True, "Email sent successfully ✅"

    except Exception as e:
        return False, str(e)