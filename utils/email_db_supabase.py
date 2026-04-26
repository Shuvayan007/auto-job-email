import requests
import time
from utils.config import load_config
from utils.logger import log_event

config = load_config()

SUPABASE_URL = config["supabase_url"]
SUPABASE_KEY = config["supabase_key"]

# ✅ IMPORTANT: match your working URL
TABLE_URL = f"{SUPABASE_URL}/rest/v1/email_logs"

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

TTL_SECONDS = 48 * 3600


# ---------------- CHECK ----------------
def can_send_email(email):
    cutoff = int(time.time()) - TTL_SECONDS

    params = {
        "email": f"eq.{email}",
        "timestamp": f"gte.{cutoff}"
    }

    response = requests.get(TABLE_URL, headers=HEADERS, params=params)
    # log_event("Supabase API", f"Response: {response.status_code} | Data: {response.text}")

    if response.status_code != 200:
        # log_event("Supabase API error", f"Status Code: {response.status_code} | Response: {response.text}") 
        raise Exception(f"Supabase Error: {response.text}")

    data = response.json()

    # log_event("Supabase API", f"Email Check Result for {email}: {data}")
    return len(data) == 0  # True = safe to send


# ---------------- INSERT ----------------
def log_email(email):
    payload = {
        "email": email,
        "timestamp": int(time.time())
    }

    response = requests.post(TABLE_URL, headers=HEADERS, json=payload)

    # log_event("Supabase API", f"Response: {response.status_code} | Data: {response.text}")

    if response.status_code not in (200, 201):
        # log_event("Supabase API error", f"Status Code: {response.status_code} | Response: {response.text}")
        raise Exception(f"Insert failed: {response.text}")


# ---------------- CLEANUP ----------------
def cleanup_old_records():
    cutoff = int(time.time()) - TTL_SECONDS

    delete_url = f"{TABLE_URL}?timestamp=lt.{cutoff}"

    response = requests.delete(delete_url, headers=HEADERS)
    # try:
    #     log_event("Supabase API", f"Cleanup Response: {response.status_code} | Data: {response.text}")
    # except:
    #     pass

    if response.status_code not in (200, 204):
        # try:
        #     log_event("Supabase API error", f"Status Code: {response.status_code} | Response: {response.text}")
        # except:
        #     pass
        raise Exception(f"Cleanup failed: {response.text}")