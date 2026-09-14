# Example: bloated MEMORY.md (before split)

> This is a synthetic example showing what a typical Hermes user's MEMORY.md
> looks like before tiering. Real names, projects, and tokens have been replaced
> with generic placeholders. ~50K chars, mostly project context that's only
> relevant when actively working on that project.

---

**Project A actual user state (Jun 19 2026, post-backfill):** Earlier memory said "5/7 ghost rate, 1 power user" — that was WRONG/stale. Actual: 6 profiles in DB, 2 with user_cvs rows, 0 ghost users (both CV uploaders have profiles). One power user (b0523320) is **pro_plus** tier with cv_count=11 (11 tailoring sessions all upserted into single row). Investor headline: **"2 CV uploaders, 6 accounts, 2 paid"**. Migration 006 = backfill ghost profiles for safety, idempotent ON CONFLICT DO NOTHING. user_cvs.user_id FK → auth.users(id) ON DELETE CASCADE enforces real signup. /cv/upload redirects to login (no anon), /cv/parse returns 401 if no user_id. **Stripe webhook bug FIXED (758c502):** profiles.update → profiles.upsert so users whose profile row was never created still get tier set on payment. sign_up in services/auth.py FIXED: now logs (not swallows) profile insert errors, added missing .execute(). **Smoke test:** scripts/test_cv_persistence.py --write verifies schema + reads+writes 3 previously-broken columns (additional_info, gap_answers, updated_at). **Repo is /Users/nick/project-a/**. **Supabase project = `aaaabbbbccccddddeeee.supabase.co`**. **Other project Supabase = `ffffgggghhhhiiiijjjj.supabase.co`. DIFFERENT PROJECTS — never confuse them when running SQL via Management API.** Verified users: 8 (as of Jun 22 2026). No `public.users` table (uses `auth.users` + `public.profiles` like Supabase Auth pattern).

§

Project A positioning + feature gap: **"Your designer CV is the reason you have no interviews"** — ATS doesn't render design, parses text and matches keywords. Contrarian hook: 50 designer CV templates (Canva/Behance) tested against real ATS = 0 passed cleanly (columns break parser, icons get skipped, graphics hide keywords). Feature gap: no from-scratch CV builder yet. Current free flow: upload-then-tailor only. YouTube Short up needs title fix + hashtag drop. Cross-post to @ChannelB (11 subs) being tested.

§

Loading state for slow AI operations — Nick's UX rule: Flask/AI app with 5-15s wait → users see static "Give me a moment..." and conclude app frozen. Refresh, lose session, file "your app is broken" bug. **Fix: spinner + multi-step progress UI that visibly rotates and lights up which step is active.** User words ("Extracting your CV with AI") not technical ("Calling LLM"). Pattern: .spinner (CSS border-top-color rotation) + .finish-steps with .step.active (full opacity) and .step.done (green ✓). 300ms intentional delays between step transitions. Hide spinner (not just steps) on completion. Full impl in local-voice-prototype skill.

§

Project A deployed: Repo github.com/username/project-a-voice. Deploy: build.project-a.com (CNAME → Railway). 7-question voice interview, MediaRecorder + faster-whisper STT, M3 for CV extraction, editable preview, /print/<sid> for browser-PDF. TTS optional — 7 main questions pre-warmed by scripts/warmup_audio.py.

§

Project B key context (TON + conference use case): TON Foundation grant angle — TON wallet + TON-holder 30% discount. Use case: Nick at crypto conferences with 500+ Telegram contacts, no context/provenance for any of them. Token2049 SG (September) = anchor launch event. Free=10 cards, Pro=$9.99/mo or $99/yr, Team=$49/mo (pricing in SKETCH.md).

§

Project A content pillar: 4-stage buyer journey. (1) standard CV = problem-aware hook, contrarian "designer CV is reason you have no interviews" lives here. (2) ATS optimised = solution-aware how-to. (3) Tailored CV = solution-aware pitch (Project A fastest path generic → tailored). (4) Interviews = product-aware proof, founder story + testimonials inline. Build in this exact order — skip stages and readers bounce. Internal linking: Stage 1 → 2 → 3 → 4 in sequence. JSON-LD FAQ on each.

§

Grammar check user-facing copy before push: Pushed testimonial with duplicate word ("it it uses") — trusted user's verbatim quote without reading. Nick flagged post-deploy. Rule: before committing testimonial/quote/copy to public surface, read each quote aloud end-to-end looking for: duplicate words, missing commas at clause boundaries, dropped apostrophes, sentence fragments.

§

Project B live (Jun 2026): web at https://project-b-production.up.railway.app, bot @ProjectBBot on Railway, Supabase (Pro), 7 tables + RLS, M3 vision OCR + M3 function-calling AI (6 tools). Repo: github.com/username/project-b (private). Schema includes `name, handle, company, title, email, phone, notes, source, search_vector, website`. **Bug to remember:** original system prompt leaked M3 model name + Supabase errors to users — replaced Jun 17. Token2049 SG Sept = anchor event. Tester model = 2-3 humans with full access.

§

Hermes Agent provider routing patterns — skill `hermes-agent-provider-routing` (devops category, June 13 2026). Covers three subsystems sharing one routing layer: (1) auxiliary tasks via `auxiliary.{task}.provider/model` config, (2) subagent dispatch via `delegate_task` model override, (3) main conversation via `model.default`. Config memoised on `.env` mtime — editing config.yaml alone does NOT reload; restart gateway.

§

**"Done" claim verification (Jun-Jul 2026).** Nick frustrated 4+ times because agent claimed patches/saves landed when they hadn't. Recurring failure modes: (1) `read_file` via `python3 -c "..."` heredoc returns empty without raising; (2) `patch` with em-dash corrupts `]"""` boundary; (3) `patch` succeeds but doesn't verify Python syntax; (4) terminal heredoc shell quoting; (5) shell redactor mangles env-var assignments (`API_KEY=***`). **Rule:** before "done"/"fixed", verify: `python3 -c "import ast; ast.parse(open('file.py').read())"` + `grep <expected> <file>`.

§

Free tier must extract value in return (Jun 19 2026, Nick's principle). Free = no giveaway. Always include a clear exchange (email signup, CV upload, etc.). Before any new free feature, ask: what's the exchange + what data do we capture?

§

**Trading bot config (Aug 13 2026):** $5,000 live funding, 4× leverage, 20% per-position cap = $1K/trade. Risk 2%/trade. 14-stock universe: NVDA, META, AAPL, GOOGL, PLTR, ARM, INTC, MU, AMAT, ON, NET, DDOG, RBLX, S. **Signal thresholds:** BUY = OR (BB<0.05 OR RSI<35); SELL = AND (BB>0.95 AND RSI>70). Nick explicit: SELL stricter than BUY so bot doesn't sell on noise. Paper-trading-first is HARD BOUNDARY — 4-week validation, then live.

§

**Carry delta = IBKR-specific term (Sep 2 2026).** Per-position P&L difference between (current price) and (entry-day EOD close). Tells you whether holding overnight paid off. NOT a commodities "carry trade" (contango/backwardation). Daily report shows: per-stock `EOD-close alt` vs current + single trend line. Persistence files (30-day rolling): `data/carry_delta_history.json`. **14-day window result (Aug 19 → Sep 2):** 46 closed trades, total +$52,988. Best sector: Semis. Worst: Fintech/Crypto.

§

Nick's work pattern + family schedule anchors (Jul 19 2026). Nick works nights till 6:30am HKT, sleeps 1:30pm-9:30pm. NOT free 9-5 — evening blocks after 7pm are his only real time with his 11-year-old son. Wife handles mornings. Dinner anchor = 7pm. Son's summer 2026 routine: piano 10-11, free/active 11-12 (drawing OR chess — son picks), lunch 12-1, summer school work 1-2, computer games 2-4, outside play 4-6, shower 6-6:45, quiet 6:45-7, dinner 7-8, friend's house 8-9:30, TV 9:30-10:30, bed 10:30.

§

Nick calls me Henry (not Hermes). The main `~/.hermes` IS Henry. All other `~/.hermes-<name>/` are sub-agents. **Naming convention:** name systems after himself (e.g. "NICK COMMAND BASE"), NOT technical terms.

§

**Communication style:** short, direct, no flowery language. Options then picks. No over-asking — default and act, or just do it. Prefers voice replies but types when doing code/projects. "you push" = git push immediately. **"yes do that" / "ok" pattern = act now, no re-asking** (June 10 2026).

§

**Stop being slow on Telegram:** each tool call keeps typing up; 5-10 calls = stuck bot. Batch lookups in ONE `execute_code`. Trust first answer. If 3+ tool calls needed, send "checking..." first.

§

**Don't leak infrastructure to end users** (Jun 17 2026). User-facing AI system prompts must NEVER mention model names, versions, or internals. On error: "I had trouble, try again" — NOT "the M3 model returned 400".

§

**Add new code as additive only.** Wrap new code in try/except at call site. No modification to existing logic in working systems. Triggered Jun 10 2026 with rezmycv.com events.

§

Former commodities broker (broker license/background). Institutional vocabulary: contango, crack spread, term structure, backwardation, vol, carry. Skip explanations of basic commodities/futures concepts. **Commodity trading preference:** "find low, not bet high". Multi-year range (5y/15y) over short-term technicals. Likes basket trades.

§

**Personal tools hosting:** LOCAL-FIRST + Cloudflare quick tunnel (`cloudflared tunnel --url`) for ad-hoc remote access. NOT Railway — Railway can't see local filesystem. When user asks "should this go on Railway?" for personal tool, answer is "no, run locally and tunnel".

§

**LaunchAgent pattern:** restart via `launchctl kickstart -k "gui/$(id -u)/ai.hermes.<name>.gateway"` from a separate shell. Can't restart from inside any Hermes gateway (tirith blocks). **The `-9` exit code shown in `launchctl list` is HISTORICAL (last terminating signal), NOT current state** — verify with PID column + `launchctl print ... state=running`.

§

**Nick's Mac specs:** 64GB unified memory (M-series). Python: `/usr/bin/python3` = 3.9.6, `/opt/homebrew/bin/python3.11` = 3.11.15, `/opt/homebrew/bin/python3.14` = 3.14.5. Hermes venv: 3.11.

§

**Terminal redactor strips API key VALUES.** The redactor replaces actual secret values with literal `***` before terminal commands / write_file / patch runs. Diagnostic: load via dotenv in Python and check `len(loaded_value) > 70` for real keys. Workaround: paste API keys directly into chat message.

§

**Landing page rule for chat-app products:** hero + subhead + how-it-works should list 4 input sources (paper card, QR, screenshot, note) instead of "Telegram QR" in every example. Maximum 2 mentions of the chat app name in the first 3 sections. Never mention LLM model name in landing copy.

§

**Trce pivot (Sep 1 2026):** Project B pivoted from hotel F&B AI direction (Aug 26) AND free-aggregator pivot (Aug) BOTH REJECTED. Keep as Telegram-first chat-style CRM (NOT Salesforce-clone). Differentiation pillars: (a) Telegram chat UX, not form/CRM; (b) AI auto-enriches contact's company from public research; (c) crypto payment rail. Token mechanics: USD-pricing oracle (7-day TWAP) recommended to dodge volatility.

§

RezMyCV updated CVs are the *current* one (CV S2026.pdf, dated 2026-08-12) — NOT the older "Head of Strategy and Product.pdf" still in `~/.hermes/cache/documents/`. **Active job-search workflow:** read the actual CV PDF first, never assume role/career from session memory.
