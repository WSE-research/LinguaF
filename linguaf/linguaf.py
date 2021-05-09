


SUPPORTED_LANGUAGES = ['en', 'ru'] # ISO-635.....

def check_language(f):
    def helper(documents, lang):
        if lang in SUPPORTED_LANGUAGES:
            return f(x)
        else:
            raise Exception(f"Language {lang} is not supported. Supported languages are {SUPPORTED_LANGUAGES}")
    return helper

class LinguisticMeasures:

    def __init__():
        self.REMOVE_STOPWORDS = False


    

@check_language
def get_num_of_lex_items(documents, lang='ru'):
    # TODO: move to commons
    # TODO: check if docs > 0
    # TODO: return list of lex items
    """
    Lexical items are: nouns, adjectives, verbs, adverbs
    """
    cnt = 0
    nltk_tags = [
        'NN','NNS','NNP','NNPS',
        'JJ', 'JJR', 'JJS',
        'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ',
        'RB', 'RBR', 'RBS'
    ]  
    morphy_tags = [
        'NOUN', 'ADJF', 'ADJS', 'VERB', 'INFN', 'ADVB'
    ]
    
    for text in documents:
        if lang == 'ru':
            if REMOVE_STOPWORDS:
                stopwords = russian_stopwords
                tokens = [t.text for t in list(tokenize(text)) if len(t.text) > 1 and t.text.lower() not in stopwords]
            else:
                tokens = [t.text for t in list(tokenize(text)) if len(t.text) > 1]
                
            tags = [morph.parse(token)[0].tag.POS for token in tokens]
            
            for tag in tags:
                if tag in morphy_tags:
                    cnt += 1
        elif lang == 'en':
            if REMOVE_STOPWORDS:
                stopwords = english_stopwords
                tags = pos_tag([t for t in word_tokenize(text) if len(t) > 1 and t.lower() not in stopwords])
            else:
                tags = pos_tag([t for t in word_tokenize(text) if len(t) > 1])
            
            for tag in tags:
                if tag[1] in nltk_tags:
                    cnt += 1
    
    return cnt

def get_words(documents, lang='en'):
    # TODO: move to commons
    # TODO: Exception: Language not supported, check if docs > 0, words > 0

    words = list()
    
    for doc in documents:
        if lang == 'ru':
            tokens = list(tokenize(text))
            
            if REMOVE_STOPWORDS:
                stopwords = russian_stopwords
                cur_words = [t.text for t in tokens if len(t.text) > 1 and t.text.lower() not in stopwords] 
            else:
                cur_words = [t.text for t in tokens if len(t.text) > 1] 
        elif lang == 'en':
            tokens = word_tokenize(text)
            
            if REMOVE_STOPWORDS:
                stopwords = english_stopwords
                cur_words = [t for t in tokens if len(t) > 1 and t.lower() not in stopwords] 
            else:
                cur_words = [t for t in tokens if len(t) > 1]
            
        words += cur_words # add retrieved tokens from a question to a global words list
    
    return words

def get_syllable_count(word_list, lang='en'):
    # TODO: Exception: Language not supported, check if words > 0

    syl_count = 0
    
    for word in word_list:
        if lang == 'ru':
            syl_count += len(rusyllab.split_word(word))
        elif lang == 'en':
            syl_count += syllables.estimate(word)
    
    return syl_count

def flesh_reading_ease(documents, lang='en'):
    # TODO: Exception: Language not supported, check if docs > 0, words > 0

    words = get_words(documents, lang)
    syl_total = get_syllable_count(words, lang)

    if lang == 'en':
        return 206.835 - 1.015*(len(words)/len(documents)) - 84.6*(syl_total/len(words))
    elif lang == 'ru'
        return 206.835 - 1.52*(len(words)/len(documents)) - 65.14*(syl_total/len(words)) # coefficients for russian


def leixical_density(documents, lang='en'):
    # TODO: Exception: Language not supported, check if docs > 0, words > 0
    words = get_words(documents, lang)
    lex_items = get_num_of_lex_items(documents, lang)

    return lex_items/len(words)

def type_toke_ratio(documents, lang='en'):
    # TODO: Exception: Language not supported, check if docs > 0, words > 0
    words = get_words(documents, lang)
    num_unq = len(Counter(words).keys())

    return num_unq / len(words)

def calculate_dependency_distance(documents, lang='ru'):
    # TODO: Exception: Language not supported, check if docs > 0
    mdds = list()
    for text in documents:
        dd = 0
        if lang == 'ru':
            doc = Doc(text)
            doc.segment(segmenter)
            doc.parse_syntax(syntax_parser)
            for t in doc.tokens:
                dd += abs(int(t.head_id.split('_')[1]) - int(t.id.split('_')[1]))
            mdd = dd/(len(doc.tokens)-1)    
        elif lang == 'en':
            doc = nlp(text)
            for token in doc:
                dd += abs(token.head.i - token.i)
            mdd = dd/(len(doc) - 1)
        mdds.append(mdd)
    
    return sum(mdds)/len(mdds)