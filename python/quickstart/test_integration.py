#!/usr/bin/env python3
"""
Zero-Quota Integration Test - Veritier (Python)
================================================
Validates your complete Veritier integration - auth, extract, and verify -
WITHOUT consuming any quota. Uses a test API key and deterministic mock responses.

This file is designed to run in CI/CD pipelines or as a pre-deployment sanity check.

Usage:
  1. pip install httpx python-dotenv
  2. Create a test API key (vt_test_...) in your Veritier dashboard
  3. cp .env.example .env  and set VERITIER_TEST_KEY=vt_test_...
  4. python test_integration.py

Expected output:
  ✓ [1/5] API connectivity confirmed
  ✓ [2/5] Extract: 3 mock claims returned, no quota consumed
  ✓ [3/5] Extract: empty-state handling (mock_claims=0) works
  ✓ [4/5] Verify: happy-path (mock_verdict=True) - all verdicts True
  ✓ [5/5] Verify: error-path (mock_verdict=False) - all verdicts False
  ✓ All integration checks passed!

See https://veritier.ai/docs#testing for full documentation.
"""

import os
import sys
import httpx
from dotenv import load_dotenv

load_dotenv()

# Use a dedicated test key to avoid touching production quota
API_KEY = os.getenv("VERITIER_TEST_KEY") or os.getenv("VERITIER_API_KEY", "")
API_URL = os.getenv("VERITIER_API_URL", "https://api.veritier.ai")

if not API_KEY:
    print("✗ Error: VERITIER_TEST_KEY (or VERITIER_API_KEY) is not set.")
    print("  Create a test key (vt_test_...) at https://veritier.ai/dashboard")
    sys.exit(1)

if not API_KEY.startswith("vt_test_"):
    print("⚠ Warning: API key does not look like a test key (expected vt_test_... prefix).")
    print("  Using a production key here will consume your monthly quota.")
    print("  Create a test key at https://veritier.ai/dashboard → API Keys → Test\n")

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

SAMPLE_TEXT = (
    "Python was created by Guido van Rossum. "
    "The language was first released in 1991. "
    "Python is named after the British comedy group Monty Python."
)

failures = []


def check(condition: bool, label: str, detail: str = ""):
    if condition:
        print(f"  ✓ {label}")
    else:
        msg = f"  ✗ FAILED: {label}" + (f" - {detail}" if detail else "")
        print(msg)
        failures.append(label)


def run_test(step: int, total: int, name: str):
    print(f"\n[{step}/{total}] {name}")


print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print("  Veritier Zero-Quota Integration Test")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
print(f"  API URL: {API_URL}")
print(f"  Key:     {API_KEY[:12]}... (length: {len(API_KEY)})\n")

# ── [1/5] API Connectivity ───────────────────────────────────────────────────
run_test(1, 5, "API connectivity check")
try:
    resp = httpx.get(f"{API_URL}/health", timeout=10.0)
    check(resp.status_code in (200, 404), "Server reachable", f"status={resp.status_code}")
except Exception as exc:
    check(False, "Server reachable", str(exc))

# ── [2/5] Extract - 3 mock claims ────────────────────────────────────────────
run_test(2, 5, "Extract: mock_claims=3 (3 mock claims)")
try:
    resp = httpx.post(
        f"{API_URL}/v1/extract",
        headers=HEADERS,
        json={"text": SAMPLE_TEXT, "mock_claims": 3},
        timeout=30.0,
    )
    check(resp.status_code == 200, "HTTP 200 OK", f"got {resp.status_code}: {resp.text[:120]}")
    if resp.status_code == 200:
        data = resp.json()
        check(len(data.get("claims", [])) == 3, "3 mock claims returned", f"got {len(data.get('claims', []))}")
        check(data.get("is_test") is True, "Response body contains is_test=True")
        check(resp.headers.get("X-Veritier-Test-Mode") == "true", "X-Veritier-Test-Mode header = true")
        check(
            any("[TEST MODE]" in w for w in data.get("warnings", [])),
            "Test-mode warning present in warnings[]"
        )
except Exception as exc:
    check(False, "Extract request succeeded", str(exc))

# ── [3/5] Extract - empty state ──────────────────────────────────────────────
run_test(3, 5, "Extract: mock_claims=0 (empty-state handling)")
try:
    resp = httpx.post(
        f"{API_URL}/v1/extract",
        headers=HEADERS,
        json={"text": SAMPLE_TEXT, "mock_claims": 0},
        timeout=30.0,
    )
    check(resp.status_code == 200, "HTTP 200 OK", f"got {resp.status_code}: {resp.text[:120]}")
    if resp.status_code == 200:
        data = resp.json()
        check(data.get("claims") == [], "claims=[] (empty list)", f"got {data.get('claims')}")
        check(data.get("is_test") is True, "Response body contains is_test=True")
except Exception as exc:
    check(False, "Extract empty-state request succeeded", str(exc))

# ── [4/5] Verify - happy path (all True) ────────────────────────────────────
run_test(4, 5, "Verify: mock_verdict=True (all verdicts True)")
try:
    resp = httpx.post(
        f"{API_URL}/v1/verify",
        headers=HEADERS,
        json={"text": SAMPLE_TEXT, "mock_verdict": True},
        timeout=30.0,
    )
    check(resp.status_code == 200, "HTTP 200 OK", f"got {resp.status_code}: {resp.text[:120]}")
    if resp.status_code == 200:
        data = resp.json()
        results = data.get("results", [])
        check(len(results) == 3, "3 ClaimResult objects returned", f"got {len(results)}")
        check(all(r["verdict"] is True for r in results), "All verdicts = True")
        check(all(r["confidence_score"] == 1.0 for r in results), "All confidence_scores = 1.0")
        check(data.get("is_test") is True, "Response body contains is_test=True")
        check(resp.headers.get("X-Veritier-Test-Mode") == "true", "X-Veritier-Test-Mode header = true")
except Exception as exc:
    check(False, "Verify happy-path request succeeded", str(exc))

# ── [5/5] Verify - error path (all False) ───────────────────────────────────
run_test(5, 5, "Verify: mock_verdict=False (all verdicts False)")
try:
    resp = httpx.post(
        f"{API_URL}/v1/verify",
        headers=HEADERS,
        json={"text": SAMPLE_TEXT, "mock_verdict": False},
        timeout=30.0,
    )
    check(resp.status_code == 200, "HTTP 200 OK", f"got {resp.status_code}: {resp.text[:120]}")
    if resp.status_code == 200:
        data = resp.json()
        results = data.get("results", [])
        check(len(results) == 3, "3 ClaimResult objects returned", f"got {len(results)}")
        check(all(r["verdict"] is False for r in results), "All verdicts = False")
        check(all(r["confidence_score"] == 0.0 for r in results), "All confidence_scores = 0.0")
        check(data.get("is_test") is True, "Response body contains is_test=True")
except Exception as exc:
    check(False, "Verify error-path request succeeded", str(exc))

# ── Summary ──────────────────────────────────────────────────────────────────
print()
if not failures:
    print("✓ All integration checks passed!")
    print("  Zero quota was consumed. Switch to a production key for live fact-checking.")
    sys.exit(0)
else:
    print(f"✗ {len(failures)} check(s) failed:")
    for f in failures:
        print(f"  - {f}")
    sys.exit(1)
