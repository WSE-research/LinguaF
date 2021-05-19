import collections
import math
from linguaf.descriptive_statistics import get_words, get_lexical_items


def lexical_density(documents: list, lang: str = 'en', remove_stopwords: bool = False) -> float:
    words = get_words(documents=documents, lang=lang, remove_stopwords=remove_stopwords)
    lex_items = get_lexical_items(documents=documents, remove_stopwords=remove_stopwords, lang=lang)
    return len(lex_items)/len(words)*100


def type_toke_ratio(documents: list, lang: str = 'en', remove_stopwords: bool = False) -> float:
    words = get_words(documents=documents, lang=lang, remove_stopwords=remove_stopwords)
    num_unq = len(collections.Counter(words).keys())
    return num_unq/len(words)*100


def log_type_token_ratio(documents: list, lang: str = 'en', remove_stopwords: bool = False) -> float:
    words = get_words(documents=documents, lang=lang, remove_stopwords=remove_stopwords)
    num_unq = len(collections.Counter(words).keys())
    return math.log(num_unq)/math.log(len(words))*100


def summer_index(documents: list, lang: str = 'en', remove_stopwords: bool = False) -> float:
    words = get_words(documents=documents, lang=lang, remove_stopwords=remove_stopwords)
    num_unq = len(collections.Counter(words).keys())
    if num_unq == 0:
        num_unq = 10**-10
    return math.log(math.log(num_unq))/math.log(math.log(len(words)))*100


def root_type_token_ratio(documents: list, lang: str = 'en', remove_stopwords: bool = False) -> float:
    words = get_words(documents=documents, lang=lang, remove_stopwords=remove_stopwords)
    num_unq = len(collections.Counter(words).keys())
    return num_unq/(len(words)**0.5)*100
