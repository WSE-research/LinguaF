import os
import re
import pathlib
import string
import pyphen
import pymorphy2
from nltk import word_tokenize, pos_tag
import collections
from linguaf import SUPPORTED_LANGS, __load_json, __check_bool_param, __check_documents_param, __check_lang_param, \
    __check_text_param, __check_words_param


PUNCTUATION = r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~—«»"""
STOPWORDS = dict()


for language in SUPPORTED_LANGS:
    STOPWORDS[language] = __load_json(
        os.path.join(pathlib.Path(__file__).parent.absolute(),
                     "resources",
                     "stopwords",
                     f"{language}.json")
    )


def remove_punctuation(text: str) -> str:
    """Remove punctuation from text string.

    Keyword arguments:
    text -- the string from which the punctuation is removed
    """
    __check_text_param(text)

    return ''.join(ch for ch in text if ch not in PUNCTUATION)


def remove_digits(text: str) -> str:
    """Remove digits from text string.

    Keyword arguments:
    text -- the string from which the digits are removed
    """
    __check_text_param(text)

    return ''.join(ch for ch in text if ch not in string.digits)


def char_count(documents: list, ignore_spaces: bool = True) -> int:
    """Count characters in a list of documents.

    Keyword arguments:
    documents -- list of textual documents.
    ignore_spaces -- boolean flag that shows if we should ignore spaces
    """
    __check_documents_param(documents)
    __check_bool_param(ignore_spaces)

    text = str()
    for doc in documents:
        text += doc
    if ignore_spaces:
        text = text.replace(" ", "")
    return len(text)


def letter_count(documents: list, ignore_spaces: bool = True, ignore_digits: bool = True) -> int:
    """Count letters in a list of documents

    Keyword arguments:
    documents -- list of textual documents.
    ignore_spaces -- boolean flag that shows if we should ignore spaces
    ignore_digits -- boolean flag that shows if we should ignore digits
    """
    __check_documents_param(documents)
    __check_bool_param(ignore_spaces)
    __check_bool_param(ignore_digits)

    text = str()
    for doc in documents:
        text += doc
    if ignore_spaces:
        text = text.replace(" ", "")
    if ignore_digits:
        text = remove_digits(text)
    return len(remove_punctuation(text))


def punctuation_count(documents: list) -> int:
    """Count number of punctuation characters in a list of textual documents

    Keyword arguments:
    documents -- the list of textual documents.
    """
    __check_documents_param(documents)

    char_cnt = char_count(documents, ignore_spaces=True)
    char_wo_punctuation = letter_count(documents, ignore_spaces=True, ignore_digits=False)
    return char_cnt - char_wo_punctuation


def digit_count(documents: list) -> int:
    """Count number of digits in a list of textual documents

    Keyword arguments:
    documents -- the list of textual documents.
    """
    __check_documents_param(documents)
    letters_w_digits = letter_count(documents, ignore_spaces=False, ignore_digits=False)
    letters_wo_digits = letter_count(documents, ignore_spaces=False, ignore_digits=True)
    return letters_w_digits - letters_wo_digits


def syllable_count(words: list, lang: str = 'en') -> int:
    """Count number of syllables in a list of words

    Keyword arguments:
    words -- the list of words
    lang -- language of the words
    """
    __check_words_param(words)
    syl_count = 0
    dic = pyphen.Pyphen(lang=lang)  # TODO: match language
    for word in words:
        syl_count += len(dic.inserted(word).split('-'))
    return syl_count


def number_of_n_syllable_words(words: list, lang: str = 'en', n: tuple = (1, 2)) -> int:
    """Count number of words with x <= n < y syllable words in a list of words

    Keyword arguments:
    words -- the list of words
    lang -- language of the words
    n -- tuple: (x, y)
    """
    __check_words_param(words)
    __check_lang_param(lang)
    if n[0] < 1 or n[1] <= n[0]:
        raise ValueError(f"The given n parameter isn't correct: {n}. n=tuple(x,y), x>0, y>x.")

    count = 0
    dic = pyphen.Pyphen(lang=lang)  # TODO: match language
    for word in words:
        syl_cnt = len(dic.inserted(word).split('-'))
        for i in n:
            if syl_cnt == i:
                count += 1
    return count


def get_words(documents: list, lang: str = 'en', remove_stopwords: bool = False) -> list:
    """Create list of words based on a list of textual documents.

    Keyword arguments:
    documents -- the list of textual documents
    lang -- language of the words
    remove_stopwords -- boolean flag that shows if the function should exclude stopwords
    """
    __check_documents_param(documents)
    __check_lang_param(lang)
    __check_bool_param(remove_stopwords)

    words = list()

    for doc in documents:
        tokens = tokenize(doc, remove_stopwords=remove_stopwords, lang=lang)
        # add retrieved tokens from a question to a global words list
        words += [t for t in tokens if len(remove_punctuation(t)) > 0]
    if len(words) == 0:
        raise Exception(f"No words found in the documents: {documents}.")

    return words


def tokenize(text: str, remove_stopwords: bool = False, lang: str = 'en') -> list:
    """Create list of tokens based on a list of textual documents.

    Keyword arguments:
    documents -- the list of textual documents
    lang -- language of the words
    remove_stopwords -- boolean flag that shows if the function should exclude stopwords
    """
    __check_text_param(text)
    __check_lang_param(lang)
    __check_bool_param(remove_stopwords)

    stopwords = STOPWORDS[lang]
    if remove_stopwords:
        tokens = [t for t in word_tokenize(text) if len(t) > 0 and t.lower() not in stopwords]
    else:
        tokens = [t for t in word_tokenize(text) if len(t) > 0]
    return tokens


def avg_syllable_per_word(documents: list, lang: str = 'en', remove_stopwords: bool = False) -> float:
    """Count average number of syllables per word based on a list of textual documents.

    Keyword arguments:
    documents -- the list of textual documents
    lang -- language of the words
    remove_stopwords -- boolean flag that shows if the function should exclude stopwords
    """
    __check_documents_param(documents)
    __check_lang_param(lang)
    __check_bool_param(remove_stopwords)

    words = get_words(documents, lang, remove_stopwords=remove_stopwords)
    syl_count = syllable_count(words, lang)
    return syl_count / len(words)


def sentence_count(documents: list) -> int:
    """Count number of sentences in a list of textual documents

    Keyword arguments:
    documents -- the list of textual documents.
    """
    __check_documents_param(documents)
    cnt = 0
    for doc in documents:
        sent_cnt = len([t for t in re.split(r'[.!?\.]+', doc) if len(t) > 0])
        if len(doc) > 0 and sent_cnt == 0:
            cnt += 1
        else:
            cnt += sent_cnt
    return cnt


def get_sentences(documents: list) -> list:
    """Convert a list of textual documents into a list of sentences.

    Keyword arguments:
    documents -- the list of textual documents.
    """
    __check_documents_param(documents)

    sentences = list()
    for doc in documents:
        sentences += [t for t in re.split(r'[.!?\.]+', doc) if len(t) > 0]
    return sentences


def avg_word_length(documents: list, lang: str = 'en', remove_stopwords: bool = False) -> float:
    """Count average word length based on a list of textual documents.

    Keyword arguments:
    documents -- the list of textual documents
    lang -- language of the words
    remove_stopwords -- boolean flag that shows if the function should exclude stopwords
    """
    __check_documents_param(documents)
    __check_lang_param(lang)
    __check_bool_param(remove_stopwords)

    words = get_words(documents, lang, remove_stopwords=remove_stopwords)
    char_cnt = char_count(documents)
    return char_cnt/len(words)


def avg_sentence_length(documents: list, ignore_spaces: bool = True) -> float:
    """Count average sentence length in a list of documents.

    Keyword arguments:
    documents -- list of textual documents.
    ignore_spaces -- boolean flag that shows if we should ignore spaces
    """
    __check_documents_param(documents)
    __check_bool_param(ignore_spaces)

    return char_count(documents, ignore_spaces)/sentence_count(documents)


def get_ngrams(
        documents: list,
        n: int = 1,
        lang: str = 'en',
        remove_stopwords: bool = True,
        output_count: bool = True
) -> list:
    """Retrieve a list of ngrams based on a list of textual documents.

    Keyword arguments:
    documents -- the list of textual documents
    n -- the "n" parameter in "ngram"
    lang -- language of the words
    remove_stopwords -- boolean flag that shows if the function should exclude stopwords
    output_count -- boolean flag that shows if the function should return ngram occurrences
    """
    __check_documents_param(documents)
    __check_lang_param(lang)
    __check_bool_param(remove_stopwords)
    __check_bool_param(output_count)
    if n < 1:
        raise ValueError(f"The n parameter should be more than 0. Got: {n}")

    words = get_words(documents, lang, remove_stopwords=remove_stopwords)
    ngrams = list()
    for i in range(0, len(words), 1):
        if i + n <= len(words):
            ngrams.append(' '.join(word for word in words[i:i+n]).lower())
    if output_count:
        return collections.Counter(ngrams).most_common()
    return ngrams


def get_lexical_items(documents: list, remove_stopwords: bool = False, lang: str = 'en') -> list:
    """Retrieve a list of lexical items (types) based on a list of textual documents.
    Lexical items (types) are: nouns, adjectives, verbs, adverbs

    Keyword arguments:
    documents -- the list of textual documents
    lang -- language of the words
    remove_stopwords -- boolean flag that shows if the function should exclude stopwords
    """
    __check_documents_param(documents)
    __check_lang_param(lang)
    __check_bool_param(remove_stopwords)

    morph = pymorphy2.MorphAnalyzer()

    lex_items = list()
    nltk_tags = [
        'NN', 'NNS', 'NNP', 'NNPS',
        'JJ', 'JJR', 'JJS',
        'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ',
        'RB', 'RBR', 'RBS'
    ]
    morphy_tags = [
        'NOUN', 'ADJF', 'ADJS', 'VERB', 'INFN', 'ADVB'
    ]

    for doc in documents:
        tokens = tokenize(text=doc, remove_stopwords=remove_stopwords, lang=lang)
        if lang == 'ru':
            tags = [morph.parse(token)[0].tag.POS for token in tokens]

            for i in range(len(tags)):
                if tags[i] in morphy_tags:
                    lex_items.append((tokens[i], tags[i]))
        elif lang == 'en':
            tags = pos_tag(tokens)

            for i in range(len(tags)):
                if tags[i][1] in nltk_tags:
                    lex_items.append((tokens[i], tags[i][1]))
    return lex_items


def words_per_sentence(documents: list, lang: str = 'en', remove_stopwords: bool = False) -> list:
    """Calculate average number of words in a sentence based on a list of documents.

    Keyword arguments:
    documents -- the list of textual documents
    lang -- language of the words
    remove_stopwords -- boolean flag that shows if the function should exclude stopwords
    """
    __check_documents_param(documents)
    __check_lang_param(lang)
    __check_bool_param(remove_stopwords)

    words = get_words(documents, lang, remove_stopwords)
    return len(words)/sentence_count(documents)
