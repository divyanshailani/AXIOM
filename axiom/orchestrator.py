# Copyright (c) 2026 Divyansh Ailani. All Rights Reserved.
# This file is part of AXIOM and is proprietary and confidential.

import json
from pathlib import Path
from dataclasses import dataclass

from axiom.core.router import NaiveBayesRouter
from axiom.core.retriever import IntentRetriever
from axiom.core.generator import TemplateGenerator
from axiom.bootstrap import MemoryBootstrap
from axiom.core.synonyms import augment_query

@dataclass
class AxiomResponse:
    response_text: str
    domain: str
    domain_confidence: float
    intent_id: str
    similarity_score: float

class ConversationBuffer:
    def __init__(self, max_length: int):
        self.max_length = max_length
        self.history = []
        
    def add(self, role: str, text: str):
        # We only buffer User text to prevent the Bot's long responses 
        # from diluting the vector math and confusing the Router.
        if role == "User":
            self.history.append(text)
            if len(self.history) > self.max_length:
                self.history = self.history[-self.max_length:]
            
    def get_context(self) -> str:
        # Join previous user prompts to provide context for pronouns
        return " ".join(self.history[:-1]) if len(self.history) > 1 else ""

class AxiomOrchestrator:
    def __init__(self):
        base_dir = Path(__file__).parent.parent
        self.memory_path = base_dir / "data" / "memory.json"
        
        # Meta-Fix: Load and patch memory dynamically
        self.memory_dict = MemoryBootstrap(base_dir).load_memory()
        
        config_path = base_dir / "data" / "orchestrator_config.json"
        with open(config_path) as f:
            self.config = json.load(f)
            
        router_config_path = base_dir / "data" / "router_config.json"
        self.retriever_config_path = base_dir / "data" / "retriever_config.json"
        
        self.router = NaiveBayesRouter(self.memory_dict, router_config_path)
        self.generator = TemplateGenerator(self.memory_dict)
        
        self.buffer = ConversationBuffer(self.config.get('conversation_history_length', 2))
        
    def chat(self, user_prompt: str) -> AxiomResponse:
        self.buffer.add("User", user_prompt)
        
        # We process each query independently. Concatenating past queries 
        # causes severe cross-contamination in Bag-of-Words math.
        contextual_prompt = user_prompt.strip()
        
        # 0. Synonyms Augmentation (Issue 4)
        augmented_prompt = augment_query(contextual_prompt)
        
        # 1. Route to domain
        domain_probs = self.router.predict_proba(augmented_prompt)
        best_domain = max(domain_probs.items(), key=lambda x: x[1])
        domain_name, domain_conf = best_domain[0], best_domain[1]
        
        # 2. Retrieve intent
        retriever = IntentRetriever(self.memory_dict, self.retriever_config_path, domain_name)
        intent_id, score = retriever.find_intent(augmented_prompt)
        
        # NEW: Graceful fallback for low confidence (Issue 5)
        if score < 0.20 and domain_name != "chit_chat":
            # Try chit_chat as a safety net for conversational fragments
            cc_retriever = IntentRetriever(self.memory_dict, self.retriever_config_path, "chit_chat")
            cc_intent_id, cc_score = cc_retriever.find_intent(augmented_prompt)
            if cc_score >= 0.25:
                domain_name = "chit_chat"
                intent_id = cc_intent_id
                score = cc_score
        
        # 3. Generate response
        response_text = self.generator.generate(domain_name, intent_id)
        
        self.buffer.add("Bot", response_text)
        
        return AxiomResponse(
            response_text=response_text,
            domain=domain_name,
            domain_confidence=domain_conf,
            intent_id=intent_id,
            similarity_score=score
        )
