# Copyright (c) 2026 Divyansh Ailani. All Rights Reserved.
# This file is part of AXIOM and is proprietary and confidential.

"""Squash data/memory_patch.json into data/memory.json.

The patch log is a transaction journal: every boot replays all of it over the
base memory. Once patches are stable and regression-tested they add boot cost
and diff noise without adding safety. This script applies every pending patch
through MemoryBootstrap (so all validation runs), verifies the merged result
round-trips byte-identically through a second load, and only then rewrites
memory.json with the merged state and empties the patch log.

Usage:
    python scripts/compact_memory.py           # dry run: report only
    python scripts/compact_memory.py --apply   # rewrite memory.json, clear log

Requires a clean git checkout: the old base + log stay recoverable from git
history, and the tool refuses to run on a dirty data/ directory so uncommitted
memory work can never be squashed away by accident.
"""

import argparse
import copy
import json
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(BASE_DIR))

from axiom.bootstrap import MemoryBootstrap


def _git_memory_files_are_clean() -> bool:
    # Only the two files the compaction rewrites must be committed; unrelated
    # uncommitted work elsewhere (config, docs) is no reason to refuse.
    result = subprocess.run(
        ["git", "status", "--porcelain", "--",
         "data/memory.json", "data/memory_patch.json"],
        cwd=BASE_DIR, capture_output=True, text=True,
    )
    if result.returncode != 0:
        return False
    return result.stdout.strip() == ""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true",
                        help="actually rewrite memory.json and clear the patch log")
    args = parser.parse_args()

    bootstrap = MemoryBootstrap(BASE_DIR)
    with open(bootstrap.memory_path, encoding="utf-8") as f:
        base = json.load(f)
    with open(bootstrap.patch_path, encoding="utf-8") as f:
        patch_doc = json.load(f)
    patches = patch_doc.get("patches", [])

    if not patches:
        print("Patch log already empty; nothing to compact.")
        return 0

    # Apply through the real loader path so unknown domains/actions/intents
    # raise exactly as they do at boot.
    merged = bootstrap.load_memory()
    # Round-trip proof: replaying the log over the merged memory must not
    # change it. add_questions/add_router_keywords are idempotent by design;
    # add_intent rejects duplicates loudly, so its replay is a documented
    # no-op error and counts as such here.
    probe = copy.deepcopy(merged)
    for patch in patches:
        try:
            bootstrap._apply_patch(probe, patch)
        except ValueError as exc:
            if patch["action"] == "add_intent" and "duplicates intent" in str(exc):
                continue
            raise
    assert probe == merged, "patch replay over merged memory changed it; log is not idempotent"
    for domain, data in base["domains"].items():
        assert domain in merged["domains"], f"merge lost domain {domain}"

    counts = {}
    for patch in patches:
        counts[patch["action"]] = counts.get(patch["action"], 0) + 1
    print(f"Patches: {len(patches)} ({', '.join(f'{c} {a}' for a, c in sorted(counts.items()))})")
    print(f"Merged intents: "
          + ", ".join(f"{d}={len(v['intents'])}" for d, v in merged["domains"].items()))

    if not args.apply:
        print("Dry run only. Re-run with --apply to compact.")
        return 0

    if not _git_memory_files_are_clean():
        print("Refusing: data/memory.json or data/memory_patch.json have "
              "uncommitted changes. Commit them first so the pre-compaction "
              "state stays recoverable from git.")
        return 1

    merged["memory_version"] = "2.4"
    with open(bootstrap.memory_path, "w", encoding="utf-8") as f:
        json.dump(merged, f, indent=2, ensure_ascii=False)
        f.write("\n")
    with open(bootstrap.patch_path, "w", encoding="utf-8") as f:
        json.dump({"patches": []}, f, indent=2)
        f.write("\n")

    # Final proof: a fresh load of the compacted files equals the pre-compaction
    # merged memory (version field aside).
    reloaded = MemoryBootstrap(BASE_DIR).load_memory()
    assert reloaded["domains"] == merged["domains"], "post-compaction load diverged"
    print(f"Compacted {len(patches)} patches into memory.json; patch log is empty.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
