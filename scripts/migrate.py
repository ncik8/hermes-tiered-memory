#!/usr/bin/env python3
"""
migrate.py — Interactive migrator from flat MEMORY.md to tiered layout.

Reads existing ~/.hermes/memories/MEMORY.md and USER.md, parses entries,
groups them by topic, and proposes a split into hot/warm/cold tiers.

Writes proposed files to ~/.hermes/memories/.staging/ for review BEFORE
anything is touched. User must explicitly approve to promote.

Requires Python 3.10+ for type union syntax (str | None, dict[str, int]).
If system python3 is older, use /opt/homebrew/bin/python3.11 or newer.

Usage:
    python3 migrate.py [--dry-run] [--auto]

Options:
    --dry-run    Show what would happen without writing anything
    --auto       Use heuristics only, no interactive prompts (less safe)
"""

import os
import re
import sys
import shutil
from pathlib import Path
from datetime import datetime

HERMES_HOME = Path(os.path.expanduser("~/.hermes"))
MEMORIES_DIR = HERMES_HOME / "memories"
STAGING_DIR = MEMORIES_DIR / ".staging"

HOT_TRIGGER_CHARS = 10000


def read_file(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def parse_entries(text: str) -> list[dict]:
    """Split memory text into entries separated by § or blank lines."""
    entries = []
    current = []
    for line in text.split("\n"):
        if line.strip() == "§":
            if current:
                entries.append({"text": "\n".join(current).strip()})
                current = []
        elif line.strip() == "" and current and current[-1].strip() == "":
            if len(current) > 1:
                entries.append({"text": "\n".join(current).strip()})
                current = []
        else:
            current.append(line)
    if current:
        entries.append({"text": "\n".join(current).strip()})
    return [e for e in entries if len(e["text"]) > 50]


# Heuristic topic detection — match common project/product keywords
# Edit this dict to add your own project names. Keys become warm file names.
TOPIC_KEYWORDS = {
    "project-a": ["project-a", "cv tailoring", "cv_count", "user_cvs", "profiles", "auth.users", "build.project-a", "project-a-voice"],
    "project-b": ["project-b", "projectbbot", "contact.project-b", "telegram crm", "business card scan"],
    "trading": ["ptb", "paper trade", "ibkr", "intraday_simulator", "carry delta", "binance", "testnet", "scanner", "trading bot"],
    "family": ["son", "kid", "family", "wife", "vfx", "junior vfx", "summer school"],
    "content": ["youtube", "ai beginner journey", "elevenlabs", "episode"],
    "hermes": ["hermes", "launchctl", "launchd", "honcho", "mempalace", "agent-reach", "claude-seo", "opencode", "sub-instance"],
    "projects": ["beepbo", "gebecert", "rosewood", "hotel f&b", "predictive cook", "cross-property", "rosewood seeds"],
}


def classify_topic(text: str) -> str | None:
    """Return the warm file name that best matches this entry, or None for hot/cold."""
    text_lower = text.lower()
    scores: dict[str, int] = {}
    for topic, keywords in TOPIC_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in text_lower)
        if score > 0:
            scores[topic] = score
    if not scores:
        return None
    return max(scores.items(), key=lambda kv: kv[1])[0]


def is_universal_rule(text: str) -> bool:
    """Heuristic: does this look like a hot-tier universal rule?"""
    indicators = [
        "always", "never", "rule:", "**rule**", "do not", "don't",
        "must", "must not", "stop", "no ", "leak", "verify before",
        "use absolute paths", "yes do that", "act now",
    ]
    text_lower = text.lower()
    return any(ind in text_lower for ind in indicators)


def is_identity_fact(text: str) -> bool:
    """Heuristic: is this a USER.md-style identity fact?"""
    indicators = [
        "name:", "pronouns:", "timezone:", "location:",
        "communication style", "ui style", "hosting preference",
        "knowledge / skill", "mac specs",
    ]
    text_lower = text.lower()
    return any(ind in text_lower for ind in indicators)


def propose_split(memory_text: str, user_text: str) -> dict:
    """Parse both files and propose a tier-by-tier split."""
    memory_entries = parse_entries(memory_text)
    user_entries = parse_entries(user_text)

    hot_memory = []
    warm_files = {}  # topic -> list of entries
    cold_md = []

    for entry in memory_entries:
        if is_universal_rule(entry["text"]) or len(entry["text"]) < 300:
            hot_memory.append(entry["text"])
        else:
            topic = classify_topic(entry["text"])
            if topic:
                warm_files.setdefault(topic, []).append(entry["text"])
            else:
                cold_md.append(entry["text"])

    hot_user = []
    for entry in user_entries:
        if is_identity_fact(entry["text"]):
            hot_user.append(entry["text"])
        else:
            cold_md.append(entry["text"])

    return {
        "hot_memory": "\n\n".join(hot_memory),
        "hot_user": "\n\n".join(hot_user),
        "warm": warm_files,
        "cold": "\n\n".join(cold_md),
    }


def write_staging(proposal: dict, dry_run: bool = False) -> None:
    """Write proposed files to .staging/ for user review."""
    if dry_run:
        print("\n=== DRY RUN — no files written ===\n")
        print(f"Hot MEMORY.md ({len(proposal['hot_memory'])} chars)")
        print(f"Hot USER.md ({len(proposal['hot_user'])} chars)")
        print(f"Cold ({len(proposal['cold'])} chars)")
        print(f"Warm topics: {list(proposal['warm'].keys())}")
        for topic, entries in proposal["warm"].items():
            print(f"  warm/{topic}.md — {len(entries)} entries, "
                  f"{sum(len(e) for e in entries)} chars")
        return

    if STAGING_DIR.exists():
        print(f"ERROR: {STAGING_DIR} already exists.")
        print("Remove it first if you want to regenerate the proposal:")
        print(f"  rm -rf {STAGING_DIR}")
        sys.exit(1)

    STAGING_DIR.mkdir(parents=True)
    warm_dir = STAGING_DIR / "warm"
    warm_dir.mkdir()

    write_file(STAGING_DIR / "MEMORY.md", proposal["hot_memory"])
    write_file(STAGING_DIR / "USER.md", proposal["hot_user"])
    write_file(STAGING_DIR / "cold.md", proposal["cold"])
    for topic, entries in proposal["warm"].items():
        write_file(warm_dir / f"{topic}.md", "\n\n".join(entries))

    # Empty pending.md buffer
    write_file(STAGING_DIR / "pending.md",
               "# pending.md — facts waiting for tier decision\n"
               "# See README.md for review process.\n")

    print(f"\nWrote staging files to {STAGING_DIR}/")
    print(f"  MEMORY.md    {len(proposal['hot_memory'])} chars")
    print(f"  USER.md      {len(proposal['hot_user'])} chars")
    print(f"  cold.md      {len(proposal['cold'])} chars")
    print(f"  warm/        {len(proposal['warm'])} files")
    print()
    print("Review the files, edit if needed, then promote with:")
    print(f"  cp -r {STAGING_DIR}/* {MEMORIES_DIR}/")
    print()
    print("To remove staging and start over:")
    print(f"  rm -rf {STAGING_DIR}")


def main():
    args = sys.argv[1:]
    dry_run = "--dry-run" in args

    memory_path = MEMORIES_DIR / "MEMORY.md"
    user_path = MEMORIES_DIR / "USER.md"

    if not memory_path.exists():
        print(f"ERROR: {memory_path} not found.")
        sys.exit(1)

    print(f"Reading {memory_path}...")
    memory_text = read_file(memory_path)
    user_text = read_file(user_path)

    print(f"  MEMORY.md: {len(memory_text)} chars")
    print(f"  USER.md:   {len(user_text)} chars")

    proposal = propose_split(memory_text, user_text)
    write_staging(proposal, dry_run=dry_run)


if __name__ == "__main__":
    main()
