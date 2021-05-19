from linguaf.descriptive_statistics import get_words, syllable_count, avg_sentence_length, avg_word_length, \
    number_of_n_syllable_words, sentence_count, words_per_sentence


def flesh_reading_ease(documents: list, lang: str = 'en', remove_stopwords: bool = False) -> float:
    words = get_words(documents, lang, remove_stopwords)
    asl = words_per_sentence(documents, lang, remove_stopwords)
    syl_total = syllable_count(words, lang)

    if lang == 'en':
        return 206.835 - 1.015*asl - 84.6*(syl_total/len(words))
    elif lang == 'ru':
        return 206.835 - 1.3*asl - 60.1*(syl_total/len(words))  # coefficients for russian


def flesh_kincaid_grade(documents: list, lang: str = 'en', remove_stopwords: bool = False) -> float:
    words = get_words(documents, lang, remove_stopwords)
    asl = words_per_sentence(documents)
    syl_total = syllable_count(words, lang)

    if lang == 'en':
        return 0.39*asl + 11.8*(syl_total/len(words)) - 15.59
    elif lang == 'ru':
        return 0.5*asl + 8.4*(syl_total/len(words)) - 15.59  # coefficients for russian


def automated_readability_index(documents: list, lang: str = 'en', remove_stopwords: bool = False) -> float:
    asl = words_per_sentence(documents, lang, remove_stopwords)
    awl = avg_word_length(documents, lang, remove_stopwords)

    return 0.5*asl + 4.71*awl - 21.43


def automated_readability_index_simple(documents: list, lang: str = 'en', remove_stopwords: bool = False) -> float:
    asl = words_per_sentence(documents, lang, remove_stopwords)
    awl = avg_word_length(documents, lang, remove_stopwords)

    return asl + 9.0*awl


def coleman_readability(documents: list, lang: str = 'en', remove_stopwords: bool = False) -> float:
    words = get_words(documents, lang, remove_stopwords)
    nws_one = number_of_n_syllable_words(words, lang, (1, 2))

    return 1.29*(100*nws_one/len(words)) - 38.45


def easy_listening(documents: list, lang: str = 'en', remove_stopwords: bool = False) -> float:
    nst = sentence_count(documents)
    words = get_words(documents, lang, remove_stopwords)
    nws_more_two = number_of_n_syllable_words(words, lang, (2, 15))

    return nws_more_two/nst
