# Veritier - MCP Integration (JavaScript)

Remote Streamable HTTP — no local proxy. The stdio proxy is Python-only ([`python/mcp/`](../../python/mcp/)).

📦 **API Docs:** [veritier.ai/docs](https://veritier.ai/docs#mcp)

---

## Remote HTTP

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

```bash
cd javascript
npm install
node mcp/mcp_test.mjs
```

Expected tools: `extract_text`, `extract_document`, `verify_text`, `verify_document`, `validate`, `attest_action`.

On a `vt_test_` key the script also calls `attest_action` with `mock_decision=allow` and `verify_text` with `action_id`.

MCP is always synchronous. Reconstruct a Claim Credential with REST:

`GET https://api.veritier.ai/v1/credentials/{id}`

---

## Tools

| Tool | Description |
|------|-------------|
| `extract_text` / `extract_document` | Claims only |
| `verify_text` / `verify_document` | Fact-check; optional `action_id` informational credential |
| `validate` | Authenticity scan (`url` on MCP; REST uses `document_url`) |
| `attest_action` | Fail-closed gate. HTTP 200 + `decision=block` is success |

---

## Need help?

- **Skill file:** [SKILL.md](../../SKILL.md)
- **Python stdio proxy:** [`python/mcp/`](../../python/mcp/)
