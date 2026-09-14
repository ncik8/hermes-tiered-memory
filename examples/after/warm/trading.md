# warm/trading.md — Trading bots (PTB)

# Load when: PTB, paper trade bot, IBKR, intraday simulator, carry delta, sector analysis, crypto bot.

## § PTB (Paper Trade Bot)
- **PTB = the yfinance simulator at `~/ibkr-bot/`** (folder stays, LaunchAgent+venv paths break if renamed).
- **LIVE runtime = `scripts/intraday_simulator.py`** (runs every 5min via launchd `com.ibkrbot.intraday`).
- State: `data/positions.json` + `data/ledger.json`.
- **DORMANT — do NOT modify for live behavior:** `bot.py` + `executor.py` + `risk.py` + `supervisor.py`.
- Trading rules: 5 concurrent positions, 10 trades/day, 2% risk/trade, 4× leverage, 5%/position.
- All Telegram messages prefixed `PTB`.
- **Patches always land in `intraday_simulator.py`, NEVER `bot.py`.**

## § Bot config (Aug 13 2026, refreshed Aug 19)
- MAX_POSITION_PCT=0.05, LEVERAGE_MULTIPLIER=4, RISK_PER_TRADE_PCT=0.02.
- 14-stock universe: NVDA, META, AAPL, GOOGL, PLTR, ARM, INTC, MU, AMAT, ON, NET, DDOG, RBLX, S.
- Live funding: $5,000 cash account after 4 weeks paper.

## § Signal thresholds (asymmetric)
- BUY = OR (BB<0.05 OR RSI<35)
- SELL = AND (BB>0.95 AND RSI>70)
- SELL stricter than BUY so bot doesn't sell on noise.

## § Carry delta (Sep 2 2026)
- **Carry delta = IBKR-specific term.** Per-position P&L difference between current price and entry-day EOD close.
- NOT a commodities "carry trade" — when explaining, lead with concrete numbers.
- 14-day window: 46 closed trades, total +$52,988. Best: Semis. Worst: Fintech/Crypto.

## § Crypto bot
- Binance Testnet, 9 pairs. Sunday 8pm HKT briefing.
- HK resident: futures/perps BLOCKED.

## § Commodities broker background
- Skip explanations of basic commodities/futures concepts.
- "Find low, not bet high". Multi-year range over short-term technicals.
- Skip value traps (Palladium/NG/Cocoa). 6-12 month hold for swing trades.
