# Copyright (c) 2026 Divyansh Ailani. All Rights Reserved.
# This file is part of AXIOM and is proprietary and confidential.

import json
import random
from pathlib import Path

class TemplateGenerator:
    def __init__(self, memory_path: Path):
        with open(memory_path) as f:
            self.memory = json.load(f)
            
    def generate(self, domain: str, intent_id: str) -> str:
        if intent_id == "unknown":
            return f"I don't have knowledge about that in my current memory. Try asking about topics in '{domain}'."
            
        intents = self.memory['domains'].get(domain, {}).get('intents', [])
        for intent_obj in intents:
            if intent_obj['intent_id'] == intent_id:
                templates = intent_obj.get('response_templates', [])
                if templates:
                    return random.choice(templates)
                    
        return "I found an intent, but I have no response templates for it."
