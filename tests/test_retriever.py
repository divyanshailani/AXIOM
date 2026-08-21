from axiom.core.retriever import IntentRetriever


def _retriever(loaded_memory, retriever_config, domain):
    return IntentRetriever(loaded_memory, retriever_config, domain)


def test_retriever_svm_intent(loaded_memory, retriever_config):
    retriever = _retriever(loaded_memory, retriever_config, 'classical_ml')

    intent, score = retriever.find_intent("explain support vector machines")
    assert intent == 'ml_svm', f"Expected ml_svm, got {intent}"
    assert score > 0.35, f"Expected score > 0.35, got {score}"


def test_retriever_unknown_intent(loaded_memory, retriever_config):
    retriever = _retriever(loaded_memory, retriever_config, 'classical_ml')

    intent, score = retriever.find_intent("how to bake a cake")
    assert intent == 'unknown', f"Expected unknown, got {intent} with score {score}"
    assert score < 0.25, f"Expected score < 0.25, got {score}"


def test_retriever_key_terms_in_vocab(loaded_memory, retriever_config):
    retriever = _retriever(loaded_memory, retriever_config, 'classical_ml')
    # xgboost appears only in key_terms, never in intent questions
    assert "xgboost" in retriever.vocab_idx, "key_terms must feed the TF-IDF vocabulary"


def test_retriever_matches_key_term_query(loaded_memory, retriever_config):
    retriever = _retriever(loaded_memory, retriever_config, 'classical_ml')
    intent, score = retriever.find_intent("whats xgboost")
    assert intent != 'unknown', f"xgboost should match via key_terms, got {intent}"


def test_retriever_near_miss_tokens(loaded_memory, retriever_config):
    retriever = _retriever(loaded_memory, retriever_config, 'classical_ml')
    # 'svmm' shares the 'svm' trigram with the svm intent's words
    intent, score = retriever.find_intent("svmm")
    assert intent == 'ml_svm', f"near-miss svmm should hit ml_svm, got {intent} ({score:.3f})"


def test_retriever_short_vocab_substring_match(loaded_memory, retriever_config):
    # 'hiii' contains the short vocab word 'hi' as a substring; the n-gram
    # feature must catch it even though 'hi' is below the n-gram size.
    chitchat = _retriever(loaded_memory, retriever_config, 'chit_chat')
    intent, score = chitchat.find_intent("hiii")
    assert intent == 'gen_greeting', f"hiii should hit gen_greeting, got {intent} ({score:.3f})"


def test_retriever_pure_noise_stays_unknown(loaded_memory, retriever_config):
    retriever = _retriever(loaded_memory, retriever_config, 'classical_ml')
    intent, score = retriever.find_intent("zzzqqq")
    assert intent == 'unknown', f"pure noise should stay unknown, got {intent} ({score:.3f})"


def test_retriever_stopword_only_question(loaded_memory, retriever_config):
    # 'how are you' is 100% stopwords in the retriever; the fallback keeps raw
    # words so it can still land on gen_greeting.
    chitchat = _retriever(loaded_memory, retriever_config, 'chit_chat')
    intent, score = chitchat.find_intent("how are you")
    assert intent == 'gen_greeting', f"Expected gen_greeting, got {intent} ({score:.3f})"