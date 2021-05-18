from linguaf.descriptive_statistics import get_words, syllable_count


def flesh_reading_ease(documents: list, lang: str = 'en', remove_stopwords: bool = False) -> float:
    words = get_words(documents, lang, remove_stopwords)
    syl_total = syllable_count(words, lang)

    if lang == 'en':
        return 206.835 - 1.015 * (len(words) / len(documents)) - 84.6 * (syl_total / len(words))
    elif lang == 'ru':
        return 206.835 - 1.52 * (len(words) / len(documents)) - 65.14 * (
                    syl_total / len(words))  # coefficients for russian
