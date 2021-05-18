import os
import re
import pathlib
import json
import string
import pyphen
import pymorphy2
from nltk import word_tokenize, pos_tag
import collections


PUNCTUATION = r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~—«»"""


def __load_json(filepath):
    data = None
    with open(filepath) as f:
        data = json.load(f)
    return data


SUPPORTED_LANGS = ['en', 'ru']
STOPWORDS = dict()

for language in SUPPORTED_LANGS:
    STOPWORDS[language] = __load_json(
        os.path.join(pathlib.Path(__file__).parent.absolute(),
                     "resources",
                     "stopwords",
                     f"{language}.json")
    )


def remove_punctuation(text: str) -> str:
    return ''.join(ch for ch in text if ch not in PUNCTUATION)


def remove_digits(text: str) -> str:
    return ''.join(ch for ch in text if ch not in string.digits)


def char_count(documents: list, ignore_spaces: bool = True) -> int:
    text = str()
    for doc in documents:
        text += doc
    if ignore_spaces:
        text = text.replace(" ", "")
    return len(text)


def letter_count(documents: list, ignore_spaces: bool = True, ignore_digits: bool = True) -> int:
    text = str()
    for doc in documents:
        text += doc
    if ignore_spaces:
        text = text.replace(" ", "")
    if ignore_digits:
        text = remove_digits(text)
    return len(remove_punctuation(text))


def punctuation_count(documents: list) -> int:
    char_cnt = char_count(documents, ignore_spaces=True)
    char_wo_punctuation = letter_count(documents, ignore_spaces=True, ignore_digits=False)
    return char_cnt - char_wo_punctuation


def digit_count(documents: list) -> int:
    letters_w_digits = letter_count(documents, ignore_spaces=False, ignore_digits=False)
    letters_wo_digits = letter_count(documents, ignore_spaces=False, ignore_digits=True)
    return letters_w_digits - letters_wo_digits


def syllable_count(words: list, lang: str = 'en') -> int:
    syl_count = 0
    dic = pyphen.Pyphen(lang=lang)  # TODO: match language
    for word in words:
        syl_count += len(dic.inserted(word).split('-'))
    return syl_count


def get_words(documents: list, lang: str = 'en', remove_stopwords: bool = False) -> list:
    words = list()

    for doc in documents:
        tokens = tokenize(doc, remove_stopwords=remove_stopwords, lang=lang)
        # add retrieved tokens from a question to a global words list
        words += [t for t in tokens if len(remove_punctuation(t)) > 0]
    if len(words) == 0:
        raise Exception(f"No words found in the documents: {documents}.")

    return words


def tokenize(document: str, remove_stopwords: bool = False, lang: str = 'en') -> list:
    stopwords = STOPWORDS[lang]
    if remove_stopwords:
        tokens = [t for t in word_tokenize(document) if len(t) > 0 and t.lower() not in stopwords]
    else:
        tokens = [t for t in word_tokenize(document) if len(t) > 0]
    return tokens


def avg_syllable_per_word(documents: list, lang: str = 'en', remove_stopwords: bool = False) -> float:
    words = get_words(documents, lang, remove_stopwords=remove_stopwords)
    syl_count = syllable_count(words, lang)
    return syl_count / len(words)


def sentence_count(documents: list) -> int:
    cnt = 0
    for doc in documents:
        sent_cnt = len([t for t in re.split(r'[.!?\.]+', doc) if len(t) > 0])
        if len(doc) > 0 and sent_cnt == 0:
            cnt += 1
        else:
            cnt += sent_cnt
    return cnt


def avg_word_length(documents: list, lang: str = 'en', remove_stopwords: bool = False) -> float:
    words = get_words(documents, lang, remove_stopwords=remove_stopwords)
    char_cnt = char_count(documents)
    return char_cnt/words


def avg_sentence_length(documents: list, ignore_spaces: bool = True) -> float:
    return char_count(documents, ignore_spaces) / sentence_count(documents)


def get_ngrams(
        documents: list,
        n: int = 1,
        lang: str = 'en',
        remove_stopwords: bool = True,
        output_count: bool = True
) -> list:
    words = get_words(documents, lang, remove_stopwords=remove_stopwords)
    ngrams = list()
    for i in range(0, len(words), 1):
        if i + n <= len(words):
            ngrams.append(' '.join(word for word in words[i:i+n]).lower())
    if output_count:
        return collections.Counter(ngrams).most_common()
    return ngrams


def get_lexical_items(documents, remove_stopwords=False, lang='en'):
    """
    Lexical items are: nouns, adjectives, verbs, adverbs
    """
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
        tokens = tokenize(document=doc, remove_stopwords=remove_stopwords, lang=lang)
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
