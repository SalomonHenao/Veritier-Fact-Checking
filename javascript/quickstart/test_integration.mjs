/**
 * Veritier Zero-Quota Integration Test
 * =====================================
 * Verifies API connectivity and tests all three endpoints (extract, verify, validate)
 * using zero-quota mock parameters.
 */

import "dotenv/config";

// Use a dedicated test key to avoid touching production quota
const API_KEY = process.env.VERITIER_TEST_KEY || process.env.VERITIER_API_KEY || "";
const API_URL = process.env.API_URL || "https://api.veritier.ai";

if (!API_KEY) {
  console.error("❌ Error: VERITIER_TEST_KEY (or VERITIER_API_KEY) is not set.");
  console.error("  Create a test key (vt_test_...) at https://veritier.ai/dashboard");
  process.exit(1);
}

if (!API_KEY.startsWith("vt_test_")) {
  console.warn("⚠️ Warning: API key does not look like a test key (expected vt_test_... prefix).");
  console.warn("  Using a production key here will consume your monthly quota.");
}

const HEADERS = {
  Authorization: `Bearer ${API_KEY}`,
  "Content-Type": "application/json",
};

const SAMPLE_TEXT =
  "Python was created by Guido van Rossum. " +
  "The language was first released in 1991. " +
  "Python is named after the British comedy group Monty Python.";

const failures = [];

function check(condition, label, detail = "") {
  if (condition) {
    console.log(`  ✓ ${label}`);
  } else {
    const msg = `  ❌ FAILED: ${label}` + (detail ? ` - ${detail}` : "");
    console.log(msg);
    failures.push(label);
  }
}

function runTest(step, total, name) {
  console.log(`\n[${step}/${total}] ${name}`);
}

async function fetchWithTimeout(resource, options = {}) {
  const { timeout = 30000 } = options;
  const controller = new AbortController();
  const id = setTimeout(() => controller.abort(), timeout);
  const response = await fetch(resource, {
    ...options,
    signal: controller.signal
  });
  clearTimeout(id);
  return response;
}

async function runAllTests() {
  console.log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
  console.log("  Veritier Zero-Quota Integration Test");
  console.log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n");
  console.log(`  API URL: ${API_URL}`);
  console.log(`  Key:     ${API_KEY.slice(0, 12)}... (length: ${API_KEY.length})\n`);

  // ─── [1/6] API Connectivity ──────────────────────────────────────────────────
  runTest(1, 6, "API connectivity check");
  try {
    const resp = await fetchWithTimeout(`${API_URL}/health`, { timeout: 10000 });
    check([200, 404].includes(resp.status), "Server reachable", `status=${resp.status}`);
  } catch (err) {
    check(false, "Server reachable", err.message);
  }

  // ─── [2/6] Extract - 3 mock claims ───────────────────────────────────────────
  runTest(2, 6, "Extract: mock_claims=3 (3 mock claims)");
  try {
    const resp = await fetchWithTimeout(`${API_URL}/v1/extract`, {
      method: "POST",
      headers: HEADERS,
      body: JSON.stringify({ text: SAMPLE_TEXT, mock_claims: 3 })
    });
    const text = await resp.text();
    check(resp.status === 200, "HTTP 200 OK", `got ${resp.status}: ${text.slice(0, 120)}`);
    if (resp.status === 200) {
      const data = JSON.parse(text);
      const claims = data.claims || [];
      check(claims.length === 3, "3 mock claims returned", `got ${claims.length}`);
      check(data.is_test === true, "Response body contains is_test=true");
    }
  } catch (err) {
    check(false, "Extract request succeeded", err.message);
  }

  // ─── [3/6] Extract - empty state ─────────────────────────────────────────────
  runTest(3, 6, "Extract: mock_claims=0 (empty-state handling)");
  try {
    const resp = await fetchWithTimeout(`${API_URL}/v1/extract`, {
      method: "POST",
      headers: HEADERS,
      body: JSON.stringify({ text: SAMPLE_TEXT, mock_claims: 0 })
    });
    const text = await resp.text();
    check(resp.status === 200, "HTTP 200 OK", `got ${resp.status}: ${text.slice(0, 120)}`);
    if (resp.status === 200) {
      const data = JSON.parse(text);
      check(Array.isArray(data.claims) && data.claims.length === 0, "claims=[] (empty list)");
      check(data.is_test === true, "Response body contains is_test=true");
    }
  } catch (err) {
    check(false, "Extract empty-state request succeeded", err.message);
  }

  // ─── [4/6] Verify - happy path (all True) ────────────────────────────────────
  runTest(4, 6, "Verify: mock_verdict=true (all verdicts True)");
  try {
    const resp = await fetchWithTimeout(`${API_URL}/v1/verify`, {
      method: "POST",
      headers: HEADERS,
      body: JSON.stringify({ text: SAMPLE_TEXT, mock_verdict: true })
    });
    const text = await resp.text();
    check(resp.status === 200, "HTTP 200 OK", `got ${resp.status}: ${text.slice(0, 120)}`);
    if (resp.status === 200) {
      const data = JSON.parse(text);
      const results = data.results || [];
      check(results.length === 3, "3 ClaimResult objects returned", `got ${results.length}`);
      check(results.every(r => r.verdict === true), "All verdicts = true");
      check(results.every(r => r.confidence_score === 1.0), "All confidence_scores = 1.0");
      check(data.is_test === true, "Response body contains is_test=true");
    }
  } catch (err) {
    check(false, "Verify happy-path request succeeded", err.message);
  }

  // ─── [5/6] Verify - error path (all False) ───────────────────────────────────
  runTest(5, 6, "Verify: mock_verdict=false (all verdicts False)");
  try {
    const resp = await fetchWithTimeout(`${API_URL}/v1/verify`, {
      method: "POST",
      headers: HEADERS,
      body: JSON.stringify({ text: SAMPLE_TEXT, mock_verdict: false })
    });
    const text = await resp.text();
    check(resp.status === 200, "HTTP 200 OK", `got ${resp.status}: ${text.slice(0, 120)}`);
    if (resp.status === 200) {
      const data = JSON.parse(text);
      const results = data.results || [];
      check(results.length === 3, "3 ClaimResult objects returned", `got ${results.length}`);
      check(results.every(r => r.verdict === false), "All verdicts = false");
      check(results.every(r => r.confidence_score === 0.0), "All confidence_scores = 0.0");
      check(data.is_test === true, "Response body contains is_test=true");
    }
  } catch (err) {
    check(false, "Verify error-path request succeeded", err.message);
  }

  // ─── [6/6] Validate - authentic document ─────────────────────────────────────
  runTest(6, 6, "Validate: mock_validation=true (authentic document)");
  try {
    const resp = await fetchWithTimeout(`${API_URL}/v1/validate`, {
      method: "POST",
      headers: HEADERS,
      body: JSON.stringify({ url: "https://example.com/doc.pdf", mock_validation: true })
    });
    const text = await resp.text();
    check(resp.status === 200, "HTTP 200 OK", `got ${resp.status}: ${text.slice(0, 120)}`);
    if (resp.status === 200) {
      const data = JSON.parse(text);
      check(data.authenticity_score === 100 || data.fraud_risk_score === 0, "authenticity_score = 100 or risk = 0");
      check(data.is_authentic === true || data.verdict === "authentic", "is_authentic = true or verdict = authentic");
      check(data.is_test === true, "Response body contains is_test=true");
    }
  } catch (err) {
    check(false, "Validate request succeeded", err.message);
  }

  // ─── Summary ─────────────────────────────────────────────────────────────────
  console.log();
  if (failures.length === 0) {
    console.log("✓ All integration checks passed!");
    console.log("  Zero quota was consumed. Switch to a production key for live fact-checking.");
    process.exit(0);
  } else {
    console.log(`❌ ${failures.length} check(s) failed:`);
    failures.forEach(f => console.log(`  - ${f}`));
    process.exit(1);
  }
}

runAllTests();
