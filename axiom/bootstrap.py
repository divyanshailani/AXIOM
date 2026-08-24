# Copyright (c) 2026 Divyansh Ailani. All Rights Reserved.
# This file is part of AXIOM and is proprietary and confidential.

import json
from pathlib import Path

class MemoryBootstrap:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.memory_path = base_dir / "data" / "memory.json"
        self.patch_path = base_dir / "data" / "memory_patch.json"

    _KNOWN_ACTIONS = {"add_questions", "add_intent", "add_router_keywords"}

    def _apply_patch(self, base: dict, patch: dict):
        domain = patch.get("domain")
        action = patch.get("action")

        if domain not in base["domains"]:
            # Fail loudly: a typo'd domain is an operator error, not a silent no-op.
            raise ValueError(f"Patch references unknown domain {domain!r}.")
        if action not in self._KNOWN_ACTIONS:
            raise ValueError(f"Patch has unknown action {action!r} for domain {domain!r}.")

        if action == "add_questions":
            intent_id = patch.get("intent_id")
            questions = patch.get("questions", [])
            if not isinstance(questions, list) or not questions:
                raise ValueError(f"add_questions for {domain}/{intent_id} needs a non-empty questions list.")
            for intent in base["domains"][domain]["intents"]:
                if intent["intent_id"] == intent_id:
                    # Idempotent replay: skip questions the intent already has
                    # (including duplicates within this same patch) so applying
                    # the transaction log twice cannot corrupt training data.
                    existing = set(intent["questions"])
                    for q in questions:
                        if q not in existing:
                            intent["questions"].append(q)
                            existing.add(q)
                    break
            else:
                raise ValueError(f"add_questions references unknown intent {intent_id!r} in {domain!r}.")
        elif action == "add_intent":
            intent = patch.get("intent")
            if not isinstance(intent, dict) or not intent.get("intent_id"):
                raise ValueError(f"add_intent for {domain!r} needs an intent dict with intent_id.")
            existing = {i["intent_id"] for i in base["domains"][domain]["intents"]}
            if intent["intent_id"] in existing:
                raise ValueError(f"add_intent duplicates intent {intent['intent_id']!r} in {domain!r}.")
            base["domains"][domain]["intents"].append(intent)
        elif action == "add_router_keywords":
            keywords = patch.get("keywords", [])
            if not isinstance(keywords, list) or not keywords:
                raise ValueError(f"add_router_keywords for {domain!r} needs a non-empty keywords list.")
            # Same idempotency rule as add_questions: replays are no-ops.
            existing = set(base["domains"][domain]["router_keywords"])
            for kw in keywords:
                if kw not in existing:
                    base["domains"][domain]["router_keywords"].append(kw)
                    existing.add(kw)

    def load_memory(self, memory_path: Path = None) -> dict:
        with open(memory_path or self.memory_path) as f:
            base = json.load(f)
            
        if self.patch_path.exists():
            with open(self.patch_path) as f:
                patches = json.load(f)
            for patch in patches.get("patches", []):
                self._apply_patch(base, patch)
                
        return base
