# warm/hermes.md — Hermes infrastructure + skills + patterns

# Load when: Hermes, hermes-agent, gateway, sub-instance, LaunchAgent, launchctl, launchd, .hermes config, memory compression, Honcho, MemPalace, dailysync.

## § Hermes sub-instance management
- **All `~/.hermes-*` sub-instances SHARE the main `~/.hermes/hermes-agent` code + venv.** Differ only by `HERMES_HOME` env var.
- `hermes update` on main = update for all sub-instances.
- Only state per-instance (config.yaml, state.db, memories).

## § Hermes v31->v40 update procedure
1. `hermes update` does config + Python deps + code.
2. `brew upgrade node` (fixes EBADENGINE).
3. `npm install` — temporarily `del` the `workspaces` field from package.json to avoid hang.
4. `hermes sessions optimize-storage` reclaims ~50% of state.db.

## § LaunchAgent pattern
- Restart: `launchctl kickstart -k "gui/$(id -u)/ai.hermes.<name>.gateway"` from a separate shell.
- **The `-9` exit code in `launchctl list` is HISTORICAL, NOT current state.**

## § Provider routing
- Three subsystems share one routing layer:
  1. **Auxiliary tasks** via `auxiliary.{task}.provider/model` config.
  2. **Subagent dispatch** via `delegate_task` model override.
  3. **Main conversation** via `model.default`.
- Config memoised on `.env` mtime — editing config.yaml alone does NOT reload; restart gateway.
- **Compression gotcha:** `auxiliary.compression.provider: auto` -> picks Claude (blocked in HK). Set explicit.

## § Memory subsystem
- Tiered layout: hot (always loaded), warm (lazy-loaded), cold (grep).
- 10K trigger: before adding to MEMORY.md, check size. If push past 10K, write to pending.md.
- See `tiered-memory-model` skill for full pattern.
- **Honcho integration (configured but NOT active):** API key already in `~/.hermes/.env`.

## § Agent-Reach
- Panniantong/Agent-Reach at `~/.agent-reach-venv/` (Python 3.11.15 from Homebrew).
- 6/15 channels active out of box: Exa, Jina Reader, V2EX, RSS, YouTube, B站.
- Skill: `devops/agent-reach`.

## § Sub-instances currently running
- beanboy, bizmind, clawpack, coinc, games, gebecert, mingyun, dashboard.
- Each has own MEMORY.md/USER.md. Henry is orchestrator index.
