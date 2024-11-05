from linguaf.descriptive_statistics import get_words, syllable_count, avg_word_length, \
    number_of_n_syllable_words, sentence_count, avg_words_per_sentence
from linguaf import __check_bool_param, __check_documents_param, __check_lang_param


def flesch_reading_ease(documents: list, lang: str = 'en', remove_stopwords: bool = False) -> float:
    """Calculates Flesch Reading Ease score based on a list of documents.
    100 -- easy to read. 0 -- hard to read.
    See Wikipedia article: https://en.wikipedia.org/wiki/Flesch%E2%80%93Kincaid_readability_tests
    Publication: Flesch 1948

    Keyword arguments:
    documents -- the list of textual documents
    lang -- language of the textual documents
    remove_stopwords -- boolean flag that shows if the function should exclude stopwords
    """
    __check_documents_param(documents)
    __check_lang_param(lang)
    __check_bool_param(remove_stopwords)

    words = get_words(documents, lang, remove_stopwords)
    asl = avg_words_per_sentence(documents, lang, remove_stopwords)
    syl_total = syllable_count(words, lang)

    if lang == 'en':
        return 206.835 - 1.015*asl - 84.6*(syl_total/len(words))
    elif lang == 'ru':
        return 206.835 - 1.3*asl - 60.1*(syl_total/len(words))  # coefficients for russian
    else:
        raise ValueError("Syllable counting is currently not supported for the language " + lang + "!")


def flesch_kincaid_grade(documents: list, lang: str = 'en', remove_stopwords: bool = False) -> float:
    """Calculates Flesch-Kincaid grade level that corresponds to a U.S. grade level.
    The higher the grade the more difficult the text.
    See Wikipedia article: https://en.wikipedia.org/wiki/Flesch%E2%80%93Kincaid_readability_tests
    Publication: Flesch and Kincaid 1975

    Keyword arguments:
    documents -- the list of textual documents
    lang -- language of the textual documents
    remove_stopwords -- boolean flag that shows if the function should exclude stopwords
    """
    __check_documents_param(documents)
    __check_lang_param(lang)
    __check_bool_param(remove_stopwords)

    words = get_words(documents, lang, remove_stopwords)
    asl = avg_words_per_sentence(documents)
    syl_total = syllable_count(words, lang)

    if lang == 'en':
        return 0.39*asl + 11.8*(syl_total/len(words)) - 15.59
    elif lang == 'ru':
        return 0.5*asl + 8.4*(syl_total/len(words)) - 15.59  # coefficients for russian
    else:
        raise ValueError("Syllable counting is currently not supported for the language " + lang + "!")


def automated_readability_index(documents: list, lang: str = 'en', remove_stopwords: bool = False) -> float:
    """Calculates automated readability index based on a list of textual documents.
    The more the index the harder the text.
    The score corresponds to a grade level (similar to Flesh-Kincaid grade).
    See Wikipedia article: https://en.wikipedia.org/wiki/Automated_readability_index
    Publication: Senter and Smith 1967

    Keyword arguments:
    documents -- the list of textual documents
    lang -- language of the textual documents
    remove_stopwords -- boolean flag that shows if the function should exclude stopwords
    """
    __check_documents_param(documents)
    __check_lang_param(lang)
    __check_bool_param(remove_stopwords)

    asl = avg_words_per_sentence(documents, lang, remove_stopwords)
    awl = avg_word_length(documents, lang, remove_stopwords)

    return 0.5*asl + 4.71*awl - 21.43


def automated_readability_index_simple(documents: list, lang: str = 'en', remove_stopwords: bool = False) -> float:
    """Calculates simplified automated readability index based on a list of textual documents.
    The more the index the harder the text.
    See Wikipedia article: https://en.wikipedia.org/wiki/Automated_readability_index
    Publication: Senter and Smith 1967

    Keyword arguments:
    documents -- the list of textual documents
    lang -- language of the textual documents
    remove_stopwords -- boolean flag that shows if the function should exclude stopwords
    """
    __check_documents_param(documents)
    __check_lang_param(lang)
    __check_bool_param(remove_stopwords)

    asl = avg_words_per_sentence(documents, lang, remove_stopwords)
    awl = avg_word_length(documents, lang, remove_stopwords)

    return asl + 9.0*awl


def coleman_readability(documents: list, lang: str = 'en', remove_stopwords: bool = False) -> float:
    """Calculates Coleman's Readability score based on a list of textual documents.
    Publication: Coleman, E.B. (1971)

    Keyword arguments:
    documents -- the list of textual documents
    lang -- language of the textual documents
    remove_stopwords -- boolean flag that shows if the function should exclude stopwords
    """
    __check_documents_param(documents)
    __check_lang_param(lang)
    __check_bool_param(remove_stopwords)

    words = get_words(documents, lang, remove_stopwords)
    nws_one = number_of_n_syllable_words(documents, lang, (1, 2), remove_stopwords)

    return 1.29*(100*nws_one/len(words)) - 38.45


def easy_listening(documents: list, lang: str = 'en', remove_stopwords: bool = False) -> float:
    """Calculates Easy Listening score based on a list of textual documents.
    Publication: Fang 1966

    Keyword arguments:
    documents -- the list of textual documents
    lang -- language of the textual documents
    remove_stopwords -- boolean flag that shows if the function should exclude stopwords
    """
    __check_documents_param(documents)
    __check_lang_param(lang)
    __check_bool_param(remove_stopwords)

    nst = sentence_count(documents)
    nws_more_two = number_of_n_syllable_words(documents, lang, (2, 15), remove_stopwords)

    return nws_more_two/nst
