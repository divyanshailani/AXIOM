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

class AxiomInputError(ValueError):
    """Raised when a user prompt cannot be processed (non-string or empty)."""

class ConversationBuffer:
    def __init__(self, max_length: int):
        self.max_length = max(max_length, 0)
        self.history = []
        
    def add(self, role: str, text: str):
        # We only buffer User text to prevent the Bot's long responses 
        # from diluting the vector math and confusing the Router.
        if role == "User":
            self.history.append(text)
            if len(self.history) > self.max_length and self.max_length > 0:
                self.history = self.history[-self.max_length:]

class AxiomOrchestrator:
    def __init__(self):
        base_dir = Path(__file__).parent.parent
        
        # Meta-Fix: Load and patch memory dynamically
        self.memory_dict = MemoryBootstrap(base_dir).load_memory()
        
        config_path = base_dir / "data" / "orchestrator_config.json"
        with open(config_path, encoding="utf-8") as f:
            self.config = json.load(f)
            
        router_config_path = base_dir / "data" / "router_config.json"
        self.retriever_config_path = base_dir / "data" / "retriever_config.json"
        
        # Single source of truth for the low-confidence fallback band.
        # The chit_chat safety net only triggers below this threshold, and a
        # recovered chit_chat intent must clear its own (independent) bar.
        with open(self.retriever_config_path, encoding="utf-8") as f:
            retriever_config = json.load(f)
        self.retrieval_threshold = float(retriever_config.get('similarity_threshold', 0.15))
        self.chitchat_admission = float(retriever_config.get('chitchat_admission', 0.25))
        
        self.router = NaiveBayesRouter(self.memory_dict, router_config_path)
        self.generator = TemplateGenerator(self.memory_dict)
        
        self.buffer = ConversationBuffer(self.config.get('conversation_history_length', 2))
        self._empty_response = None
        
    @staticmethod
    def _coerce_prompt(user_prompt):
        if not isinstance(user_prompt, str):
            raise AxiomInputError(f"Expected a string prompt, got {type(user_prompt).__name__}.")
        stripped = user_prompt.strip()
        if not stripped:
            raise AxiomInputError("Empty prompt.")
        return stripped
        
    def chat(self, user_prompt) -> AxiomResponse:
        try:
            contextual_prompt = self._coerce_prompt(user_prompt)
        except AxiomInputError as exc:
            # Provider of last resort: never crash the CLI / caller on bad input.
            if self._empty_response is None:
                self._empty_response = AxiomResponse(
                    response_text="I didn't catch that. Could you rephrase?",
                    domain="chit_chat",
                    domain_confidence=1.0,
                    intent_id="gen_feedback",
                    similarity_score=1.0,
                )
            return self._empty_response
        
        self.buffer.add("User", contextual_prompt)
        
        # We process each query independently. Concatenating past queries 
        # causes severe cross-contamination in Bag-of-Words math.
        
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
        if score < self.retrieval_threshold and domain_name != "chit_chat":
            # Try chit_chat as a safety net for conversational fragments
            cc_retriever = IntentRetriever(self.memory_dict, self.retriever_config_path, "chit_chat")
            cc_intent_id, cc_score = cc_retriever.find_intent(augmented_prompt)
            if cc_score >= self.chitchat_admission:
                domain_name = "chit_chat"
                intent_id = cc_intent_id
                score = cc_score
                # The confidence reported must belong to the domain we adopt.
                domain_conf = domain_probs.get("chit_chat", 0.0)
        
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