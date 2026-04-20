#!/usr/bin/env python3
"""
Disinformation Shield - Veritier Use Case (Python)
====================================================
Screens user-generated content, social media posts, or news snippets for
false claims before they spread. Acts as a truth firewall for platforms
that need to catch misinformation at the point of entry.

Unlike hallucination_audit (which targets AI-generated text), this example
targets human-authored content - viral posts, forwarded messages, and
news articles that may contain misleading or fabricated claims.

Usage:
  1. pip install httpx python-dotenv
  2. Set VERITIER_API_KEY in your .env
  3. python disinformation_shield.py

Get your free API key: https://veritier.ai/register
Full docs: https://veritier.ai/docs
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

# ── Simulated user-generated content (social media post / forwarded message) ─
incoming_content = (
    "BREAKING: The WHO just confirmed that drinking hot water with lemon "
    "cures the flu. A new study from Harvard Medical School published last "
    "week found that 98% of patients recovered within 24 hours. The CDC has "
    "already updated their official guidelines to recommend this treatment."
)

print("🛡  Veritier Disinformation Shield")
print("━" * 50)
print(f"\n📥 Incoming content:\n   \"{incoming_content}\"\n")
print("⏳ Screening for false claims...\n")

response = httpx.post(
    f"{API_URL}/v1/verify",
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    },
    json={"text": incoming_content},
    timeout=120.0,
)

if response.status_code != 200:
    print(f"✗ API error ({response.status_code}): {response.text}")
    sys.exit(1)

data = response.json()
results = data.get("results", [])

false_claims = [r for r in results if r.get("verdict") is False]
unverified_claims = [r for r in results if r.get("verdict") is None]
true_claims = [r for r in results if r.get("verdict") is True]

# ── Display results ──────────────────────────────────────────────────────
if false_claims:
    print(f"🚨 DISINFORMATION DETECTED ({len(false_claims)} false claim(s)):\n")
    for r in false_claims:
        print(f"  ❌ \"{r['claim']}\"")
        print(f"     Why it's false: {r.get('explanation', 'N/A')}")
        sources = r.get("source_urls", [])
        if sources:
            print(f"     Evidence: {', '.join(sources[:3])}")
        print()

if unverified_claims:
    print(f"⚠  UNVERIFIABLE CLAIMS ({len(unverified_claims)}):\n")
    for r in unverified_claims:
        print(f"  ❓ \"{r['claim']}\"")
        print(f"     Note: {r.get('explanation', 'Insufficient evidence to verify')}")
        print()

if true_claims:
    print(f"✅ Verified claims ({len(true_claims)}):")
    for r in true_claims:
        print(f"   ✓ \"{r['claim']}\"")

# ── Verdict summary ──────────────────────────────────────────────────────
print(f"\n{'━' * 50}")
total = len(results)
risk = len(false_claims) / total * 100 if total else 0

if false_claims:
    print(f"  🚫 BLOCKED - {len(false_claims)}/{total} claims are false ({risk:.0f}% disinformation rate)")
    print(f"  → This content should NOT be published or shared.")
elif unverified_claims:
    print(f"  ⚠  FLAGGED - {len(unverified_claims)}/{total} claims could not be verified")
    print(f"  → This content requires human review before publishing.")
else:
    print(f"  ✅ PASSED - All {total} claims verified as accurate")
    print(f"  → This content is safe to publish.")
