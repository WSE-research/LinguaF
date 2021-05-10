import json
from razdel import tokenize
from collections import Counter
import syllables
import rusyllab
from nltk import word_tokenize, pos_tag
import pymorphy2
import nltk
import spacy
from natasha import Segmenter, NewsSyntaxParser, Doc, NewsEmbedding, NamesExtractor, MorphVocab

# TODO: while installing
nltk.download('averaged_perceptron_tagger')
nltk.download("stopwords")  # TODO: get own stopwords

SUPPORTED_LANGUAGES = ['en', 'ru']  # https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes


def check_params(f):
    def helper(self, documents, lang):
        if lang not in SUPPORTED_LANGUAGES:
            raise Exception(f"Language {lang} is not supported. Supported languages are {SUPPORTED_LANGUAGES}")
        if type(documents) != list:
            raise Exception(f"The documents parameter has to be list. Now: {type(documents)}")
        return f(self, documents, lang)
    return helper

# TODO: add word count, char count, sentence count etc.
class LinguisticMeasures:

    def __init__(self, remove_stopwords=False):
        self.REMOVE_STOPWORDS = remove_stopwords
        self.segmenter = Segmenter()
        self.emb = NewsEmbedding()
        self.morph_vocab = MorphVocab()
        self.syntax_parser = NewsSyntaxParser(self.emb)
        self.names_extractor = NamesExtractor(self.morph_vocab)

        self.morph = pymorphy2.MorphAnalyzer()
        self.nlp = spacy.load("en_core_web_sm")

        self.stopwords = dict()
        self.stopwords['ru'] = nltk.corpus.stopwords.words("russian")
        self.stopwords['en'] = nltk.corpus.stopwords.words("english")

    def set_remove_stopwords(self, remove_stopwords=False):
        self.REMOVE_STOPWORDS = remove_stopwords

    @check_params
    def get_num_of_lex_items(self, documents, lang='en'):
        # TODO: return list of lex items
        # TODO: refactor to make it shorter
        """
        Lexical items are: nouns, adjectives, verbs, adverbs
        """
        cnt = 0
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
            if lang == 'ru':
                if self.REMOVE_STOPWORDS:
                    stopwords = self.stopwords['ru']
                    tokens = [t.text for t in list(tokenize(doc)) if len(t.text) > 1 and t.text.lower() not in stopwords]
                else:
                    tokens = [t.text for t in list(tokenize(doc)) if len(t.text) > 1]

                tags = [self.morph.parse(token)[0].tag.POS for token in tokens]

                for tag in tags:
                    if tag in morphy_tags:
                        cnt += 1
            elif lang == 'en':
                if self.REMOVE_STOPWORDS:
                    stopwords = self.stopwords['en']
                    tags = pos_tag([t for t in word_tokenize(doc) if len(t) > 1 and t.lower() not in stopwords])
                else:
                    tags = pos_tag([t for t in word_tokenize(doc) if len(t) > 1])

                for tag in tags:
                    if tag[1] in nltk_tags:
                        cnt += 1

        return cnt

    @check_params
    def get_words(self, documents, lang='en'):
        words = list()

        for doc in documents:
            if lang == 'ru':
                tokens = list(tokenize(doc))

                if self.REMOVE_STOPWORDS:
                    stopwords = self.stopwords['ru']
                    cur_words = [t.text for t in tokens if len(t.text) > 1 and t.text.lower() not in stopwords]
                else:
                    cur_words = [t.text for t in tokens if len(t.text) > 1]
            elif lang == 'en':
                tokens = word_tokenize(doc)

                if self.REMOVE_STOPWORDS:
                    stopwords = self.stopwords['en']
                    cur_words = [t for t in tokens if len(t) > 1 and t.lower() not in stopwords]
                else:
                    cur_words = [t for t in tokens if len(t) > 1]

            words += cur_words  # add retrieved tokens from a question to a global words list

        if len(words) == 0:
            raise Exception(f"No words found in the documents: {documents}.")

        return words

    @staticmethod
    @check_params
    def get_syllable_count(word_list, lang='en'):
        syl_count = 0

        for word in word_list:
            if lang == 'ru':
                syl_count += len(rusyllab.split_word(word))
            elif lang == 'en':
                syl_count += syllables.estimate(word)

        return syl_count

    @check_params
    def flesh_reading_ease(self, documents, lang='en'):
        words = self.get_words(documents, lang)
        syl_total = self.get_syllable_count(words, lang)

        if lang == 'en':
            return 206.835 - 1.015*(len(words)/len(documents)) - 84.6*(syl_total/len(words))
        elif lang == 'ru':
            return 206.835 - 1.52*(len(words)/len(documents)) - 65.14*(syl_total/len(words))  # coefficients for russian

    @check_params
    def lexical_density(self, documents, lang='en'):
        words = self.get_words(documents, lang)
        lex_items = self.get_num_of_lex_items(documents, lang)

        return lex_items/len(words)

    @check_params
    def type_toke_ratio(self, documents, lang='en'):
        words = self.get_words(documents, lang)
        num_unq = len(Counter(words).keys())

        return num_unq / len(words)

    @check_params
    def calculate_mean_dependency_distance(self, documents, lang='en'):
        mdds = list()
        for text in documents:
            dd = 0
            if lang == 'ru':
                doc = Doc(text)
                doc.segment(self.segmenter)
                doc.parse_syntax(self.syntax_parser)
                for t in doc.tokens:
                    dd += abs(int(t.head_id.split('_')[1]) - int(t.id.split('_')[1]))
                mdd = dd/(len(doc.tokens)-1)
            elif lang == 'en':
                doc = self.nlp(text)
                for token in doc:
                    dd += abs(token.head.i - token.i)
                mdd = dd/(len(doc) - 1)
            mdds.append(mdd)

        return sum(mdds)/len(mdds)
