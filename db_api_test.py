import requests
import time
from utils.config import load_config

config = load_config()

SUPABASE_URL = config["supabase_url"]
SUPABASE_KEY = config["supabase_key"]

url = f"{SUPABASE_URL}/rest/v1/email_logs"

print(f"[{SUPABASE_KEY}]")
print("Dot count:", SUPABASE_KEY.count("."))

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

payload = {
    "email": "manual@test.com",
    "timestamp": int(time.time())
}

res = requests.post(url, headers=headers, json=payload)
print(res.status_code, res.text)