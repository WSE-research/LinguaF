import json

SUPPORTED_LANGS = ['en', 'ru', 'de', 'fr', 'es', 'zh', # stopwords from nltk
                   'lt', 'be', 'uk', 'hy'] # stopwords from other sources
__version__ = '0.1.2'


def __load_json(filepath):
    data = None
    with open(filepath, encoding="utf8") as f:
        data = json.load(f)
    return data


def __check_documents_param(param):
    if type(param) != list:
        raise TypeError(f"The documents parameter has to be list. Now: {type(param)}")
    for d in param:
        if type(d) != str:
            raise TypeError(f"The documents list should contain strings(str). Now: {type(d)}")


def __check_words_param(param):
    if type(param) != list:
        raise TypeError(f"The words parameter has to be list. Now: {type(param)}")
    for d in param:
        if type(d) != str:
            raise TypeError(f"The words list should contain strings(str). Now: {type(d)}")

def __check_text_param(param):
    if type(param) != str:
        raise TypeError(f"The text should be a string(str). Now: {type(param)}")


def __check_bool_param(param):
    if type(param) != bool:
        raise TypeError(f"The given parameter has to be of type bool. Now: {type(param)}")


def __check_lang_param(param):
    if type(param) != str:
        raise TypeError(f"The lang parameter has to be of type str. Now: {type(param)}")
    if param not in SUPPORTED_LANGS:
        raise ValueError(f"The given language isn't supported. The supported ones are: {SUPPORTED_LANGS}")
