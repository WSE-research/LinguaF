import json
from collections import Counter
import pyphen
from nltk import word_tokenize, pos_tag
import pymorphy2
import nltk
import spacy
import string
import re
from natasha import Segmenter, NewsSyntaxParser, Doc, NewsEmbedding
import pathlib
import os

# TODO: check documents static
# TODO: while installing
nltk.download('averaged_perceptron_tagger')

__SUPPORTED_LANGUAGES = ['en', 'ru']  # https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes


def check_documents(f):
    def helper(self, documents):
        if type(documents) != list:
            raise Exception(f"The documents parameter has to be list. Now: {type(documents)}")
        return f(self, documents)
    return helper


def check_params(f):
    def helper(self, documents, lang):
        if lang not in __SUPPORTED_LANGUAGES:
            raise Exception(f"Language {lang} is not supported. Supported languages are {__SUPPORTED_LANGUAGES}")
        if type(documents) != list:
            raise Exception(f"The documents parameter has to be list. Now: {type(documents)}")
        return f(self, documents, lang)
    return helper


def load_json(filepath):
    data = None
    with open(filepath) as f:
        data = json.load(f)
    return data


class LinguisticMeasures:

    def __init__(self, remove_stopwords=False):
        self.__REMOVE_STOPWORDS = remove_stopwords
        self.__segmenter = Segmenter()
        self.__emb = NewsEmbedding()
        # self.__morph_vocab = MorphVocab()
        self.__syntax_parser = NewsSyntaxParser(self.__emb)
        # self.names_extractor = NamesExtractor(self.__morph_vocab)

        self.__morph = pymorphy2.MorphAnalyzer()
        self.__nlp = spacy.load("en_core_web_sm")

        self.stopwords = dict()
        self.stopwords['ru'] = load_json(
            os.path.join(pathlib.Path(__file__).parent.absolute(),
                         "resources",
                         "stopwords-russian.json")
        )
        self.stopwords['en'] = load_json(
            os.path.join(pathlib.Path(__file__).parent.absolute(),
                         "resources",
                         "stopwords-english.json")
        )

    def set_remove_stopwords(self, remove_stopwords=False):
        self.__REMOVE_STOPWORDS = remove_stopwords

    def tokenize(self, document, lang='en'):
        stopwords = self.stopwords[lang]
        if self.__REMOVE_STOPWORDS:
            tokens = [t for t in word_tokenize(document) if len(t) > 0 and t.lower() not in stopwords]
        else:
            tokens = [t for t in word_tokenize(document) if len(t) > 0]
        return tokens

    @check_params
    def get_lexical_items(self, documents, lang='en'):
        """
        Lexical items are: nouns, adjectives, verbs, adverbs
        """
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
            tokens = self.tokenize(doc, lang)
            if lang == 'ru':
                tags = [self.__morph.parse(token)[0].tag.POS for token in tokens]

                for i in range(len(tags)):
                    if tags[i] in morphy_tags:
                        lex_items.append((tokens[i], tags[i]))
            elif lang == 'en':
                tags = pos_tag(tokens)

                for i in range(len(tags)):
                    if tags[i][1] in nltk_tags:
                        lex_items.append((tokens[i], tags[i][1]))
        return lex_items

    @check_params
    def get_words(self, documents, lang='en'):
        words = list()

        for doc in documents:
            tokens = self.tokenize(doc, lang=lang)
            # add retrieved tokens from a question to a global words list
            words += [t for t in tokens if len(self.remove_punctuation(t)) > 0]
        if len(words) == 0:
            raise Exception(f"No words found in the documents: {documents}.")

        return words

    @staticmethod
    def syllable_count(words, lang='en'):
        syl_count = 0
        dic = pyphen.Pyphen(lang=lang)  # TODO: create in constructor?
        for word in words:
            syl_count += len(dic.inserted(word).split('-'))
        return syl_count

    @check_params
    def flesh_reading_ease(self, documents, lang='en'):
        words = self.get_words(documents, lang)
        syl_total = self.syllable_count(words, lang)

        if lang == 'en':
            return 206.835 - 1.015*(len(words)/len(documents)) - 84.6*(syl_total/len(words))
        elif lang == 'ru':
            return 206.835 - 1.52*(len(words)/len(documents)) - 65.14*(syl_total/len(words))  # coefficients for russian

    @check_params
    def lexical_density(self, documents, lang='en'):
        words = self.get_words(documents, lang)
        lex_items = self.get_lexical_items(documents, lang)
        return len(lex_items)/len(words)*100

    @check_params
    def type_toke_ratio(self, documents, lang='en'):
        words = self.get_words(documents, lang)
        num_unq = len(Counter(words).keys())
        return num_unq/len(words)*100

    @check_params
    def mean_dependency_distance(self, documents, lang='en'):
        mdds = list()
        for text in documents:
            dd = 0
            if lang == 'ru':
                doc = Doc(text)
                doc.segment(self.__segmenter)
                doc.parse_syntax(self.__syntax_parser)
                for t in doc.tokens:
                    dd += abs(int(t.head_id.split('_')[1]) - int(t.id.split('_')[1]))
                mdd = dd/(len(doc.tokens)-1)
            elif lang == 'en':
                doc = self.__nlp(text)
                for token in doc:
                    dd += abs(token.head.i - token.i)
                mdd = dd/(len(doc) - 1)
            mdds.append(mdd)

        return sum(mdds)/len(mdds)

    @staticmethod
    def char_count(documents, ignore_spaces=True):
        text = str()
        for doc in documents:
            text += doc
        if ignore_spaces:
            text = text.replace(" ", "")
        return len(text)

    @staticmethod
    def remove_punctuation(text):
        return ''.join(ch for ch in text if ch not in string.punctuation)

    def letter_count(self, documents, ignore_spaces=True):
        text = str()
        for doc in documents:
            text += doc
        if ignore_spaces:
            text = text.replace(" ", "")
        return len(self.remove_punctuation(text))

    @staticmethod
    def sentence_count(documents):
        cnt = 0
        for doc in documents:
            sent_cnt = len([t for t in re.split(r'[.!?\.]+', doc) if len(t) > 0])
            if len(doc) > 0 and sent_cnt == 0:
                cnt += 1
            else:
                cnt += sent_cnt
        return cnt

    def avg_sentence_length(self, documents, ignore_spaces=True):
        return self.char_count(documents, ignore_spaces)/self.sentence_count(documents)

    @check_params
    def avg_syllables_per_word(self, documents, lang='en'):
        words = self.get_words(documents, lang)
        syl_count = self.syllable_count(words, lang)
        return syl_count/len(words)
