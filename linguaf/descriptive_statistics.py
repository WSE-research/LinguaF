import os
import re
import pathlib
import json
import string
import pyphen
from nltk import word_tokenize


def __load_json(filepath):
    data = None
    with open(filepath) as f:
        data = json.load(f)
    return data


STOPWORDS = dict()
STOPWORDS['ru'] = __load_json(
            os.path.join(pathlib.Path(__file__).parent.absolute(),
                         "resources",
                         "stopwords-russian.json")
        )
STOPWORDS['en'] = __load_json(
    os.path.join(pathlib.Path(__file__).parent.absolute(),
                 "resources",
                 "stopwords-english.json")
)


def remove_punctuation(text):
    return ''.join(ch for ch in text if ch not in string.punctuation)


def remove_digits(text):
    return ''.join(ch for ch in text if ch not in string.digits)


def char_count(documents, ignore_spaces=True):
    text = str()
    for doc in documents:
        text += doc
    if ignore_spaces:
        text = text.replace(" ", "")
    return len(text)


def letter_count(documents, ignore_spaces=True, ignore_digits=True):
    text = str()
    for doc in documents:
        text += doc
    if ignore_spaces:
        text = text.replace(" ", "")
    if ignore_digits:
        text = remove_digits(text)
    return len(remove_punctuation(text))


def punctuation_count(documents):
    char_cnt = char_count(documents, ignore_spaces=True)
    char_wo_punctuation = letter_count(documents, ignore_spaces=True, ignore_digits=False)
    return char_cnt - char_wo_punctuation


def digit_count(documents):
    letters_w_digits = letter_count(documents, ignore_spaces=False, ignore_digits=False)
    letters_wo_digits = letter_count(documents, ignore_spaces=False, ignore_digits=True)
    return letters_w_digits - letters_wo_digits


def syllable_count(words, lang='en'):
    syl_count = 0
    dic = pyphen.Pyphen(lang=lang)  # TODO: match language
    for word in words:
        syl_count += len(dic.inserted(word).split('-'))
    return syl_count


def get_words(documents, lang='en'):
    words = list()

    for doc in documents:
        tokens = tokenize(doc, lang=lang)
        # add retrieved tokens from a question to a global words list
        words += [t for t in tokens if len(remove_punctuation(t)) > 0]
    if len(words) == 0:
        raise Exception(f"No words found in the documents: {documents}.")

    return words


def tokenize(document, remove_stopwords=False, lang='en'):
    stopwords = STOPWORDS[lang]
    if remove_stopwords:
        tokens = [t for t in word_tokenize(document) if len(t) > 0 and t.lower() not in stopwords]
    else:
        tokens = [t for t in word_tokenize(document) if len(t) > 0]
    return tokens


def avg_syllable_per_word(documents, lang='en'):
    words = get_words(documents, lang)
    syl_count = syllable_count(words, lang)
    return syl_count/len(words)


def sentence_count(documents):
    cnt = 0
    for doc in documents:
        sent_cnt = len([t for t in re.split(r'[.!?\.]+', doc) if len(t) > 0])
        if len(doc) > 0 and sent_cnt == 0:
            cnt += 1
        else:
            cnt += sent_cnt
    return cnt


def avg_word_length(documents, lang='en'):
    words = get_words(documents, lang)
    char_cnt = char_count(documents)
    return char_cnt/words


def avg_sentence_length(documents, ignore_spaces=True):
    return char_count(documents, ignore_spaces)/sentence_count(documents)


def word_frequency(documents, lang='en'):
    # TODO
    pass
