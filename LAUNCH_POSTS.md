# Launch Posts — hermes-tiered-memory

Three versions for different surfaces. All link to https://github.com/ncik8/hermes-tiered-memory.

---

## 1. Hacker News (Show HN)

**Title:** Show HN: Tiered memory layout for Hermes – cuts per-turn tokens 85%

**Body:**

I kept hitting the same wall with Hermes (the local AI agent framework from Nous Research): MEMORY.md is one flat file, capped at 50K chars, and when it fills the oldest preferences get auto-compressed away — which are usually the most important ones.

Every user hits this around 30-40K chars. The standard advice is "just trim your memory" but that throws away institutional knowledge you've spent months building.

I split mine into three tiers by **retrieval pattern**, not by topic:

- **Hot** (MEMORY.md, ~2K chars): universal rules, never grows. Always injected.
- **Warm** (warm/<topic>.md): project-specific context. Loaded only when topic matches.
- **Cold** (cold.md): searchable archive. Grep when needed.

Results on my own deployment:
- 74,872 chars/turn → 8,672 chars/turn (88% reduction)
- ~18,700 tokens/turn → ~2,800 tokens/turn
- $1.40/mo → $0.21/mo at 30 sessions
- Auto-compression: never (hot tier hard-capped at 10K with a buffer rule)

Repo has a working Python migrator, anonymised before/after example, and a 14-slide visual explainer.

A 10K trigger rule (top of MEMORY.md) handles growth automatically — new facts buffer to pending.md when MEMORY.md is full, and the agent pings you instead of auto-splitting. Quarterly manual review for the long tail.

Curious if anyone else has hit the same wall. What's your memory layout for long-running agent sessions?

https://github.com/ncik8/hermes-tiered-memory

---

## 2. Reddit r/LocalLLaMA

**Title:** Splitting my Hermes memory into hot/warm/cold tiers — 85% fewer tokens per turn

**Body:**

Been running Hermes as my main AI assistant for months. Kept running into the same issue: MEMORY.md auto-compresses when it fills, and the oldest entries are usually the ones I cared about most (stable preferences, hard rules, project state).

Tried Honcho for a while but the per-turn cost adds up and I already had well-curated memory. Tried ChromaDB but it's overkill for what I needed.

Settled on a flat-file tiered layout that needs zero new infrastructure:

```
~/.hermes/memories/
├── MEMORY.md       (~2K, always loaded, never grows)
├── USER.md         (~1K, always loaded)
├── pending.md      (buffer when hot hits 10K)
├── cold.md         (grep-only archive)
└── warm/           (~6K each, loaded only on topic match)
    ├── trading.md
    ├── project-a.md
    └── ...
```

Result on my deployment:
- **Before:** 75K chars injected every turn (~18.7K tokens)
- **After:** 8.7K chars hot + ~2K warm on topic match (~2.8K tokens)
- Cost per turn: $0.0009 → $0.0001
- No more compression cliff

A simple 10K trigger rule (in MEMORY.md itself) tells the agent "stop adding, write to pending.md instead, ping me" — no daily cron, no extra tooling.

Wrote it up as a drop-in for other Hermes users: https://github.com/ncik8/hermes-tiered-memory

Migrator script + anonymised before/after example included. Happy to hear what others are doing for long-running agent memory.

---

## 3. X (Twitter) thread

**1/**
Spent months curating my Hermes agent's memory. Then it hit 50K chars and auto-compressed away my most important rules.

Split it into 3 tiers. Per-turn tokens dropped 85%. Cost: $1.40/mo → $0.21/mo.

https://github.com/ncik8/hermes-tiered-memory

**2/**
The trick: tier by **retrieval pattern**, not by topic.

- Hot (always-injected, never grows) — universal rules
- Warm (lazy-loaded) — project context
- Cold (grep-only) — searchable archive

No new infra. Just flat files.

**3/**
10K growth trigger in MEMORY.md itself:

> if (would push past 10K) {
>   write to pending.md
>   ping user
> }

No daily cron. No magic. Agent asks before rewriting.

**4/**
Shipped: migrator script + anonymised example + 14-slide visual.

If you use Hermes and your MEMORY.md is creeping toward 50K, give it a try.

https://github.com/ncik8/hermes-tiered-memory

---

## Where to post

- **HN:** Tuesday-Thursday, 8-10am US Eastern is peak. Avoid Mondays.
- **Reddit:** r/LocalLLaMA, r/LocalLLM, r/MachineLearning. Best times: Tue-Thu morning US time.
- **X:** Any time, threads do well morning US East.

## Tips for posting

- For HN: lead with the numbers, not the philosophy. "Show HN" tag is essential.
- For Reddit: do NOT link directly to repo. Post the writeup, then drop the link in comments if asked. Reddit penalises pure self-promotion.
- For X: keep it under 5 tweets. Add the demo deck link (it's hosted in the repo at docs/deck.html).
