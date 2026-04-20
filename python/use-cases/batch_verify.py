#!/usr/bin/env python3
"""
Batch Verification with Rate Limit Handling - Veritier Use Case (Python)
=========================================================================
Processes multiple text snippets through the Veritier verification API,
respecting rate-limit headers and automatically backing off when throttled.

This is essential for production workloads where you're processing
content at scale (e.g., auditing a CMS, scanning a document library).

Usage:
  python batch_verify.py

Get your free API key: https://veritier.ai/register
"""

import os
import sys
import time
import httpx
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("VERITIER_API_KEY", "")
API_URL = os.getenv("VERITIER_API_URL", "https://api.veritier.ai")

if not API_KEY:
    print("✗ Error: VERITIER_API_KEY is not set.")
    print("  Get your free key at https://veritier.ai/register")
    sys.exit(1)

# ── Batch of texts to verify ───────────────────────────────────────────
texts = [
    "The speed of light is approximately 299,792 kilometers per second.",
    "Water boils at 100 degrees Celsius at sea level.",
    "The Amazon River is the longest river in the world.",
    "Jupiter has 79 confirmed moons as of 2024.",
    "The human body contains 206 bones.",
]

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

print(f"📦 Batch: {len(texts)} texts to verify\n")

for i, text in enumerate(texts, 1):
    print(f"── [{i}/{len(texts)}] ──────────────────────────────────────")
    print(f"📝 \"{text}\"")

    response = httpx.post(
        f"{API_URL}/v1/verify",
        headers=headers,
        json={"text": text, "grounding_mode": "web"},
        timeout=120.0,
    )

    # ── Handle rate limiting ────────────────────────────────────────────
    if response.status_code == 429:
        reset_seconds = int(response.headers.get("RateLimit-Reset", "60"))
        print(f"⏸ Rate limited. Waiting {reset_seconds}s before retrying...")
        time.sleep(reset_seconds)

        # Retry once after waiting
        response = httpx.post(
            f"{API_URL}/v1/verify",
            headers=headers,
            json={"text": text, "grounding_mode": "web"},
            timeout=120.0,
        )

    if response.status_code == 402:
        print("⚠ Monthly quota exhausted. Upgrade at https://veritier.ai/dashboard")
        break

    if response.status_code != 200:
        print(f"✗ Error ({response.status_code}): {response.text}")
        continue

    data = response.json()
    remaining = response.headers.get("RateLimit-Remaining", "?")
    reset = response.headers.get("RateLimit-Reset", "?")

    for res in data.get("results", []):
        verdict = res.get("verdict")
        icon = {True: "✅", False: "❌", None: "❓"}.get(verdict, "❓")
        print(f"   {icon} {res.get('claim')} → {verdict} (confidence: {res.get('confidence_score')})")

    print(f"   ── Remaining: {remaining} req/min | Reset: {reset}s\n")

    # ── Proactive backoff if running low on rate limit ──────────────────
    try:
        if int(remaining) <= 1:
            wait = int(reset) + 1
            print(f"⏸ Rate limit nearly exhausted. Waiting {wait}s...")
            time.sleep(wait)
    except (ValueError, TypeError):
        pass

print("✓ Batch complete.")
