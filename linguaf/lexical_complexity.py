from linguaf.descriptive_statistics import get_sentences
from natasha import Segmenter, NewsSyntaxParser, Doc, NewsEmbedding
import spacy


def mean_dependency_distance(documents: list, lang: str = 'en') -> float:
    """Calculates Mean Dependency Distance score over a list of documents
    The higher the score the more complex are the sentences.

    Keyword arguments:
    documents -- the list of textual documents
    lang -- language of the textual documents
    """
    segmenter = Segmenter()
    emb = NewsEmbedding()
    syntax_parser = NewsSyntaxParser(emb)
    nlp = spacy.load("en_core_web_sm")

    mdds = list()
    sentences = get_sentences(documents)

    for text in sentences:
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
