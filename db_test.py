import time
from utils.email_db_supabase import can_send_email, log_email, cleanup_old_records

TEST_EMAIL = "test@example.com"

print("\n--- TEST START ---\n")

# Step 1: Ensure cleanup runs
print("Running cleanup...")
cleanup_old_records()
print("Cleanup done ✅\n")

# Step 2: Check if email can be sent initially
print("Checking if email can be sent (should be True)...")
can_send = can_send_email(TEST_EMAIL)
print("Result:", can_send)

if not can_send:
    print("❌ Unexpected: Email already exists in DB")
else:
    print("✅ OK: Email allowed\n")

# Step 3: Insert email
print("Inserting email...")
log_email(TEST_EMAIL)
print("Inserted ✅\n")

# Step 4: Check again (should now be blocked)
print("Checking again (should be False)...")
can_send = can_send_email(TEST_EMAIL)
print("Result:", can_send)

if can_send:
    print("❌ ERROR: Email should be blocked but isn't")
else:
    print("✅ OK: Email blocked as expected\n")

# Step 5: Simulate old record (manual wait or DB edit)
print("Simulating old record test...")

print("""
👉 To fully test cleanup:
1. Go to Supabase table
2. Manually reduce timestamp of this email to OLD value
3. Run script again
""")

print("\n--- TEST END ---")