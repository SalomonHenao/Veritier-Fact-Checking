# Veritier - MCP Integration

Connect any MCP-compatible AI agent to Veritier. Six tools: extract, verify, validate, and fail-closed `attest_action`.

📦 **API Docs:** [veritier.ai/docs](https://veritier.ai/docs#mcp) · 🔑 **Get your free key:** [veritier.ai/register](https://veritier.ai/register)

---

## Option A: Remote HTTP (recommended)

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
mcp add --transport http veritier https://api.veritier.ai/mcp/ \
  --header "Authorization: Bearer YOUR_API_KEY"
```

---

## Option B: Local stdio proxy

For clients that require a local subprocess.

```bash
pip install mcp httpx anyio
export VERITIER_API_KEY="vt_your_key_here"   # or vt_test_... for zero-quota
python veritier_mcp_test.py
```

```json
{
  "mcpServers": {
    "veritier": {
      "command": "python",
      "args": ["/absolute/path/to/mcp/veritier_mcp_proxy.py"],
      "env": {
        "VERITIER_API_KEY": "vt_your_key_here"
      }
    }
  }
}
```

Expected (test key):

```
✓ Initialize: server=veritier-proxy v2.2.0
✓ Tools discovered: ['extract_text', 'extract_document', 'verify_text', 'verify_document', 'validate', 'attest_action']
```

MCP is always synchronous. `use_webhook` has no effect. Reconstruct / JWKS / revoke are REST, not MCP tools.

---

## Tools

| Tool | Description | Quota |
|------|-------------|-------|
| `extract_text` | Extract falsifiable claims from raw text | Extractions |
| `extract_document` | Extract claims from a URL document | Extractions |
| `verify_text` | Extract + fact-check. Optional `action_id` informational credential (not fail-closed) | Verifications |
| `verify_document` | Same for a URL document | Verifications |
| `validate` | Authenticity scan (`url` parameter name on MCP) | Validations |
| `attest_action` | Fail-closed procedure lookup + signed Claim Credential | Verifications |

`attest_action` procedures: `package_exists` (npm/PyPI), `citation_exists` (CourtListener existence **and quoted passages** in the opinion), `filing_exists` (SEC EDGAR), `statute_exists` (Cornell LII / IRC), `policy_ground`. HTTP 200 with `decision=block` is success.

Zero-quota on a `vt_test_` key: `mock_claims`, `mock_verdict`, `mock_validation`, `mock_decision`.

---

## Files

| File | Description |
|------|-------------|
| [veritier_mcp_proxy.py](veritier_mcp_proxy.py) | Stdio proxy v2.2 |
| [veritier_mcp_test.py](veritier_mcp_test.py) | Integration test v2.2 |

---

## Need help?

- **Skill file:** [SKILL.md](../../SKILL.md)
- **REST samples:** [python/](../)
- **JavaScript MCP HTTP test:** [javascript/mcp/](../../javascript/mcp/)
