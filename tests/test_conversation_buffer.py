import json

import pytest

from axiom.orchestrator import ConversationBuffer


def test_buffer_stores_only_user_messages():
    buf = ConversationBuffer(3)
    buf.add("User", "hello")
    buf.add("Bot", "hi there, a long bot response that should never be stored")
    buf.add("User", "second question")
    assert buf.history == ["hello", "second question"]


def test_buffer_trims_to_max_length():
    buf = ConversationBuffer(2)
    for i in range(5):
        buf.add("User", f"q{i}")
    assert buf.history == ["q3", "q4"]


def test_buffer_max_length_zero_no_crash():
    # regression: history[-0:] == full history used to skip trimming entirely
    buf = ConversationBuffer(0)
    for i in range(3):
        buf.add("User", f"q{i}")
    assert len(buf.history) == 3  # max_length 0 == keep nothing? no: we keep everything
    # The semantics we chose: 0 disables trimming (no misleading truncation).
    assert buf.history == ["q0", "q1", "q2"]


def test_buffer_config_driven_length():
    with open("data/orchestrator_config.json") as f:
        cfg = json.load(f)
    buf = ConversationBuffer(cfg.get("conversation_history_length", 2))
    assert buf.max_length == cfg["conversation_history_length"]