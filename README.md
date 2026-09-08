# ✅ Veritier - AI Fact-Checking API Examples

**Stop AI Hallucinations. Verify Claims in Real Time.**

Veritier is an **AI fact-checking API** that extracts falsifiable claims from any text or document and verifies each against live web evidence - or your own private references. Deterministic boolean verdicts, confidence scores, and source URLs. Built for developers, media platforms, and autonomous AI agents.

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://python.org)
[![Node.js 18+](https://img.shields.io/badge/Node.js-18%2B-brightgreen.svg)](https://nodejs.org)
[![Veritier API](https://img.shields.io/badge/API-veritier.ai-purple.svg)](https://veritier.ai)

🌐 [Website](https://veritier.ai) · 📖 [Documentation](https://veritier.ai/docs) · 🔑 [Get Free API Key](https://veritier.ai/register) · 📊 [Dashboard](https://veritier.ai/dashboard)

---

## ⚡ 30-Second Quickstart

Get your free API key at [veritier.ai/register](https://veritier.ai/register), then:

<table>
<tr>
<th>Python</th>
<th>JavaScript</th>
</tr>
<tr>
<td>

```python
import httpx

response = httpx.post(
    "https://api.veritier.ai/v1/verify",
    headers={
        "Authorization": "Bearer YOUR_API_KEY",
        "Content-Type": "application/json",
    },
    json={"text": "The Eiffel Tower is in Berlin."},
)

for claim in response.json()["results"]:
    print(f"{claim['verdict']}: {claim['claim']}")
    # False: The Eiffel Tower is in Berlin.
```

</td>
<td>

```javascript
const res = await fetch("https://api.veritier.ai/v1/verify", {
  method: "POST",
  headers: {
    Authorization: "Bearer YOUR_API_KEY",
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    text: "The Eiffel Tower is in Berlin.",
  }),
});

const { results } = await res.json();
results.forEach((c) => console.log(`${c.verdict}: ${c.claim}`));
// false: The Eiffel Tower is in Berlin.
```

</td>
</tr>
</table>

---

## 📁 What's Inside

This repository contains ready-to-run examples in **Python** and **JavaScript**, plus MCP integration scripts for AI agents. Agent-oriented copy lives in [`SKILL.md`](SKILL.md) (same content as `https://veritier.ai/skill.md`).

### Python Examples → [`python/`](python/)

| Example | Description |
|---------|-------------|
| [extract_text.py](python/quickstart/extract_text.py) | Extract claims from text without verifying |
| [verify_text.py](python/quickstart/verify_text.py) | Verify claims against live web evidence |
| [validate_document.py](python/quickstart/validate_document.py) | Authenticity scan (`document_url` / `extracted_text`) |
| [attest_action.py](python/quickstart/attest_action.py) | Fail-closed action attestation |
| [reconstruct_credential.py](python/quickstart/reconstruct_credential.py) | Public reconstruct, JWKS, optional revoke |
| [test_integration.py](python/quickstart/test_integration.py) | Zero-quota extract / verify / validate / attest / credentials |
| [verify_article_url.py](python/use-cases/verify_article_url.py) | Fact-check all claims from a web page |
| [hallucination_audit.py](python/use-cases/hallucination_audit.py) | Catch LLM hallucinations before they reach users |
| [disinformation_shield.py](python/use-cases/disinformation_shield.py) | Screen content for false claims - truth firewall |
| [private_references.py](python/use-cases/private_references.py) | Verify against your own documents (no web search) |
| [batch_verify.py](python/use-cases/batch_verify.py) | Batch-process texts with rate-limit handling |
| [gate_tool_call.py](python/use-cases/gate_tool_call.py) | Attest, then only proceed on `decision=allow` |
| [informational_credential.py](python/use-cases/informational_credential.py) | Optional `action_id` on verify (not fail-closed) |
| [webhook_receiver.py](python/webhooks/webhook_receiver.py) | HMAC-signed webhooks + `Idempotency-Key` |

### JavaScript Examples → [`javascript/`](javascript/)

| Example | Description |
|---------|-------------|
| [extract_text.mjs](javascript/quickstart/extract_text.mjs) | Extract claims from text without verifying |
| [verify_text.mjs](javascript/quickstart/verify_text.mjs) | Verify claims against live web evidence |
| [validate_document.mjs](javascript/quickstart/validate_document.mjs) | Authenticity scan (`document_url` / `extracted_text`) |
| [attest_action.mjs](javascript/quickstart/attest_action.mjs) | Fail-closed action attestation |
| [reconstruct_credential.mjs](javascript/quickstart/reconstruct_credential.mjs) | Public reconstruct, JWKS, optional revoke |
| [test_integration.mjs](javascript/quickstart/test_integration.mjs) | Zero-quota extract / verify / validate / attest / credentials |
| [verify_article_url.mjs](javascript/use-cases/verify_article_url.mjs) | Fact-check all claims from a web page |
| [hallucination_audit.mjs](javascript/use-cases/hallucination_audit.mjs) | Catch LLM hallucinations before they reach users |
| [disinformation_shield.mjs](javascript/use-cases/disinformation_shield.mjs) | Screen content for false claims - truth firewall |
| [private_references.mjs](javascript/use-cases/private_references.mjs) | Verify against your own documents (no web search) |
| [batch_verify.mjs](javascript/use-cases/batch_verify.mjs) | Batch-process texts with rate-limit handling |
| [gate_tool_call.mjs](javascript/use-cases/gate_tool_call.mjs) | Attest, then only proceed on `decision=allow` |
| [informational_credential.mjs](javascript/use-cases/informational_credential.mjs) | Optional `action_id` on verify (not fail-closed) |
| [webhook_receiver.mjs](javascript/webhooks/webhook_receiver.mjs) | HMAC-signed webhooks + `Idempotency-Key` |

### MCP Integration - Python → [`python/mcp/`](python/mcp/)

| File | Description |
|------|-------------|
| [veritier_mcp_proxy.py](python/mcp/veritier_mcp_proxy.py) | Stdio proxy v2.2 (includes `attest_action`) |
| [veritier_mcp_test.py](python/mcp/veritier_mcp_test.py) | Integration test - auto-detects test keys for zero-quota runs |

### MCP Integration - JavaScript → [`javascript/mcp/`](javascript/mcp/)

| File | Description |
|------|-------------|
| [mcp_test.mjs](javascript/mcp/mcp_test.mjs) | Streamable HTTP test (extract / verify / validate / attest_action) |

---

## 🛠 Available API Tools

| Tool | Endpoint | Description | Quota |
|------|----------|-------------|-------|
| **extract_text** | `POST /v1/extract` | Extract falsifiable claims from raw text | Extractions |
| **extract_document** | `POST /v1/extract` | Extract claims from a URL document | Extractions |
| **verify_text** | `POST /v1/verify` | Extract + fact-check. Optional `action_id` informational credential | Verifications |
| **verify_document** | `POST /v1/verify` | Extract + fact-check from a URL document | Verifications |
| **validate** | `POST /v1/validate` | Authenticity scan (`document_url` / `document_base64` / `extracted_text`) | Validations |
| **attest_action** | `POST /v1/attest_action` | Fail-closed procedure lookup + signed Claim Credential. HTTP 200 with `decision=block` is success | Verifications |
| **reconstruct** | `GET /v1/credentials/{id}` | Public workpaper (no API key, 400-day TTL) | none |
| **jwks** | `GET /v1/credentials/.well-known/jwk` | Current and previous Ed25519 public keys | none |
| **revoke** | `POST /v1/credentials/{id}/revoke` | Issuer revoke; GET stays 200 with `revoked: true` | none |

### Verification Response

```
Claim: 'The Eiffel Tower is located in Berlin.'
  Verdict: false
  Confidence: 1.0
  Explanation: The Eiffel Tower is located in Paris, France, not Berlin.
  Sources: https://en.wikipedia.org/wiki/Eiffel_Tower
```

| Verdict | Meaning |
|---------|---------|
| `true` | Supported by evidence |
| `false` | Contradicted by evidence |
| `null` | Insufficient evidence to determine |

`attest_action` returns `decision`: `allow` | `block` | `escalate`. Treat HTTP 200 with `decision=block` as success. Optional `action_id` on `/v1/verify` is informational only — it does not fail-close.

---

## 🤖 MCP Integration (AI Agents)

Connect any MCP-compatible AI agent to Veritier with zero local setup:

```json
{
  "mcpServers": {
    "veritier": {
      "type": "http",
      "url": "https://api.veritier.ai/mcp/",
      "headers": {
        "Authorization": "Bearer YOUR_API_KEY"
      }
    }
  }
}
```

For clients that need a local subprocess, see the [stdio proxy](python/mcp/) in the `python/mcp/` folder. MCP tools: `extract_text`, `extract_document`, `verify_text`, `verify_document`, `validate`, `attest_action`. Reconstruct, JWKS, and revoke are REST only.

## 🔑 Getting Started

1. **Register** at [veritier.ai/register](https://veritier.ai/register) - free, no credit card
2. **Confirm** the verification email
3. **Go to** [veritier.ai/dashboard](https://veritier.ai/dashboard)
4. **Click** "Mint New Key" - copy the `vt_` key immediately (shown once)
5. **Set** `VERITIER_API_KEY` in your environment:
   ```bash
   # Copy the template
   cp .env.example .env
   # Add your key
   ```
6. **Run** any example:
   ```bash
   # Python
   cd python && pip install -r requirements.txt
   python quickstart/verify_text.py

   # JavaScript
   cd javascript && npm install
   node quickstart/verify_text.mjs
   ```

---

## 💰 Plans

| Tier | Price | Req/min | Verifications/mo | Extractions/mo | Validations/mo |
|------|-------|:---:|:---:|:---:|:---:|
| **Free** | $0 | 10 | 25 | 100 | 5 |
| **Pro** | $19.99/mo | 60 | 500 | 2,000 | 100 |
| **Business** | $249.99/mo | 300 | 10,000 | 50,000 | 2,000 |

Upgrade anytime at [veritier.ai/dashboard](https://veritier.ai/dashboard) - takes effect immediately.

---

## Integration Testing (Zero-Quota)

Build and validate your integration **without consuming any quota**. Test mode returns deterministic mock data through the full auth pipeline - no LLM is ever called.

### 1. Create a test key

Sign in at [veritier.ai/dashboard](https://veritier.ai/dashboard) → **API Keys → Test** → **Mint New Key**.  
Test keys are prefixed `vt_test_` and are completely isolated from your production quota.

### 2. Run the zero-quota integration test

```bash
export VERITIER_TEST_KEY="vt_test_your_key_here"

# Python
python python/quickstart/test_integration.py

# JavaScript
node javascript/quickstart/test_integration.mjs
```

```
OK [1/10] API connectivity confirmed
OK [2/10] Extract: 3 mock claims returned
...
OK [8/10] Attest: mock_decision=allow
OK [9/10] Public reconstruct + JWKS
OK [10/10] Issuer revoke
All integration checks passed. Zero quota was consumed.
```

### 3. Mock parameters

| Parameter | Endpoint | Description |
|-----------|----------|-------------|
| `mock_claims` | `POST /v1/extract` | Integer 0–1000. Returns that many mock claims. No LLM, no extraction quota. |
| `mock_verdict` | `POST /v1/verify` | Boolean. `true` = all verdicts true, `false` = all false. No LLM, no verification quota. |
| `mock_validation` | `POST /v1/validate` | Boolean. `true` = authentic, `false` = fraudulent. REST body uses `document_url` / `extracted_text`. |
| `mock_decision` | `POST /v1/attest_action` | `allow` or `block`. Signed credential, no lookup. Test keys auto-activate allow when omitted. |

**Rules:**
- Mock fields are **only accepted with test keys** - production keys return `400 Bad Request`. The Engine playground may send `mock_decision` on a dashboard JWT; this samples repo uses API keys.
- Test responses include `"is_test": true` in the body and `X-Veritier-Test-Mode: true` header.
- **RPM rate limiting applies in test mode.** Monthly quota is not consumed, but requests-per-minute limits are still enforced - production rate behaviour is fully replicated.
- With a test key, omitting mock params **auto-activates** test mode with safe defaults (1 claim / true verdict / authentic validation / allow attest).
- Test requests are logged and visible in the Test view in your dashboard.
- Input validation (injection scanning, field limits) runs normally. Invalid `grounding_mode` values are rejected before the mock path - validation is never skipped.

---

## 🔒 Security

- API keys are prefixed `vt_` and SHA-256 hashed at rest - Veritier never stores the raw value
- Keys can be revoked at any time from the dashboard
- Only send your key to `https://api.veritier.ai`
- All inputs are screened by a content firewall before reaching the verification engine
- Webhook deliveries are signed with HMAC-SHA256 (`X-Veritier-Signature` over the **raw body**). Retries reuse `Idempotency-Key` / `X-Veritier-Idempotency-Key`. HMAC does not cover extra headers.
- Claim Credentials are public workpapers (`/c/:id`). They do not include account id or email. The issuer may revoke; GET stays 200 with `revoked: true`. They are not a judicial finding.

---

## 🏗 Use Cases

### Catch LLM Hallucinations
Feed AI-generated text through Veritier before publishing. The [hallucination_audit](python/use-cases/hallucination_audit.py) example shows how to flag false claims automatically.

### Truth Firewall (Stop Disinformation)
Screen user-generated content, news snippets, or social media posts for false claims. Use the [disinformation_shield](python/use-cases/disinformation_shield.py) to catch misinformation before it spreads.

### Fact-Check Articles
Pass any URL to the document verification endpoint. The [verify_article_url](python/use-cases/verify_article_url.py) example verifies every claim in a web page.

### Verify Against Internal Documents
Use `grounding_mode: "references"` to check claims against your own private data - no web search involved. See the [private_references](python/use-cases/private_references.py) example.

### Gate a tool call
Call `POST /v1/attest_action` before the agent runs a command. Only proceed on `decision=allow`. See [gate_tool_call](python/use-cases/gate_tool_call.py). HTTP 200 with `decision=block` means refuse the action.

### Informational workpaper on verify
Pass `action_id` on `POST /v1/verify` to mint a Claim Credential without fail-closing. See [informational_credential](python/use-cases/informational_credential.py).

### Content Moderation at Scale
Process thousands of texts with automatic rate-limit handling. The [batch_verify](python/use-cases/batch_verify.py) example handles throttling and backoff for you.

---

## 📄 License

The code in this repository is provided under the [MIT License](LICENSE).  
The Veritier API is a commercial service - see [veritier.ai](https://veritier.ai) for terms.
