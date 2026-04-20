def generate_email() -> dict:
    # first_name = first_name or ""
    # company = company or "the company"

    subject = "Serving Notice Period | Data Scientist | 3.5+ Yrs | LWD: 8th June"

    html_body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6;">
        <p>Hi,</p>

        <p>
        I came across your LinkedIn post regarding the Data Scientist opening and wanted to share my profile for your consideration. Please find my resume attached.
        </p>

        <p>I am currently working as a <b>Data Scientist</b> at EY Global Delivery <b>Services</b> with <b>3.5+</b> years of experience, and my background aligns well with the requirements you mentioned.</p>

        <ul>
            <li><b>Current Organization:</b> EY Global Delivery Services</li>
            <li><b>Total Experience in Data Science:</b> 3.5+ years</li>
            <li><b>Last Working Day:</b> 8th June, 2026</li>
        </ul>

        <p>
        I am currently serving my notice period, with my last working day on 8th June 2026.
        </p>

        <p>
        Please let me know if any further information is required. 
        I look forward to your response.
        </p>

        <p>
        Warm regards,<br>
        <b>Shuvayan Pal</b><br>
        📞 +91 8910227437<br>
        📧 <a href="mailto:shuvayanpal2000@gmail.com">shuvayanpal2000@gmail.com</a><br>
        🔗 LinkedIn URL: <a href="https://www.linkedin.com/in/shuvayanpal/">https://www.linkedin.com/in/shuvayanpal/</a>
        </li>
        </p>
    </body>
    </html>
    """

    return {
        "subject": subject,
        "html_body": html_body
    }