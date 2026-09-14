# Tiered Memory for Hermes

> Hot / Warm / Cold memory layout that scales with the user instead of against the 50K char budget.

![demo](docs/deck.html) — open `docs/deck.html` in a browser for the 14-slide visual explainer.

## The problem

Default Hermes memory = one flat `MEMORY.md` file, injected every turn, capped at 50K chars. When it fills, Hermes auto-compresses the oldest entries — which are usually the most important ones (stable preferences, hard rules, project structure).

Every Hermes user hits the same wall around the 30-40K char mark.

## The fix: three tiers by retrieval pattern, not by topic

```
~/.hermes/memories/
├── MEMORY.md              # hot: always injected, ~2K chars, NEVER grows
├── USER.md                # hot: identity + communication rules, ~1K chars
├── pending.md             # buffer when hot tier hits threshold
├── cold.md                # grep-only archive, unbounded
└── warm/                  # lazy-loaded topic context, ~6K each
    ├── <project-1>.md
    ├── <project-2>.md
    └── ...
```

**Hot tier** = universal rules. Identity, communication style, hard NOs, bug patterns, workflow anchors. Loaded every turn.

**Warm tier** = per-topic context. One file per active project or recurring subject. Loaded only when topic matches.

**Cold tier** = searchable archive. One-off debugging breadcrumbs, historical facts. Grep when needed.

## Results

| Metric | Default Hermes | Tiered layout |
|---|---|---|
| Per-turn bytes (typical) | 74,872 | 8,672 hot + ~2K warm avg |
| Per-turn tokens (typical) | ~18,700 | ~2,800 |
| Per-turn cost | ~$0.0009 | ~$0.0001 |
| Per-month cost (30 sessions) | ~$1.40 | ~$0.21 |
| Auto-compression risk | Every ~30K chars | Never (hot tier capped at 10K) |

**Reduction: ~85% per-turn tokens. Lower inference latency as a bonus.**

## Adoption (5 steps, ~30 minutes)

### 1. Backup your current memory

```bash
cp ~/.hermes/memories/MEMORY.md ~/.hermes/memories/MEMORY.md.backup-$(date +%Y%m%d)
cp ~/.hermes/memories/USER.md   ~/.hermes/memories/USER.md.backup-$(date +%Y%m%d)
```

### 2. Run the migrator

```bash
python3 scripts/migrate.py
```

The migrator reads your current `MEMORY.md` + `USER.md`, detects obvious groupings
(project names as headers, dates, repeated patterns), and proposes a split.

You approve each file's contents before it's written. Nothing is overwritten
without confirmation.

### 3. Review the staging directory

The migrator writes to `~/.hermes/memories/.staging/` first. Read each file,
edit if needed, then promote to live:

```bash
cp -r ~/.hermes/memories/.staging/* ~/.hermes/memories/
```

### 4. Add the 10K trigger to your new MEMORY.md

The trigger rule goes at the top of the new hot MEMORY.md:

```markdown
# § GROWTH TRIGGER (10,000 chars): Before writing a new fact to this file,
# check size. If adding the fact would push past 10,000 chars, write it to
# pending.md instead and ping the user: "MEMORY.md hit 10K. N facts queued.
# Want to split?" Do NOT auto-split — wait for explicit approval.
```

### 5. Verify and restart

```bash
ls -la ~/.hermes/memories/{MEMORY.md,USER.md,pending.md,cold.md,warm/}
```

Next Hermes session will pick up the new layout automatically. No restart required.

## What goes where (decision tree)

```
Is this a universal rule that should apply every turn?
├─ Yes → hot tier (MEMORY.md)
└─ No → Is it topic-specific to an active project?
    ├─ Yes → warm/<project>.md
    └─ No → Is it something I might look up once?
        ├─ Yes → cold.md
        └─ No → pending.md (decide later, or drop)
```

**Hot tier examples:** "yes do that = act now", "British slang in intro copy",
"never leak model names to end users", "use absolute paths not ~/...".

**Warm tier examples:** TRCE bot schema, RezMyCV pricing, trading bot rules,
family schedule, YouTube production format.

**Cold tier examples:** old job-search research, deprecated tool gotchas,
one-off debugging breadcrumbs.

## Maintenance

### 10K trigger (automatic)

When MEMORY.md hits 10K chars, new facts auto-buffer to `pending.md` and the agent
notifies you. You decide what to move where. No daily cron.

### Quarterly review (manual)

Every 3 months, read MEMORY.md + USER.md + warm/*.md end-to-end. Look for:

- Stale entries (project abandoned, tool deprecated, rule no longer applies)
- Duplicates that crept in
- Facts that should move between tiers
- Anything sensitive you don't want auto-injected forever

Cost: ~50K tokens × 4/year = ~$0.01/year.

### What NOT to do

- Don't auto-rewrite hot MEMORY.md
- Don't auto-promote entries between tiers
- Don't use a daily cron to "clean up" — it will eventually strip nuance
- Don't put project-specific rules in hot just because you mention them often
- Don't create warm files with less than ~500 chars (just put it in cold)

## Why not just use Honcho or LangChain Memory?

| Tool | Tiering | Local | Free | Open | Hermes-ready |
|---|---|---|---|---|---|
| Honcho | yes | no | no | no | yes |
| LangChain Memory | yes | yes | yes | yes | no |
| MemGPT / Letta | yes | yes | yes | yes | no |
| ChromaDB | partial | yes | yes | yes | DIY |
| Built-in MEMORY.md | no | yes | yes | yes | yes |
| **This layout** | **yes** | **yes** | **yes** | **yes** | **yes** |

Honcho requires a hosted API + costs per dialectic reasoning call.
LangChain/MemGPT are general frameworks — you'd have to integrate them.
This is the simplest possible tiered layout that works with stock Hermes.

## Files in this repo

- `SKILL.md` — the spec, lifted from the Hermes skill format
- `scripts/migrate.py` — interactive migrator for existing Hermes users
- `examples/before.md` — sample bloated MEMORY.md (anonymised)
- `examples/after/` — what the same content looks like split into tiers
- `docs/deck.html` — 14-slide visual explainer (open in browser)
- `LICENSE` — MIT

## License

MIT — see `LICENSE`.
