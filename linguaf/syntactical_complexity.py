from linguaf.descriptive_statistics import get_sentences, get_words
from linguaf import __check_documents_param, __check_lang_param
from natasha import Segmenter, NewsSyntaxParser, Doc, NewsEmbedding
import spacy


def mean_dependency_distance(documents: list, lang: str = 'en') -> float:
    """Calculates Mean Dependency Distance score over a list of documents
    The higher the score the more complex are the sentences.

    Keyword arguments:
    documents -- the list of textual documents
    lang -- language of the textual documents
    """
    __check_documents_param(documents)
    __check_lang_param(lang)

    dd = 0
    sentences = get_sentences(documents)
    words = get_words(documents, lang)

    for text in sentences:

        if lang == 'ru':
            segmenter = Segmenter()
            emb = NewsEmbedding()
            syntax_parser = NewsSyntaxParser(emb)
            doc = Doc(text)
            doc.segment(segmenter)
            doc.parse_syntax(syntax_parser)
            for t in doc.tokens:
                dd += abs(int(t.head_id.split('_')[1]) - int(t.id.split('_')[1]))
                
        elif lang == 'en':
            try:
                nlp = spacy.load("en_core_web_sm")
            except:
                spacy.cli.download('en_core_web_sm')  # required for english language
                nlp = spacy.load("en_core_web_sm")

            doc = nlp(text)
            for token in doc:
                dd += abs(token.head.i - token.i)
        else:
            raise ValueError("Syllable counting is currently not supported for the language " + lang + "!")

    return dd/(len(words) - len(sentences))
