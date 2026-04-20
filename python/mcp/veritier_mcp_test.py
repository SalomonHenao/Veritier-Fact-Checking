#!/usr/bin/env python3
"""
Veritier MCP Integration Test (v2)
====================================
Verifies that your Veritier MCP stdio proxy is correctly configured
and can communicate with the Veritier API.

Usage:
  1. Install dependencies:
     pip install mcp httpx anyio

  2. Set your API key:
     export VERITIER_API_KEY="vt_your_api_key_here"

  3. Place this file in the same directory as veritier_mcp_proxy.py

  4. Run the test:
     python veritier_mcp_test.py

Expected output:
  ✓ Initialize: server=veritier-proxy v2.0.0
  ✓ Tools discovered: ['extract_text', 'extract_document', 'verify_text', 'verify_document']
  ✓ extract_text result:
    - The Eiffel Tower is located in Paris, France.
    - The Eiffel Tower stands 330 metres tall.
  ✓ verify_text result:
    Claim: 'The Eiffel Tower is located in Berlin.'
    Verdict: False
    Confidence: 1.0
    ...
  ✓ All checks passed! Your MCP integration is working correctly.

More info: https://veritier.ai/docs#mcp
"""

import asyncio
import json
import os
import sys
from pathlib import Path

EXPECTED_TOOLS = ["extract_text", "extract_document", "verify_text", "verify_document"]


async def test_mcp_proxy():
    api_key = os.getenv("VERITIER_API_KEY", "")

    if not api_key:
        print("✗ Error: VERITIER_API_KEY environment variable is not set.")
        print("  Get your free API key at https://veritier.ai/register")
        sys.exit(1)

    # Locate the proxy script in the same directory as this test
    proxy_path = Path(__file__).parent / "veritier_mcp_proxy.py"
    if not proxy_path.exists():
        print(f"✗ Error: Cannot find veritier_mcp_proxy.py")
        print(f"  Expected at: {proxy_path}")
        print(f"  Download it from: https://veritier.ai/veritier_mcp_proxy.py")
        sys.exit(1)

    print(f"  Proxy: {proxy_path}")
    print(f"  Key:   {'*' * 8} (length: {len(api_key)})\n")

    # Launch the standalone proxy as a subprocess
    proc = await asyncio.create_subprocess_exec(
        sys.executable, str(proxy_path),
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        env={**os.environ, "VERITIER_API_KEY": api_key},
    )

    async def send(msg: dict):
        proc.stdin.write((json.dumps(msg) + "\n").encode())
        await proc.stdin.drain()

    async def recv(timeout: int = 90) -> dict | None:
        line = await asyncio.wait_for(proc.stdout.readline(), timeout=timeout)
        return json.loads(line.decode()) if line else None

    try:
        # [1] Initialize MCP session
        await send({
            "jsonrpc": "2.0", "id": 1, "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "veritier-mcp-test", "version": "2.0"}
            }
        })
        init = await recv(timeout=15)
        server_info = init["result"]["serverInfo"]
        print(f"✓ Initialize: server={server_info['name']} v{server_info['version']}")

        # [2] Confirm initialization
        await send({"jsonrpc": "2.0", "method": "notifications/initialized"})

        # [3] Discover available tools
        await send({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
        tools = await recv(timeout=10)
        tool_names = [t["name"] for t in tools["result"]["tools"]]
        print(f"✓ Tools discovered: {tool_names}")

        missing = [t for t in EXPECTED_TOOLS if t not in tool_names]
        if missing:
            print(f"✗ Error: Missing expected tools: {missing}")
            sys.exit(1)

        # [4] Action: Extract claims
        extract_text = "The Eiffel Tower is located in Paris, France. It stands 330 metres tall."
        print(f"\n⏳ Extracting claims from: \"{extract_text}\"")

        await send({
            "jsonrpc": "2.0", "id": 3, "method": "tools/call",
            "params": {"name": "extract_text", "arguments": {"text": extract_text}}
        })
        result = await recv(timeout=60)
        content = result["result"]["content"][0]["text"]

        print(f"✓ extract_text result:\n")
        for line in content.split("\n"):
            print(f"  {line}")

        # [5] Action: Verify claims (with a known false statement)
        test_claim = "The Eiffel Tower is located in Berlin."
        print(f"\n⏳ Verifying: \"{test_claim}\"")

        await send({
            "jsonrpc": "2.0", "id": 4, "method": "tools/call",
            "params": {"name": "verify_text", "arguments": {"text": test_claim}}
        })
        result = await recv(timeout=120)
        content = result["result"]["content"][0]["text"]

        print(f"✓ verify_text result:\n")
        for line in content.split("\n"):
            print(f"  {line}")

        print("\n✓ All checks passed! Your MCP integration is working correctly.")

    except asyncio.TimeoutError:
        print("✗ Error: Timed out waiting for a response from the proxy.")
        print("  Make sure the 'mcp' package is installed: pip install mcp")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Error: {e}")
        sys.exit(1)
    finally:
        proc.stdin.close()
        await proc.wait()


if __name__ == "__main__":
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("  Veritier MCP Integration Test v2")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
    asyncio.run(test_mcp_proxy())
