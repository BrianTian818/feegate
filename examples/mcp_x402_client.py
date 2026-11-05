#!/usr/bin/env python3
"""Feegate x402 MCP client — call a paid MCP tool with automatic payment.

From the official quickstart: https://feegate.org/quickstart
Install:  pip install "mcp<2" "x402==2.25.0" web3
Wallet:   a private key holding USDC on Base mainnet. Gas is sponsored by
          the facilitator, so no ETH is needed.

Usage:
  export FG_PRIVATE_KEY=0x...
  python mcp_x402_client.py
"""
import asyncio
import os
import sys

from eth_account import Account
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client
from x402.mcp import create_payment_hook

MCP_URL = "https://api.feegate.org/mcp/gpu-market"


async def main() -> None:
    key = os.environ.get("FG_PRIVATE_KEY")
    if not key:
        sys.exit("set FG_PRIVATE_KEY to a Base-mainnet USDC key first")
    account = Account.from_key(key)

    async with streamablehttp_client(MCP_URL) as (r, w, _):
        async with ClientSession(r, w, hooks=[create_payment_hook(account)]) as s:
            await s.initialize()
            # free tools first — discovery costs nothing
            print(await s.call_tool("list_gpu_models", {}))
            # paid tool: $0.05/call, auto-negotiated + auto-paid via x402
            print(await s.call_tool("gpu_price", {"gpu": "H100"}))


if __name__ == "__main__":
    asyncio.run(main())
