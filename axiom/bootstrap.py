# Copyright (c) 2026 Divyansh Ailani. All Rights Reserved.
# This file is part of AXIOM and is proprietary and confidential.

import json
from pathlib import Path

class MemoryBootstrap:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.memory_path = base_dir / "data" / "memory.json"
        self.patch_path = base_dir / "data" / "memory_patch.json"

    def _apply_patch(self, base: dict, patch: dict):
        domain = patch.get("domain")
        action = patch.get("action")
        
        if domain not in base["domains"]:
            return

        if action == "add_questions":
            intent_id = patch.get("intent_id")
            questions = patch.get("questions", [])
            for intent in base["domains"][domain]["intents"]:
                if intent["intent_id"] == intent_id:
                    intent["questions"].extend(questions)
                    break
        elif action == "add_intent":
            intent = patch.get("intent")
            base["domains"][domain]["intents"].append(intent)
        elif action == "add_router_keywords":
            keywords = patch.get("keywords", [])
            base["domains"][domain]["router_keywords"].extend(keywords)

    def load_memory(self) -> dict:
        with open(self.memory_path) as f:
            base = json.load(f)
            
        if self.patch_path.exists():
            with open(self.patch_path) as f:
                patches = json.load(f)
            for patch in patches.get("patches", []):
                self._apply_patch(base, patch)
                
        return base
