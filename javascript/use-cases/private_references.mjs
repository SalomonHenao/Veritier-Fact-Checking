/**
 * Private Reference Grounding - Veritier Use Case (JavaScript)
 * ==============================================================
 * Verify claims against YOUR OWN documents instead of the open web.
 * Essential for enterprise use cases: validate content against internal
 * policies, research papers, or proprietary data.
 *
 * Usage:
 *   node private_references.mjs
 *
 * Get your free API key: https://veritier.ai/register
 */

import "dotenv/config";

const API_KEY = process.env.VERITIER_API_KEY || "";
const API_URL = process.env.VERITIER_API_URL || "https://api.veritier.ai";

if (!API_KEY) {
  console.error("✗ Error: VERITIER_API_KEY is not set.");
  console.error("  Get your free key at https://veritier.ai/register");
  process.exit(1);
}

// ── Your private reference document ────────────────────────────────────
const companyPolicy = `
Acme Corp Employee Handbook (2026 Edition)
==========================================
- All employees receive 20 days of paid vacation per year.
- Remote work is permitted up to 3 days per week.
- The standard work week is 37.5 hours.
- Parental leave is 16 weeks for all parents.
- Annual performance reviews occur in March.
`;

// ── Text containing claims to verify against the reference ─────────────
const textToVerify =
  "At Acme Corp, employees get 25 days of vacation per year. " +
  "Remote work is allowed 3 days a week. " +
  "Performance reviews happen every quarter.";

console.log("📄 Reference document: Acme Corp Employee Handbook");
console.log(`\n📝 Claims to verify:\n   "${textToVerify}"\n`);
console.log("⏳ Verifying against private reference...\n");

const response = await fetch(`${API_URL}/v1/verify`, {
  method: "POST",
  headers: {
    Authorization: `Bearer ${API_KEY}`,
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    text: textToVerify,
    grounding_mode: "references",
    grounding_references: [
      { type: "text", content: companyPolicy },
      // You can also add URL references:
      // { type: "url", content: "https://your-internal-docs.com/handbook" },
    ],
  }),
});

if (!response.ok) {
  console.error(`✗ API error (${response.status}): ${await response.text()}`);
  process.exit(1);
}

const data = await response.json();
const results = data.results || [];

const icons = { true: "✅", false: "❌", null: "❓" };

console.log(`✓ Verified ${results.length} claim(s) against your reference:\n`);
for (const res of results) {
  const verdict = res.verdict;
  const icon = icons[String(verdict)] || "❓";

  console.log(`  ${icon} Claim: '${res.claim}'`);
  console.log(`     Verdict:      ${verdict}`);
  console.log(`     Confidence:   ${res.confidence_score}`);
  console.log(`     Explanation:  ${res.explanation}`);
  if (res.source_label) {
    console.log(`     Source label: ${res.source_label}`);
  }
  console.log();
}
