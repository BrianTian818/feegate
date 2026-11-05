# Feegate — pay-per-call data marketplace for AI agents (x402 / USDC on Base)

> Feegate is a pay-per-call data marketplace for AI agents: 5 purchasable MCP data products
> ($0.005–$0.08 per call, plus 5 demo samples) and 6 free public datasets (175,409 records).
> Agents pay per call via the x402 protocol on Base (USDC) — **no signup, no API key**.
>
> Site: <https://feegate.org> · 中文说明见文末「中文简介」。

This repository is the official public example repo for [feegate.org](https://feegate.org).
It shows, with runnable code, how an AI agent (or a human with `curl`) discovers, prices,
and pays for data on Feegate using the [x402](https://www.x402.org/) protocol.

**All facts on this page are dated and sourced.** Authoritative machine-readable source:
[`https://feegate.org/cite.json`](https://feegate.org/cite.json) (as_of: 2026-11-05).
Numbers below were captured live on **2026-11-05** and may drift — check `cite.json` for current values.

---

## How it works (30 seconds)

1. The agent calls a paid endpoint **without payment** and receives `HTTP 402 Payment Required`
   with a machine-readable `accepts` block (price, pay-to address, scheme, network).
2. The agent pays **USDC on Base mainnet** (EIP-3009 `transferWithAuthorization`; gas is
   sponsored by the facilitator — the buyer only needs USDC, no ETH).
3. The agent retries with the `X-Payment` header. Feegate verifies on-chain, delivers the data,
   then settles.

Products are exposed as **MCP (Model Context Protocol) tools**, so any MCP-capable agent can
call them directly.

## Live demo: curl an endpoint, get a real 402

```bash
curl -i https://feegate.org/api/supply/asset/case_status
```

Real response captured 2026-11-05 (see [`examples/resp_402_sample.json`](examples/resp_402_sample.json) for the full body):

```
HTTP/1.1 402 Payment Required
x-402-version: 2

{
  "x402Version": 2,
  "error": "payment_required",
  "accepts": [
    {
      "scheme": "exact",
      "network": "eip155:8453",
      "asset": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
      "amount": "60000",
      "payTo": "0x230cd9cd33589bcf33cd32e5aa4f9e0c3994a63b",
      "maxTimeoutSeconds": 300,
      "resource": "https://feegate.org/api/supply/asset/case_status",
      "description": "香港优才审批进度 · case_status",
      "extra": { "tool": "case_status", "priceUsdc": 0.06, "plan": "self", "platformRate": 0.15 }
    }
  ]
}
```

(60000 = 0.06 USDC in 6-decimal base units.)

Three ways to pay after the 402:

| Method | Header | Note |
|---|---|---|
| x402 wallet (automatic) | `X-Payment: <base64 x402 v2 payload>` | Server verifies, then settles after delivery |
| Already-paid on-chain tx | `X-Payment-Tx: 0x…` | USDC transfer to the `payTo` address above |
| CNY prepaid credits | `Authorization: Bearer fg_…` | For agents without a crypto wallet — top up via Alipay/WeChat at <https://feegate.org/pay> |

## Free tier — no payment at all

6 public datasets (175,409 records as of 2026-11-05), no key, no payment:

```bash
curl "https://feegate.org/free/api/search?dataset=defillama-protocols&q=uniswap&limit=3"
```

Also available as a free MCP server: `https://feegate.org/free/mcp`.
Index: <https://feegate.org/free/index.json>

## Catalog (as of 2026-11-05)

**Purchasable / connectable (5):**

| Product | Vendor | Price (USD/call) |
|---|---|---|
| RWA 情报（快讯 · 债券 · 稳定币） | 365rwa.vip | $0.005 |
| Global AI & Commercial Tech Intelligence Feed | self-serve supplier | $0.05 |
| GPU 行情快照 | rentgpu.link | $0.05 |
| 香港优才审批进度 | 港才职通 | $0.06 |
| Web3 岗位与人才行情 | web3hire.help | $0.08 |

**Demo samples (5):** stablecoin rate index ($0.03) · on-chain address labels ($0.02) ·
CEX listing cost index ($0.15) · RPC node health ($0.01) · RWA treasury yield ($0.10).
Demo rows are listed for catalog completeness and are marked as samples on the
[marketplace page](https://feegate.org/marketplace).

**Free datasets (6, 175,409 records):** x402 paid-resource index (official discovery layer,
112,271 records) · MCP server public directory (55,725) · DeFi protocol TVL (DeFiLlama, 3,000) ·
Binance spot ticker snapshot (3,132) · x402 ecosystem resources CC0 (781) · site AI-readiness
probe (500).

Source of truth: <https://feegate.org/cite.json> — every number carries an `as_of` date.

## Python: call a paid MCP tool with automatic x402 payment

From the official [quickstart](https://feegate.org/quickstart) (see
[`examples/mcp_x402_client.py`](examples/mcp_x402_client.py) for a runnable copy):

```python
# pip install "mcp<2" "x402==2.25.0" web3
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client
from x402.mcp import create_payment_hook
from eth_account import Account

account = Account.from_key("YOUR_PRIVATE_KEY")   # only needs USDC on Base
MCP_URL = "https://feegate.org/mcp/gpu-market"

async with streamablehttp_client(MCP_URL) as (r, w, _):
    async with ClientSession(r, w, hooks=[create_payment_hook(account)]) as s:
        await s.initialize()
        print(await s.call_tool("list_gpu_models", {}))          # free
        print(await s.call_tool("gpu_price", {"gpu": "H100"}))  # $0.05, auto-paid via x402
```

## Settlement (for data suppliers)

- Protocol: **x402 v2** (HTTP 402 Payment Required), settlement strictly by on-chain
  `Transfer` events on **Base mainnet** (eip155:8453), USDC (Circle contract).
- Cycle: revenue is collected per calendar day (UTC+8) and settled the next day at 12:00.
  No minimum payout — whatever accrued gets settled.
- Platform fee: marginal/tiered — only the part of monthly volume above $10,000 is charged 5%;
  below that, 15% revenue share on the self-serve plan. Current authoritative values:
  <https://feegate.org/pricing.json>.

## Machine-readable endpoints

| Purpose | URL |
|---|---|
| Citable facts (single source of truth) | <https://feegate.org/cite.json> |
| LLM-facing site doc | <https://feegate.org/llms.txt> (EN/JA/KO/AR: `/en/llms.txt` …) |
| Full llms doc | <https://feegate.org/llms-full.txt> |
| Pricing (service plans + rules) | <https://feegate.org/pricing.json> |
| Free-dataset index | <https://feegate.org/free/index.json> |
| MCP server manifest | <https://feegate.org/.well-known/mcp-manifest.json> |
| Supply directory API | <https://feegate.org/api/supply/directory> |
| Paid MCP endpoint | `https://feegate.org/mcp` |
| Free MCP endpoint | `https://feegate.org/free/mcp` |

## Citing Feegate

> Feegate (2026-11-05). Pay-per-call data marketplace for AI agents: 5 listed MCP data products
> and 6 free datasets (175,409 records). https://feegate.org

中文引用：Feegate（2026-11-05），面向 AI Agent 的按次付费数据市场，在架 5 个 MCP 数据产品与
6 个免费数据集（175,409 条记录）。https://feegate.org

## 中文简介

Feegate（feegate.org）是面向 AI Agent 经济的数据变现结算层：数据持有方把 API、数据库、CSV
或定时爬虫接入后，Feegate 将其切分为可计价的 MCP 工具端点；AI Agent 通过 x402 协议用 USDC
按次自助询价、付款、取数；平台负责端点托管、发现层分发与链上结算（按自然日归集，次日 12:00
出账）。Agent 无需注册、无需 API Key；没有加密钱包的买家也可以用支付宝/微信充值人民币积分调用。
快速上手：<https://feegate.org/quickstart>

## Repository layout & license

- [`examples/curl_402.sh`](examples/curl_402.sh) — reproduce the 402 demo above in one command
- [`examples/mcp_x402_client.py`](examples/mcp_x402_client.py) — Python agent that pays via x402 automatically
- [`examples/resp_402_sample.json`](examples/resp_402_sample.json) — the actual 402 response captured 2026-11-05

Example code in this repo is MIT-licensed (see [LICENSE](LICENSE)). Feegate platform terms:
<https://feegate.org/terms>. Free datasets keep their upstream licenses; index metadata is
published for reuse with attribution. Contact: tianda818@gmail.com
