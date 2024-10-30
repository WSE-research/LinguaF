import stopwordsiso
import logging
import os
import re
import pathlib
import string
import pyphen
import spacy
from spacy.lang.de.examples import sentences
from spacy.cli.download import download
import pymorphy3
from nltk import word_tokenize, pos_tag
import nltk
import collections
from linguaf import SUPPORTED_LANGS, __load_json, __check_bool_param, __check_documents_param, __check_lang_param, \
    __check_text_param, __check_words_param

LOGGER = logging.getLogger(__name__)

try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('taggers/averaged_perceptron_tagger')
except:
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')

PUNCTUATION = r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~—«»"""
STOPWORDS = dict()

for language in SUPPORTED_LANGS:
    try:
        # TODO: consider using nltk directly
        # get stopwords from local files 
        STOPWORDS[language] = __load_json(
            os.path.join(pathlib.Path(__file__).parent.absolute(),
                         "resources",
                         "stopwords",
                         f"{language}.json")
        )
        LOGGER.debug(f"Reading stopwords for language \"{language}\" from local file")
    except FileNotFoundError as e:
        # get stopwords from stopwordsiso lib
        if stopwordsiso.has_lang(language):
            LOGGER.debug(f"No local stopword file found for language \"{language}\"")
            STOPWORDS[language] = stopwordsiso.stopwords(language)
            LOGGER.debug(f"Reading stopwords for language \"{language}\" from stopwordsiso library")
        else:
            raise Exception(f"No stopwords could be found for language \"{language}\"")


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
    __check_lang_param(lang)

    unsupported_langs = ['zh', 'hy']
    if lang in unsupported_langs:
        raise ValueError(f"Syllable counting is currently not supported for the language " + lang + "!")
        # TODO: chinese does have syllables! so this should be supported eventually
        # however, chinese does not support hyphenation, so the implementation below does not work for it

    syl_count = 0
    dic = pyphen.Pyphen(lang=lang)  # TODO: match language
    for word in words:
        syl_count += len(dic.inserted(word).split('-'))
    return syl_count


def number_of_n_syllable_words(documents: list, lang: str = 'en', n: tuple = (1, 2), remove_stopwords=False) -> int:
    """Count number of words with x <= n < y syllable words in a list of words

    Keyword arguments:
    documents -- the list of documents
    lang -- language of the words
    n -- tuple: (x, y)
    """
    __check_documents_param(documents)
    __check_lang_param(lang)

    counts = number_of_n_syllable_words_all(documents, lang, remove_stopwords)
    count = 0
    for i in range(n[0], n[1]):
        count += counts.get(i, 0)
    return count


def number_of_n_syllable_words_all(documents: list, lang: str = 'en', remove_stopwords: bool = False) -> dict:
    """Count each found number of syllables in a list of words.

    Keyword arguments:
    documents -- the list of documents
    lang -- language of the words
    """
    __check_documents_param(documents)
    __check_lang_param(lang)

    # TODO: refactor duplicate code!
    unsupported_langs = ['zh', 'hy']
    if lang in unsupported_langs:
        raise ValueError(f"Syllable counting is currently not supported for the language " + lang + "!")
        # TODO: chinese does have syllables! so this should be supported eventually
        # however, chinese does not support hyphenation, so the implementation below does not work for it!

    words = get_words(documents, lang, remove_stopwords)

    counts = collections.defaultdict(int)
    dic = pyphen.Pyphen(lang=lang)  # TODO: match language
    for word in words:
        syl_cnt = len(dic.inserted(word).split('-'))
        counts[syl_cnt] += 1
    return counts


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

    morph = pymorphy3.MorphAnalyzer()

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
    spacy_tags = [
        # TODO: do we want punct tags? 
        'NOUN', 'AUX', 'PROPN', 'DET', 'PRON', 'ADV', 'ADP', 'VERB', 'ADJ', 'INTJ', 'PART', 'SCONJ'
    ]

    # TODO: use spacy for other languages 
    for doc in documents:
        tokens = tokenize(text=doc, remove_stopwords=remove_stopwords, lang=lang)
        if lang == 'ru':
            tags = [morph.parse(token)[0].tag.POS for token in tokens]

            for i in range(len(tags)):
                if tags[i] in morphy_tags:
                    lex_items.append((tokens[i], tags[i]))
        elif lang == 'uk':
            tags = [morph.parse(token)[0].tag.POS for token in tokens]

            for i in range(len(tags)):
                if tags[i] in morphy_tags:
                    lex_items.append((tokens[i], tags[i]))
        elif lang == 'en':
            tags = pos_tag(tokens)

            for i in range(len(tags)):
                if tags[i][1] in nltk_tags:
                    lex_items.append((tokens[i], tags[i][1]))
        elif lang == 'de':
            nlp = load_spacy_language_model('de_core_news_sm')
            #nlp.tokenizer = nlp.tokenizer.tokens_from_list
            # TODO: always use comparison to predefined tags? 
            # TODO: this does not used the pre-tokenized sentence!
            tags = nlp(doc)
            for tag in tags:
                if tag.pos_ in spacy_tags:
                    lex_items.append((tag.text, tag.pos_))
        elif lang == 'fr':
            nlp = load_spacy_language_model('fr_core_news_sm')
            tags = nlp(doc)
            for tag in tags:
                if tag.pos_ in spacy_tags:
                    lex_items.append((tag.text, tag.pos_))
        elif lang == 'es':
            nlp = load_spacy_language_model('es_core_news_sm')
            tags = nlp(doc)
            for tag in tags:
                if tag.pos_ in spacy_tags:
                    lex_items.append((tag.text, tag.pos_))
        elif lang == 'zh':
            nlp = load_spacy_language_model('zh_core_web_sm')
            tags = nlp(doc)
            for tag in tags:
                if tag.pos_ in spacy_tags:
                    lex_items.append((tag.text, tag.pos_))
        elif lang == 'lt':
            nlp = load_spacy_language_model('lt_core_news_sm')
            tags = nlp(doc)
            for tag in tags:
                if tag.pos_ in spacy_tags:
                    lex_items.append((tag.text, tag.pos_))
        else:
            raise ValueError(f"POS tagging is currently not supported for language \"{lang}\"!")
    return lex_items


def load_spacy_language_model(model: str):
    try:
        nlp = spacy.load(model)
    except OSError:
        LOGGER.info('Could not find language model "' + model + '".\n'
            'Downloading language model for the spaCy POS tagger\n')
        download(model)
        nlp = spacy.load(model)
    return nlp


def avg_words_per_sentence(documents: list, lang: str = 'en', remove_stopwords: bool = False) -> list:
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
