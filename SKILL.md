---
name: tiered-memory-model
description: Use when designing a tiered Hermes memory layout.
---

# Tiered Memory for Hermes

## Why

Default Hermes memory uses one flat file (`MEMORY.md` + `USER.md`) injected every turn.
Both files have a fixed char budget (~50K). When they hit 100%, Hermes auto-compresses
the oldest entries — which are usually the most important ones (stable preferences,
hard rules, project structure).

The fix: split into three tiers by retrieval pattern, not by topic.

## The three tiers

```
~/.hermes/
├── MEMORY.md              # hot: always injected, ~2000 chars, NEVER grows
├── USER.md                # hot: identity + communication rules, ~1000 chars
├── pending.md             # buffer when hot tier hits threshold
├── cold.md                # grep-only archive, unbounded
└── warm/                  # lazy-loaded topic context, ~6K each
    ├── trce.md
    ├── rezmycv.md
    ├── trading.md
    ├── family.md
    ├── content.md
    ├── hermes.md
    └── projects.md
```

## What goes where

**Hot tier** (`MEMORY.md` + `USER.md`)
- Universal communication rules ("yes do that = act now")
- Hard NOs (never leak model names, no markdown in bot replies)
- Bug patterns to recognise (terminal redactor, `patch` em-dash bug)
- Workflow anchors (use absolute paths, LaunchAgent patterns)
- Cost / tool stack defaults (M3 + MiniMax image, not premium models)
- User identity (name, timezone, communication style, UI preferences)

**NOT hot**: anything project-specific, anything topic-bound, anything you'd only
need when actively working on that topic.

**Warm tier** (`warm/<topic>.md`)
- One file per active project or recurring context
- Project state: infra URLs, deploy notes, schema, recent decisions
- Procedural knowledge specific to that domain
- Loaded only when topic matches the conversation

**Cold tier** (`cold.md`)
- One-off debugging breadcrumbs
- Old job-search research
- Historical facts that might come up once
- Grep when needed, never auto-injected

## Per-turn injection

| Old layout | New layout |
|---|---|
| 74K chars always loaded | 8K chars hot + 0-9K warm on topic match |
| ~18K tokens/turn | ~2-3K tokens/turn typical |
| $1.40/mo at 30 sessions | $0.21/mo |

Reduction: ~85% per-turn token cost. Lower inference latency as a bonus.

## 10K character growth trigger

Hot MEMORY.md has a soft ceiling at 10,000 chars (well under the 50K auto-compress
limit). When adding a new fact would push past 10K:

1. Do NOT add to MEMORY.md
2. Append the fact to `pending.md` instead, with date + source
3. Ping the user on Telegram: "MEMORY.md hit 10K. N facts queued. Want to split?"
4. Wait for explicit approval before moving anything

The trigger happens at write time, not on a cron. No infrastructure needed.

## Reviewing pending.md

When you see the trigger ping, propose the split:

```
Current MEMORY.md: 10,247 bytes (over threshold)
Pending facts: 7

Proposed split:
- "TRCE bot no delete_contact rule" -> warm/trce.md (already covered there)
- "Italian restaurant near home for client dinners" -> pending.md -> cold.md (one-off)
- "Always check xyz before deploying" -> hot MEMORY.md (universal rule, kept short)
```

User approves -> you commit moves -> hot drops back to ~7K -> cycle resets.

## What NOT to do

- Don't auto-rewrite hot MEMORY.md
- Don't auto-promote entries between tiers
- Don't use a daily cron to "clean up" — it will eventually strip nuance
- Don't put project-specific rules in hot just because you mention the project often
- Don't create warm files with less than ~500 chars (just put it in cold)

## Quarterly review (manual, not automated)

Every 3 months, read MEMORY.md + USER.md + warm/*.md end-to-end. Look for:

- Stale entries (project abandoned, tool deprecated, rule no longer applies)
- Duplicates that crept in
- Facts that should move between tiers (hot->warm if no longer universal;
  warm->hot if appeared in 10+ conversations)
- Anything sensitive you don't want auto-injected forever

Cost: ~50K tokens x 4/year = ~$0.01/year. Trivial.

## Adoption for other Hermes users

This pattern drops in for any Hermes install:

1. Backup existing MEMORY.md and USER.md
2. Identify universal rules (small subset) -> hot MEMORY.md
3. Identify identity/communication profile -> hot USER.md
4. Group project knowledge by topic -> warm/<topic>.md
5. Archive one-offs -> cold.md
6. Add the 10K trigger rule to new MEMORY.md
7. Create empty pending.md

Expected effort: 30-60 minutes for a curated memory like Nick's.
Expected payoff: 85% token reduction + no more compression cliff.
