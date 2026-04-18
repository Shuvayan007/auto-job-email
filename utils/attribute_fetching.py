import json
from openai import OpenAI
from utils.config import load_config

config = load_config()

# Initialize client once
client = OpenAI(
    base_url=config['endpoint'],
    api_key=config["api_key"]
)


def get_name_and_company(text: str) -> dict:
    prompt = f"""
    Extract the following from the text:
    - Recruiter's FIRST NAME
    - COMPANY NAME

    Rules:
    - Return STRICT JSON only
    - Do NOT add explanation
    - If not found, return empty strings

    Format:
    {{
        "first_name": "",
        "company": ""
    }}

    TEXT:
    {text}
    """

    try:
        response = client.chat.completions.create(
            model=config["deployment"],  # e.g., gpt-4o-mini
            messages=[
                {"role": "system", "content": "You are a precise information extractor."},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )

        content = response.choices[0].message.content.strip()

        # Safe JSON parsing
        return json.loads(content)

    except Exception as e:
        print(f"Azure OpenAI Error: {str(e)}")

        return {
            "first_name": "Recruiter",
            "company": "the company"
        }