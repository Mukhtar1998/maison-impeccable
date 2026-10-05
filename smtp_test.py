#!/usr/bin/env python3
"""
SMTP Connection Tester
Run this to verify Gmail SMTP is working
"""

import os
import smtplib
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load environment
load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SMTP_TO = os.getenv("SMTP_TO")
EMAIL_FROM = os.getenv("EMAIL_FROM", SMTP_USER)

print("=" * 60)
print("MAISON IMPECCABLE - SMTP TESTER")
print("=" * 60)

# Check environment
print("\n1. Checking environment variables...")
print(f"   SMTP_HOST: {SMTP_HOST or '❌ MISSING'}")
print(f"   SMTP_PORT: {SMTP_PORT or '❌ MISSING'}")
print(f"   SMTP_USER: {SMTP_USER[:10] + '***' if SMTP_USER else '❌ MISSING'}")
print(f"   SMTP_PASSWORD: {'***' if SMTP_PASSWORD else '❌ MISSING'} ({len(SMTP_PASSWORD)} chars)" if SMTP_PASSWORD else "   SMTP_PASSWORD: ❌ MISSING")
print(f"   SMTP_TO: {SMTP_TO or '❌ MISSING'}")
print(f"   EMAIL_FROM: {EMAIL_FROM or '❌ MISSING'}")

if not all([SMTP_HOST, SMTP_USER, SMTP_PASSWORD, SMTP_TO]):
    print("\n❌ Configuration incomplete. Fix .env file.")
    exit(1)

# Test connection
print("\n2. Testing SMTP connection...")
try:
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=10) as server:
        print(f"   ✓ Connected to {SMTP_HOST}:{SMTP_PORT}")
        
        print("   Initiating TLS...")
        server.starttls()
        print("   ✓ TLS secured")
        
        print(f"   Logging in as {SMTP_USER}...")
        server.login(SMTP_USER, SMTP_PASSWORD)
        print("   ✓ Authentication successful")

except smtplib.SMTPAuthenticationError as e:
    print(f"   ❌ Authentication failed: {e}")
    print("   → Check SMTP_USER and SMTP_PASSWORD in .env")
    print("   → Make sure you're using an App Password, not your regular password")
    exit(1)

except smtplib.SMTPException as e:
    print(f"   ❌ SMTP error: {e}")
    exit(1)

except Exception as e:
    print(f"   ❌ Connection error: {e}")
    print("   → Check SMTP_HOST and SMTP_PORT")
    print("   → Make sure port 587 is not blocked by firewall")
    exit(1)

# Test email send
print("\n3. Sending test email...")
try:
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Test Email - Maison Impeccable"
    msg["From"] = EMAIL_FROM
    msg["To"] = SMTP_TO
    
    body = """
This is a test email from Maison Impeccable server.

If you receive this, SMTP is configured correctly.

---
Sent at: """ + __import__("datetime").datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    msg.attach(MIMEText(body, "plain"))
    
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=10) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(msg)
    
    print(f"   ✓ Email sent to {SMTP_TO}")

except Exception as e:
    print(f"   ❌ Failed to send email: {e}")
    exit(1)

print("\n" + "=" * 60)
print("✓ ALL TESTS PASSED!")
print("=" * 60)
print("\nYour SMTP is configured correctly.")
print("The server is ready to send emails.")
print("\nStart the app with: python server.py")
