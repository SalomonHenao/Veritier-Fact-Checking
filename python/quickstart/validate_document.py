#!/usr/bin/env python3
"""
Document Authenticity Scan - Veritier Quickstart (Python)
==========================================================
Runs a deep deep authenticity scan on a document URL or base64.
Detects tampering, extracts facts, and cross-references them against web evidence.

Usage:
  1. pip install httpx python-dotenv
  2. cp .env.example .env  (then add your API key)
  3. python validate_document.py

Get your free API key: https://veritier.ai/register
Full docs: https://veritier.ai/docs
"""

import os
import sys
import httpx
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("VERITIER_API_KEY", "")
API_URL = "https://api.veritier.ai"  # hardcoded - never sent to any other domain

if not API_KEY:
    print("❌ Error: VERITIER_API_KEY is not set.")
    print("  Get your free key at https://veritier.ai/register")
    sys.exit(1)

# 📄 Sample document URL to validate 📄📄📄📄📄📄📄📄📄📄📄📄📄📄📄📄
sample_url = "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"

print(f"📥 Input URL:\n   \"{sample_url}\"\n")
print("🔍 Running deep authenticity scan...\n")

response = httpx.post(
    f"{API_URL}/v1/validate",
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    },
    json={"document_url": sample_url},
    timeout=60.0,
)

if response.status_code != 200:
    print(f"❌ API error ({response.status_code}): {response.text}")
    sys.exit(1)

data = response.json()
risk_score = data.get("authenticity_risk_score", 0)
print(f"🛡️ Authenticity Risk Score: {risk_score}/100")

findings = data.get("findings", [])
print(f"\n📋 Extracted {len(findings)} findings:")
for i, finding in enumerate(findings, 1):
    print(f"  {i}. {finding}")

if data.get("warnings"):
    print(f"\n⚠️ Warnings: {'; '.join(data['warnings'])}")

print(f"\n⏱️ Rate limit: {response.headers.get('RateLimit-Remaining', '?')} requests remaining this minute")
