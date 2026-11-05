#!/usr/bin/env bash
# Feegate x402 demo — reproduce the live 402 flow in one command.
# Docs: https://feegate.org/quickstart
set -euo pipefail

echo "== 1) Call a paid endpoint WITHOUT payment -> expect HTTP 402 =="
curl -sS -i "https://feegate.org/api/supply/asset/case_status"
echo
echo "== 2) Parse the price from the accepts block (jq optional) =="
curl -sS "https://feegate.org/api/supply/asset/case_status" \
  | python -c "import json,sys; a=json.load(sys.stdin)['accepts'][0]; print('price USDC:', a['extra']['priceUsdc'], '| payTo:', a['payTo'], '| network:', a['network'])"

echo
echo "== 3) Pay, then retry with one of: =="
echo "   X-Payment: <base64 x402 v2 payload>        # x402 wallet (automatic)
   X-Payment-Tx: 0x<tx hash>                      # USDC transfer already on-chain
   Authorization: Bearer fg_<token>               # CNY prepaid credits (https://feegate.org/pay)"

echo
echo "== 4) Free tier needs no payment at all =="
curl -sS "https://feegate.org/free/api/search?dataset=defillama-protocols&q=uniswap&limit=3"
echo
