"""End-to-end pipeline test for LinguaF.

Exercises the public API across three modules (descriptive statistics,
readability, lexical diversity) on a real English passage and asserts the
results are internally consistent and within plausible ranges. This is the
library equivalent of an end-to-end test: real input in, real measures out,
through the actual published functions (English path uses NLTK only — no heavy
spaCy model download required).
"""
import pytest

from linguaf import descriptive_statistics as ds
from linguaf import lexical_diversity as ld
from linguaf import readability as r

pytestmark = pytest.mark.e2e

DOCUMENTS = [
    "Computational linguistics studies the statistical modelling of natural language.",
    "It combines methods from computer science, linguistics and mathematics.",
    "Readability measures estimate how difficult a passage is to read.",
]


def test_full_measure_pipeline_is_consistent():
    # --- descriptive statistics ---
    assert ds.sentence_count(DOCUMENTS) == len(DOCUMENTS)
    assert ds.char_count(DOCUMENTS) > 0
    assert ds.letter_count(DOCUMENTS) > 0
    assert ds.char_count(DOCUMENTS) >= ds.letter_count(DOCUMENTS)

    words = ds.get_words(DOCUMENTS, lang="en")
    assert isinstance(words, list) and len(words) > 0

    avg_wlen = ds.avg_word_length(DOCUMENTS, lang="en")
    assert avg_wlen > 0

    # --- readability ---
    fre = r.flesch_reading_ease(DOCUMENTS, lang="en")
    assert -50 < fre < 121, f"Flesch reading ease out of plausible range: {fre}"

    fkg = r.flesch_kincaid_grade(DOCUMENTS, lang="en")
    assert 0 < fkg < 30, f"Flesch-Kincaid grade out of plausible range: {fkg}"

    # --- lexical diversity ---
    ttr = ld.type_token_ratio(DOCUMENTS, lang="en")  # ratio in (0, 1]
    assert 0 < ttr <= 1

    density = ld.lexical_density(DOCUMENTS, lang="en")  # percentage in (0, 100]
    assert 0 < density <= 100


def test_pipeline_rejects_invalid_input_types():
    # The public API validates its arguments; passing a bare string (not a list
    # of documents) must raise rather than silently misbehave.
    with pytest.raises(TypeError):
        ds.sentence_count("not a list of documents")
