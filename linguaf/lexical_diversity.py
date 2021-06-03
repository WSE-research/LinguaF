import collections
import math
from linguaf.descriptive_statistics import get_words, get_lexical_items
from linguaf import __check_bool_param, __check_documents_param, __check_lang_param


def lexical_density(documents: list, lang: str = 'en', remove_stopwords: bool = False) -> float:
    """Calculates lexical density based on a list of documents.
    Lexical density is the ratio between number of lexical items and number of words in total.
    See Wikipedia article: https://en.wikipedia.org/wiki/Lexical_density

    Keyword arguments:
    documents -- the list of textual documents
    lang -- language of the textual documents
    remove_stopwords -- boolean flag that shows if the function should exclude stopwords
    """
    __check_documents_param(documents)
    __check_lang_param(lang)
    __check_bool_param(remove_stopwords)

    words = get_words(documents=documents, lang=lang, remove_stopwords=remove_stopwords)
    lex_items = get_lexical_items(documents=documents, remove_stopwords=remove_stopwords, lang=lang)
    return len(lex_items)/len(words)*100


def type_token_ratio(documents: list, lang: str = 'en', remove_stopwords: bool = False) -> float:
    """Calculates Type-Token Ratio based on a list of documents.
    Types -- are unique words, Tokens (in this context) -- are words in total.
    See Wikipedia article: https://de.wikipedia.org/wiki/Type-Token-Relation

    Keyword arguments:
    documents -- the list of textual documents
    lang -- language of the textual documents
    remove_stopwords -- boolean flag that shows if the function should exclude stopwords
    """
    __check_documents_param(documents)
    __check_lang_param(lang)
    __check_bool_param(remove_stopwords)

    words = get_words(documents=documents, lang=lang, remove_stopwords=remove_stopwords)
    num_unq = len(collections.Counter(words).keys())
    return num_unq/len(words)


def log_type_token_ratio(documents: list, lang: str = 'en', remove_stopwords: bool = False) -> float:
    """Calculates Log Type-Token Ratio (Herdan's Constant) based on a list of documents.
    Types -- are unique words, Tokens (in this context) -- are words in total.
    Publicaiton: Herdan, 1960, as cited in Tweedie & Baayen, 1998

    Keyword arguments:
    documents -- the list of textual documents
    lang -- language of the textual documents
    remove_stopwords -- boolean flag that shows if the function should exclude stopwords
    """
    __check_documents_param(documents)
    __check_lang_param(lang)
    __check_bool_param(remove_stopwords)

    words = get_words(documents=documents, lang=lang, remove_stopwords=remove_stopwords)
    num_unq = len(collections.Counter(words).keys())
    return math.log(num_unq)/math.log(len(words)) if len(words) != 1 else 0


def summer_index(documents: list, lang: str = 'en', remove_stopwords: bool = False) -> float:
    """Calculates Summer's Index based on a list of documents.
    The index is the same as Double Log Type-Token Ratio.

    Keyword arguments:
    documents -- the list of textual documents
    lang -- language of the textual documents
    remove_stopwords -- boolean flag that shows if the function should exclude stopwords
    """
    __check_documents_param(documents)
    __check_lang_param(lang)
    __check_bool_param(remove_stopwords)

    words = get_words(documents=documents, lang=lang, remove_stopwords=remove_stopwords)
    num_unq = len(collections.Counter(words).keys())
    if num_unq == 0:
        num_unq = 10**-10
    return math.log(math.log(num_unq))/math.log(math.log(len(words))) if len(words) != 1 else 0


def root_type_token_ratio(documents: list, lang: str = 'en', remove_stopwords: bool = False) -> float:
    """Calculates Root Type-Token Ratio based on a list of documents.
    Publication: Guiraud, 1954. Also cited in Tweedie & Baayen, 1998

    Keyword arguments:
    documents -- the list of textual documents
    lang -- language of the textual documents
    remove_stopwords -- boolean flag that shows if the function should exclude stopwords
    """
    __check_documents_param(documents)
    __check_lang_param(lang)
    __check_bool_param(remove_stopwords)

    words = get_words(documents=documents, lang=lang, remove_stopwords=remove_stopwords)
    num_unq = len(collections.Counter(words).keys())
    return num_unq/(len(words)**0.5)
