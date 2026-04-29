import json
from openai import OpenAI
from utils.config import load_config

config = load_config()

client = OpenAI(
    base_url=config['endpoint'],
    api_key=config["api_key"]
)


def generate_personalized_email(linkedin_text: str) -> dict:
    prompt = f"""
You are an expert job application email writer.

Your task is to:
1. Understand the LinkedIn job post carefully
2. Identify any recruiter instructions or required details
3. Generate a professional email strictly following those instructions

-------------------------------------

STRICT INSTRUCTIONS:
- Return STRICT JSON only
- Do NOT add explanation
- Subject MUST include "Serving Notice Period"
- Keep the email concise and recruiter-friendly
- Use clean HTML formatting (<p>, <ul>, <li>)
- If recruiter name not found → use "Hi Hiring Team,"
- Do NOT hallucinate details not present in candidate profile
- ONLY include details if:
  - explicitly mentioned in the job post OR
  - part of candidate’s standard profile

-------------------------------------

CRITICAL BEHAVIOR:

From the LinkedIn post, detect if recruiter is asking for:
- Current CTC
- Expected CTC
- Notice Period
- Location / Preferred Location
- Experience
- Skills
- Portfolio / Links
- Immediate joiner
- Any specific format

👉 If requested → INCLUDE them in a clean bullet section
👉 If NOT requested → DO NOT include unnecessarily

-------------------------------------

CANDIDATE DETAILS:

Name: Shuvayan Pal
Mobile: +91 8910227437
Email: shuvayanpal2000@gmail.com
LinkedIn: https://www.linkedin.com/in/shuvayanpal/
Location: Kolkata

Total Experience: 3.5+ years
Current Role: Data Scientist
Current Organization: EY Global Delivery Services

Skills: Python, Machine Learning, Generative AI

Current CTC: 7.3 LPA
Expected CTC: 15–17 LPA

Notice Period: 60 days
Serving Notice Period: Yes
Last Working Day: 8th June 2026

-------------------------------------

EMAIL STRUCTURE:

Subject:
<Generate a high open-rate subject including "Serving Notice Period">

HTML Body:

<p>Hi &lt;Recruiter Name or Hiring Team&gt;,</p>

<p>I hope you are doing well.</p>

<p>&lt;1 line referencing the job post / opportunity&gt;</p>

<p>I am currently working as a Data Scientist at EY Global Delivery Services with 3.5+ years of experience and am keen to explore relevant opportunities.</p>

<p><b>Quick details:</b></p>

<ul>
<li>Total experience: 3.5+ years</li>
<li>Current organization: EY Global Delivery Services</li>
<li>Notice period: 60 days (Serving Notice Period – LWD: 8th June 2026)</li>
</ul>

<!-- CONDITIONAL BLOCK -->
<p><b>Additional requested details:</b></p>
<ul>
<li>Include ONLY if explicitly asked in the job post</li>
</ul>

<p>&lt;Optional 1 short line aligning with role/company&gt;</p>

<p>I would be happy to connect and discuss how my experience can support your team’s requirements.</p>

<p>Thank you for your time and consideration. Looking forward to your response.</p>

<p>
Warm regards,<br>
Shuvayan Pal<br>
📞 +91 8910227437<br>
📧 shuvayanpal2000@gmail.com<br>
🔗 LinkedIn: https://www.linkedin.com/in/shuvayanpal/
</p>

-------------------------------------

INPUT LINKEDIN POST:
{linkedin_text}

-------------------------------------

OUTPUT FORMAT:
{{
  "subject": "",
  "html_body": ""
}}
"""

    try:
        response = client.chat.completions.create(
            model=config["deployment"],
            messages=[
                {"role": "system", "content": "You generate structured professional emails."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4
        )

        content = response.choices[0].message.content.strip()

        try:
            return json.loads(content)
        except:
            return {
                "subject": "Serving Notice Period | Data Scientist | 3.5+ Yrs",
                "html_body": content
            }

    except Exception as e:
        print(f"AI Email Error: {str(e)}")

        return {
            "subject": "Serving Notice Period | Data Scientist",
            "html_body": "<p>Error generating email</p>"
        }