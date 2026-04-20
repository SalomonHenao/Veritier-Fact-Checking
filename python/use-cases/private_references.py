#!/usr/bin/env python3
"""
Private Reference Grounding - Veritier Use Case (Python)
=========================================================
Verify claims against YOUR OWN documents instead of the open web.
This is essential for enterprise use cases where you need to validate
content against internal policies, research papers, or proprietary data.

Supports two reference types:
  - "text": raw text content from your documents
  - "url": a URL to a document Veritier will fetch

Usage:
  python private_references.py

Get your free API key: https://veritier.ai/register
"""

import os
import sys
import httpx
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("VERITIER_API_KEY", "")
API_URL = os.getenv("VERITIER_API_URL", "https://api.veritier.ai")

if not API_KEY:
    print("✗ Error: VERITIER_API_KEY is not set.")
    print("  Get your free key at https://veritier.ai/register")
    sys.exit(1)

# ── Your private reference document ────────────────────────────────────
company_policy = """
Acme Corp Employee Handbook (2026 Edition)
==========================================
- All employees receive 20 days of paid vacation per year.
- Remote work is permitted up to 3 days per week.
- The standard work week is 37.5 hours.
- Parental leave is 16 weeks for all parents.
- Annual performance reviews occur in March.
"""

# ── Text containing claims to verify against the reference ─────────────
text_to_verify = (
    "At Acme Corp, employees get 25 days of vacation per year. "
    "Remote work is allowed 3 days a week. "
    "Performance reviews happen every quarter."
)

print("📄 Reference document: Acme Corp Employee Handbook")
print(f"\n📝 Claims to verify:\n   \"{text_to_verify}\"\n")
print("⏳ Verifying against private reference...\n")

response = httpx.post(
    f"{API_URL}/v1/verify",
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    },
    json={
        "text": text_to_verify,
        "grounding_mode": "references",
        "grounding_references": [
            {"type": "text", "content": company_policy},
            # You can also add URL references:
            # {"type": "url", "content": "https://your-internal-docs.com/handbook"},
        ],
    },
    timeout=120.0,
)

if response.status_code != 200:
    print(f"✗ API error ({response.status_code}): {response.text}")
    sys.exit(1)

data = response.json()
results = data.get("results", [])

VERDICT_ICONS = {True: "✅", False: "❌", None: "❓"}

print(f"✓ Verified {len(results)} claim(s) against your reference:\n")
for res in results:
    verdict = res.get("verdict")
    icon = VERDICT_ICONS.get(verdict, "❓")
    print(f"  {icon} Claim: '{res.get('claim')}'")
    print(f"     Verdict:      {verdict}")
    print(f"     Confidence:   {res.get('confidence_score')}")
    print(f"     Explanation:  {res.get('explanation')}")
    if res.get("source_label"):
        print(f"     Source label: {res.get('source_label')}")
    print()
