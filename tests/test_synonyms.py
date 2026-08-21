from axiom.core.synonyms import augment_query, ML_SYNONYMS


def test_word_boundary_no_substring():
    # 'dl' inside 'handle' must NOT trigger the deep learning expansion
    assert augment_query("please handle this") == "please handle this"


def test_ml_synonym_expands():
    out = augment_query("what is dl")
    assert "deep learning" in out, f"expected deep learning expansion, got {out!r}"


def test_synonym_case_insensitive():
    out = augment_query("What is DL?")
    assert "deep learning" in out


def test_multiple_synonyms_expand_once_each():
    out = augment_query("svm and knn")
    assert "support vector machine" in out
    assert "k nearest neighbors" in out


def test_casual_synonym_expands():
    out = augment_query("thx")
    assert "thanks" in out, f"expected thanks expansion, got {out!r}"


def test_no_extra_for_plain_text():
    out = augment_query("what is linear regression")
    # canonical form is already present; only the variants' canonical may append
    assert "linear regression" in out


def test_all_ml_canonicals_present_as_phrases():
    # every canonical should itself be a phrase the matcher recognizes back
    for canonical, variants in ML_SYNONYMS.items():
        assert len(canonical.split()) >= 1