import collections
from natasha import Segmenter, NewsSyntaxParser, Doc, NewsEmbedding
import spacy
from linguaf.descriptive_statistics import get_words, get_lexical_items


def lexical_density(documents: list, lang: str = 'en', remove_stopwords: bool = False) -> float:
    words = get_words(documents=documents, lang=lang, remove_stopwords=remove_stopwords)
    lex_items = get_lexical_items(documents=documents, remove_stopwords=remove_stopwords, lang=lang)
    return len(lex_items)/len(words)*100


def type_toke_ratio(documents: list, lang: str = 'en', remove_stopwords: bool = False) -> float:
    words = get_words(documents=documents, lang=lang, remove_stopwords=remove_stopwords)
    num_unq = len(collections.Counter(words).keys())
    return num_unq/len(words)*100


def mean_dependency_distance(documents: list, lang: str = 'en') -> float:
    segmenter = Segmenter()
    emb = NewsEmbedding()
    syntax_parser = NewsSyntaxParser(emb)
    nlp = spacy.load("en_core_web_sm")

    mdds = list()
    for text in documents:
        dd = 0
        if lang == 'ru':
            doc = Doc(text)
            doc.segment(segmenter)
            doc.parse_syntax(syntax_parser)
            for t in doc.tokens:
                dd += abs(int(t.head_id.split('_')[1]) - int(t.id.split('_')[1]))
            mdd = dd/(len(doc.tokens) - 1)
        elif lang == 'en':
            doc = nlp(text)
            for token in doc:
                dd += abs(token.head.i - token.i)
            mdd = dd/(len(doc) - 1)
        mdds.append(mdd)

    return sum(mdds)/len(mdds)
