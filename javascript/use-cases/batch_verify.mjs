/**
 * Batch Verification with Rate Limit Handling - Veritier Use Case (JavaScript)
 * ==============================================================================
 * Processes multiple text snippets through the Veritier verification API,
 * respecting rate-limit headers and automatically backing off when throttled.
 *
 * Essential for production workloads: auditing a CMS, scanning a document
 * library, or batch-checking user-generated content.
 *
 * Usage:
 *   node batch_verify.mjs
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

/**
 * Sleep for the given number of milliseconds.
 */
function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

// ── Batch of texts to verify ───────────────────────────────────────────
const texts = [
  "The speed of light is approximately 299,792 kilometers per second.",
  "Water boils at 100 degrees Celsius at sea level.",
  "The Amazon River is the longest river in the world.",
  "Jupiter has 79 confirmed moons as of 2024.",
  "The human body contains 206 bones.",
];

const headers = {
  Authorization: `Bearer ${API_KEY}`,
  "Content-Type": "application/json",
};

console.log(`📦 Batch: ${texts.length} texts to verify\n`);

const icons = { true: "✅", false: "❌", null: "❓" };

for (let i = 0; i < texts.length; i++) {
  const text = texts[i];
  console.log(`── [${i + 1}/${texts.length}] ──────────────────────────────────────`);
  console.log(`📝 "${text}"`);

  let response = await fetch(`${API_URL}/v1/verify`, {
    method: "POST",
    headers,
    body: JSON.stringify({ text, grounding_mode: "web" }),
  });

  // ── Handle rate limiting ────────────────────────────────────────────
  if (response.status === 429) {
    const resetSeconds = parseInt(response.headers.get("RateLimit-Reset") || "60", 10);
    console.log(`⏸ Rate limited. Waiting ${resetSeconds}s before retrying...`);
    await sleep(resetSeconds * 1000);

    // Retry once
    response = await fetch(`${API_URL}/v1/verify`, {
      method: "POST",
      headers,
      body: JSON.stringify({ text, grounding_mode: "web" }),
    });
  }

  if (response.status === 402) {
    console.log("⚠ Monthly quota exhausted. Upgrade at https://veritier.ai/dashboard");
    break;
  }

  if (!response.ok) {
    console.log(`✗ Error (${response.status}): ${await response.text()}`);
    continue;
  }

  const data = await response.json();
  const remaining = response.headers.get("RateLimit-Remaining") ?? "?";
  const reset = response.headers.get("RateLimit-Reset") ?? "?";

  for (const res of data.results || []) {
    const verdict = res.verdict;
    const icon = icons[String(verdict)] || "❓";
    console.log(`   ${icon} ${res.claim} → ${verdict} (confidence: ${res.confidence_score})`);
  }

  console.log(`   ── Remaining: ${remaining} req/min | Reset: ${reset}s\n`);

  // ── Proactive backoff if running low on rate limit ──────────────────
  const remainingNum = parseInt(remaining, 10);
  if (!isNaN(remainingNum) && remainingNum <= 1) {
    const waitSeconds = parseInt(reset, 10) + 1;
    console.log(`⏸ Rate limit nearly exhausted. Waiting ${waitSeconds}s...`);
    await sleep(waitSeconds * 1000);
  }
}

console.log("✓ Batch complete.");
