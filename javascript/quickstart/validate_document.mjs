/**
 * Document Authenticity Scan - Veritier Quickstart (JavaScript)
 * ==============================================================
 * Runs a deep deep authenticity scan on a document URL or base64.
 * Detects tampering, extracts facts, and cross-references them against web evidence.
 *
 * Usage:
 *   1. npm install dotenv
 *   2. cp .env.example .env  (then add your API key)
 *   3. node validate_document.mjs
 *
 * Get your free API key: https://veritier.ai/register
 * Full docs: https://veritier.ai/docs
 */

import "dotenv/config";

const API_KEY = process.env.VERITIER_API_KEY || "";
const API_URL = "https://api.veritier.ai";  // hardcoded - never sent to any other domain

if (!API_KEY) {
  console.error("❌ Error: VERITIER_API_KEY is not set.");
  console.error("  Get your free key at https://veritier.ai/register");
  process.exit(1);
}

// 📄 Sample document URL to validate 📄📄📄📄📄📄📄📄📄📄📄📄📄📄📄📄
const sampleUrl = "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf";

console.log(`📥 Input URL:\n   "${sampleUrl}"\n`);
console.log("🔍 Running deep authenticity scan...\n");

const response = await fetch(`${API_URL}/v1/validate`, {
  method: "POST",
  headers: {
    Authorization: `Bearer ${API_KEY}`,
    "Content-Type": "application/json",
  },
  body: JSON.stringify({ document_url: sampleUrl }),
});

if (!response.ok) {
  console.error(`❌ API error (${response.status}): ${await response.text()}`);
  process.exit(1);
}

const data = await response.json();
const riskScore = data.authenticity_risk_score ?? 0;
console.log(`🛡️ Authenticity Risk Score: ${riskScore}/100`);

const findings = data.findings || [];
console.log(`\n📋 Extracted ${findings.length} findings:`);
findings.forEach((finding, i) => {
  console.log(`  ${i + 1}. ${finding}`);
});

if (data.warnings?.length) {
  console.log(`\n⚠️ Warnings: ${data.warnings.join("; ")}`);
}

console.log(
  `\n⏱️ Rate limit: ${response.headers.get("RateLimit-Remaining") ?? "?"} requests remaining this minute`
);
