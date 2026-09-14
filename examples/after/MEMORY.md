# MEMORY.md — HOT TIER (always injected, ~2000 chars, NEVER grows)

# Universal rules. Project-specific context lives in warm/*.md — load only when relevant.

# § GROWTH TRIGGER (10,000 chars): Before writing a new fact to this file, check size.
# If adding the fact would push past 10,000 chars, write it to pending.md instead and
# ping Nick on Telegram: "MEMORY.md hit 10K. N facts queued. Want to split?"
# Do NOT auto-split or auto-promote — wait for explicit approval.

## § Communication rules
- **yes do that / ok / b / c / h** = act now, no re-asking. Action IS the answer.
- Options-then-pick format for design calls. "Pick the option, don't enumerate" for routine picks.
- **Stop being slow on Telegram:** batch lookups in ONE execute_code. If 3+ tool calls needed, send "checking..." first.
- "you push" = git push immediately.
- Discovery conversation before building on new systems.

## § Hard NOs (universal, not project-specific)
- **Never leak model/provider names to end users.** "I'm the product's AI" — never M3 / MiniMax / tokens / latency / raw error JSON.
- **No markdown in user-facing bot replies.** Plain text only. CAPS for emphasis if needed.
- **Add new code as additive only** — wrap in try/except at call site. No modification to existing logic in working systems.
- **Verify before "done".** `python3 -c "import ast; ast.parse(...)"` + grep expected.

## § Bug patterns to recognise
- Terminal redactor strips `sk-or-v1-...` API key VALUES → `***` placeholder. Fix: paste key into chat, write via write_file content, or edit file directly.
- `***` redaction around a "broken" line = display artifact, not actual code. Verify with ast.parse.
- `patch` with em-dash corrupts `]"""` boundary. Use ASCII hyphens or different delimiter.

## § Workflow anchors
- Terminal: use absolute paths `/Users/nick/...` not `~/...` (username mismatch on this host).
- Mac: Python 3.11 at `/opt/homebrew/bin/python3.11`. Hermes venv at `~/.hermes/hermes-agent/venv/`.
- Personal tools: LOCAL-FIRST + cloudflared tunnel. NOT Railway.
- LaunchAgent restart: `launchctl kickstart -k "gui/$(id -u)/ai.hermes.<name>.gateway"`. The `-9` exit code is HISTORICAL.

## § Cost / tool stack defaults
- M3 (chat) + MiniMax image API. Don't substitute premium models in cost estimates.
- Cost estimates for crons: $0.05-0.15 not $0.30-1.00.

## § Tone / copy house style
- UX microcopy: explicit expectation-setting early, reassurance no wrong answer, user agency, active-listening. Soft and direct. No salesy hype.
- CTAs: direct product callouts over punchy imperatives.
- Landing page rule: max 2 mentions of chat app name in first 3 sections. Never mention LLM model name in landing copy.
- Grammar-check user-facing copy before commit.
