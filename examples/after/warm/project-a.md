# warm/project-a.md — Project A (CV tailoring platform)

# Load when: Project A, build.project-a.com, project-a-voice, CV tailoring, ATS, TailorMyCV.

## § Current state
- Investor headline: "2 CV uploaders, 6 accounts, 2 paid" (pro_plus = paying tier).
- 6 profiles in DB, 2 with user_cvs rows, 0 ghost users.
- 1 power user = pro_plus tier with cv_count=11.
- 8 verified users in auth.users (Jun 22 2026).
- No `public.users` table — uses `auth.users` + `public.profiles`.

## § Infra
- Supabase project: `aaaabbbbccccddddeeee.supabase.co`. DIFFERENT from Project B project.
- Auth setup: `~/.env.supabase.project-a` (chmod 600), `~/.env.supabase` (PAT for Management API).
- Project A voice deployed: github.com/username/project-a-voice. build.project-a.com (CNAME -> Railway).
- 7-question voice interview, MediaRecorder + faster-whisper STT, M3 for CV extraction.
- TTS optional — 7 main questions pre-warmed by scripts/warmup_audio.py.

## § MiniMax env var precedence
- When both `MINIMAX_CHAT_URL` and `MINIMAX_BASE_URL` set, code uses `MINIMAX_CHAT_URL` as source of truth.
- If unset/wrong, falls back to `MINIMAX_BASE_URL` (auto-appends /chat/completions).
- **Set them consistently** — having both pointing to different paths causes 404.

## § Position / content pillar
- **Hook: "Your designer CV is the reason you have no interviews"** — ATS doesn't render design.
- 50 designer CV templates (Canva/Behance) tested against real ATS = 0 passed cleanly.
- **4-stage buyer journey:**
  1. Standard CV = problem-aware hook
  2. ATS optimised = solution-aware how-to
  3. Tailored CV = solution-aware pitch
  4. Interviews = product-aware proof

## § Loading state UX rule (Flask/AI apps)
- 5-15s wait -> users see static "Give me a moment..." and conclude app frozen.
- **Fix:** spinner + multi-step progress UI. User words not technical.
- Pattern: `.spinner` + `.finish-steps` with `.step.active` + `.step.done`. 300ms delays.

## § Stripe / auth / events bugs (FIXED, do not reintroduce)
- **Stripe webhook (758c502):** profiles.update -> profiles.upsert.
- **sign_up in services/auth.py:** now logs errors, added missing .execute().
- **Events logger:** was threading.Thread(daemon=True) — daemon threads killed on gunicorn cleanup.
  Fix: module-level ThreadPoolExecutor(max_workers=2) + atexit handler.
- **Smoke test:** scripts/test_cv_persistence.py --write (non-destructive cleanup).

## § Funnel
- 13 funnel steps: view_landing -> view_signup -> signup -> login -> view_upload -> upload_cv -> view_paste_job -> paste_job -> view_gap_answer -> submit_gap_answer -> view_preview -> download_pdf -> click_upgrade.
- Endpoint: `GET /admin/funnel` (JSON), `GET /admin/funnel/view` (HTML).

## § Migration 006
- Idempotent ON CONFLICT DO NOTHING. Run before investor pitch for clean numbers.
