# Veritier - JavaScript Fact-Checking Examples

Verify claims, scan documents, and fail-close tool calls with the **Veritier API**. Node.js 18+ native `fetch`.

📦 **API Docs:** [veritier.ai/docs](https://veritier.ai/docs) · 🔑 **Get your free key:** [veritier.ai/register](https://veritier.ai/register)

---

## Prerequisites

- **Node.js 18+**
- A free Veritier API key ([register here](https://veritier.ai/register))

```bash
npm install
cp ../.env.example .env
# Edit .env: VERITIER_API_KEY, optionally VERITIER_TEST_KEY
```

---

## Examples

### Quickstart

| Script | Description | Run |
|--------|-------------|-----|
| [extract_text.mjs](quickstart/extract_text.mjs) | Extract falsifiable claims (no verification) | `node quickstart/extract_text.mjs` |
| [verify_text.mjs](quickstart/verify_text.mjs) | Fact-check claims against live web evidence | `node quickstart/verify_text.mjs` |
| [validate_document.mjs](quickstart/validate_document.mjs) | Authenticity scan (`document_url` / `extracted_text`) | `node quickstart/validate_document.mjs` |
| [attest_action.mjs](quickstart/attest_action.mjs) | Fail-closed `POST /v1/attest_action` | `node quickstart/attest_action.mjs` |
| [reconstruct_credential.mjs](quickstart/reconstruct_credential.mjs) | Public GET + JWKS + optional revoke | `node quickstart/reconstruct_credential.mjs crc_...` |
| [test_integration.mjs](quickstart/test_integration.mjs) | Zero-quota extract/verify/validate/attest/credentials | `node quickstart/test_integration.mjs` |

### Use cases

| Script | Description | Run |
|--------|-------------|-----|
| [verify_article_url.mjs](use-cases/verify_article_url.mjs) | Verify claims from a web page URL | `node use-cases/verify_article_url.mjs <URL>` |
| [hallucination_audit.mjs](use-cases/hallucination_audit.mjs) | Catch LLM hallucinations before they reach users | `node use-cases/hallucination_audit.mjs` |
| [disinformation_shield.mjs](use-cases/disinformation_shield.mjs) | Screen user content for false claims | `node use-cases/disinformation_shield.mjs` |
| [private_references.mjs](use-cases/private_references.mjs) | Verify against your own documents | `node use-cases/private_references.mjs` |
| [batch_verify.mjs](use-cases/batch_verify.mjs) | Batch-process with rate-limit handling | `node use-cases/batch_verify.mjs` |
| [gate_tool_call.mjs](use-cases/gate_tool_call.mjs) | Attest, then only proceed on `decision=allow` | `node use-cases/gate_tool_call.mjs` |
| [informational_credential.mjs](use-cases/informational_credential.mjs) | `action_id` on verify (not fail-closed) | `node use-cases/informational_credential.mjs` |

### Webhooks

| Script | Description | Run |
|--------|-------------|-----|
| [webhook_receiver.mjs](webhooks/webhook_receiver.mjs) | HMAC-SHA256 + `Idempotency-Key` (including `type: attestation`) | `node webhooks/webhook_receiver.mjs` |

### MCP

| Script | Description | Run |
|--------|-------------|-----|
| [mcp_test.mjs](mcp/mcp_test.mjs) | Streamable HTTP MCP test (includes `attest_action`) | `node mcp/mcp_test.mjs` |

---

## API endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v1/extract` | POST | Extract claims without verifying |
| `/v1/verify` | POST | Extract + verify. Optional `action_id` mints an informational credential |
| `/v1/validate` | POST | Authenticity scan (`document_url`, `document_base64`, or `extracted_text`) |
| `/v1/attest_action` | POST | Fail-closed procedure lookup. HTTP 200 + `decision=block` is success |
| `/v1/credentials/{id}` | GET | Reconstruct a Claim Credential (no auth, 400-day TTL) |
| `/v1/credentials/.well-known/jwk` | GET | Ed25519 public keys |
| `/v1/credentials/{id}/revoke` | POST | Issuer revoke; public GET stays 200 with `revoked: true` |

---

## Need help?

- **Full docs:** [veritier.ai/docs](https://veritier.ai/docs)
- **Python MCP stdio proxy:** [`python/mcp/`](../python/mcp/)
- **Python examples:** [`python/`](../python/)
