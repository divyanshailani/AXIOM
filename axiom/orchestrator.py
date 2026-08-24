# Copyright (c) 2026 Divyansh Ailani. All Rights Reserved.
# This file is part of AXIOM and is proprietary and confidential.

import json
from datetime import datetime, timezone
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
    """Raised when a user prompt cannot be processed (non-string, empty, or
    content-free such as punctuation-only input)."""

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

        config_path = base_dir / "data" / "orchestrator_config.json"
        with open(config_path, encoding="utf-8") as f:
            self.config = json.load(f)

        # Meta-Fix: Load and patch memory dynamically. The memory location is
        # config-driven so test rigs can point the engine elsewhere.
        memory_relpath = self.config.get('memory_path', 'data/memory.json')
        self.memory_dict = MemoryBootstrap(base_dir).load_memory(
            base_dir / memory_relpath
        )

        router_config_path = base_dir / "data" / "router_config.json"
        self.retriever_config_path = base_dir / "data" / "retriever_config.json"

        # Single source of truth for the low-confidence fallback band.
        # The chit_chat safety net only triggers below this threshold, and a
        # recovered chit_chat intent must clear its own (independent) bar.
        with open(self.retriever_config_path, encoding="utf-8") as f:
            retriever_config = json.load(f)
        self.retrieval_threshold = float(retriever_config.get('similarity_threshold', 0.15))
        self.chitchat_admission = float(retriever_config.get('chitchat_admission', 0.25))

        # Context retry: when standalone retrieval fails or stays weak, the
        # previous user query is concatenated as a second attempt so pronoun
        # follow-ups ("what about its variance?") resolve against the
        # established topic. Gates below keep this from hijacking queries that
        # already stand on their own.
        retry_cfg = self.config.get('context_retry', {})
        self.context_retry_enabled = bool(retry_cfg.get('enabled', True))
        self.context_retry_min_score = float(retry_cfg.get('min_score', 0.35))
        self.context_retry_floor = float(retry_cfg.get('standalone_floor', 0.30))

        miss_log_relpath = self.config.get('miss_log_path')
        self.miss_log_path = (base_dir / miss_log_relpath) if miss_log_relpath else None

        self.router = NaiveBayesRouter(self.memory_dict, router_config_path)
        self.generator = TemplateGenerator(self.memory_dict)

        # Retrievers are precomputed once per domain. Building one per message
        # re-parsed configs and recomputed TF-IDF on every single query.
        self._retrievers = {
            domain: IntentRetriever(self.memory_dict, self.retriever_config_path, domain)
            for domain in self.memory_dict['domains']
        }

        self.buffer = ConversationBuffer(self.config.get('conversation_history_length', 2))
        self._empty_response = None
        self._last_domain = None

    @staticmethod
    def _coerce_prompt(user_prompt):
        if not isinstance(user_prompt, str):
            raise AxiomInputError(f"Expected a string prompt, got {type(user_prompt).__name__}.")
        stripped = user_prompt.strip()
        if not stripped:
            raise AxiomInputError("Empty prompt.")
        if not any(ch.isalnum() for ch in stripped):
            # Punctuation-only input would route by priors alone and produce a
            # misleading "I don't have knowledge about 'domain'" answer.
            raise AxiomInputError("Prompt has no readable content.")
        return stripped

    def _log_miss(self, query: str, reason: str, routed_domain: str,
                  detail: dict, domain_probs: dict):
        """Appends a fallback event to the miss log so tuning is data-driven.

        Logging must never break chatting, so any IO problem is swallowed.
        """
        if self.miss_log_path is None:
            return
        entry = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "query": query,
            "reason": reason,
            "routed_domain": routed_domain,
            "router_top3": sorted(domain_probs.items(), key=lambda x: -x[1])[:3],
            "best_intent": detail.get("intent_id"),
            "score": round(float(detail.get("score", 0.0)), 4),
            "runner_up_score": round(float(detail.get("runner_up_score", 0.0)), 4),
        }
        try:
            self.miss_log_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.miss_log_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        except OSError:
            pass

    def _retrieve(self, prompt: str, domain_name: str) -> dict:
        return self._retrievers[domain_name].find_intent_detailed(prompt)

    def _context_retry(self, contextual_prompt: str, augmented_prompt: str,
                       previous_prompt: str, primary_domain: str,
                       primary_score: float) -> dict:
        """Second retrieval pass over the previous query + current one.

        Only runs when standalone matching already failed or stayed weak. Two
        gates keep it from hijacking legitimate standalone answers: the merged
        match must clear the raised min_score bar AND hold at least twice the
        primary evidence (a real follow-up fragment collapses without its
        topic; a complete question does not).
        """
        if not self.context_retry_enabled or previous_prompt is None:
            return None
        merged_query = previous_prompt + " " + contextual_prompt
        merged_augmented = augment_query(merged_query)

        candidate_domains = [primary_domain]
        if (self._last_domain and self._last_domain != primary_domain
                and self._last_domain != "chit_chat"):
            candidate_domains.append(self._last_domain)

        best = None
        for domain in candidate_domains:
            detail = self._retrieve(merged_augmented, domain)
            if best is None or detail["score"] > best["score"]:
                best = detail
                best["domain"] = domain
        if best is None or not best["accepted"]:
            return None
        if best["score"] < self.context_retry_min_score:
            return None
        if best["score"] < 2.0 * primary_score:
            return None
        best["reason"] = "context_retry"
        return best

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

        # Capture the previous turn before buffering this one: the retry must
        # concatenate the PRIOR query with the current one.
        previous_prompt = self.buffer.history[-1] if self.buffer.history else None
        self.buffer.add("User", contextual_prompt)

        # We process each query independently first. Concatenating past queries
        # into the primary pass causes severe cross-contamination in Bag-of-Words
        # math; past context is only consulted as an explicit retry below.

        # 0. Synonyms Augmentation (Issue 4)
        augmented_prompt = augment_query(contextual_prompt)

        # 1. Route to domain
        domain_probs = self.router.predict_proba(augmented_prompt)
        best_domain = max(domain_probs.items(), key=lambda x: x[1])
        domain_name, domain_conf = best_domain[0], best_domain[1]

        # 2. Retrieve intent (cached retriever for the routed domain)
        detail = self._retrieve(augmented_prompt, domain_name)
        intent_id, score = detail["intent_id"], detail["score"]

        # Graceful fallback for low confidence (Issue 5)
        if not detail["accepted"] and domain_name != "chit_chat":
            # Try chit_chat as a safety net for conversational fragments
            cc_detail = self._retrieve(augmented_prompt, "chit_chat")
            if cc_detail["accepted"] and cc_detail["score"] >= self.chitchat_admission:
                domain_name = "chit_chat"
                detail = cc_detail
                intent_id, score = cc_detail["intent_id"], cc_detail["score"]
                # The confidence reported must belong to the domain we adopt.
                domain_conf = domain_probs.get("chit_chat", 0.0)

        # Context retry: resolve follow-up fragments against the previous topic.
        # Fires only when the query failed to stand on its own (score below
        # standalone_floor) and is not itself conversational — chit_chat turns
        # belong to the social flow, not the topic thread, and must never be
        # reinterpreted through the previous topic's vocabulary.
        if (self.context_retry_enabled
                and score < self.context_retry_floor
                and domain_name != "chit_chat"):
            retry = self._context_retry(contextual_prompt, augmented_prompt,
                                        previous_prompt, domain_name, score)
            if retry is not None:
                domain_name = retry["domain"]
                detail = retry
                intent_id, score = retry["intent_id"], retry["score"]
                domain_conf = domain_probs.get(domain_name, 0.0)

        if not detail["accepted"]:
            self._log_miss(contextual_prompt, detail["reason"], domain_name,
                           detail, domain_probs)

        # 3. Generate response
        response_text = self.generator.generate(domain_name, intent_id)

        self.buffer.add("Bot", response_text)
        self._last_domain = domain_name

        return AxiomResponse(
            response_text=response_text,
            domain=domain_name,
            domain_confidence=domain_conf,
            intent_id=intent_id,
            similarity_score=score
        )
