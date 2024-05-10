from linguaf import descriptive_statistics as ds
import pytest
import logging

LOGGER = logging.getLogger(__name__)

def test_sentence_count():
    ru_sentence_cnt = [
        (["Привет, меня зовут Александр! Я создатель этой библиотеки.", "Пользуйтесь на здоровье!"], 3),
        (["Пока"], 1),
        (["Привет...это я...", "Как дела? Хорошо?"], 4)
    ]

    en_sentence_cnt = [
        (["Hello, I'm Aleksandr! I'm the creator of this library.", "Enjoy using it!"], 3),
        (["Bye"], 1),
        (["Hello...it's me...", "How are you? Good!"], 4)
    ]

    for i in range(len(ru_sentence_cnt)):
        v = ru_sentence_cnt[i][1]
        res = ds.sentence_count(ru_sentence_cnt[i][0])
        assert v == res

    for i in range(len(en_sentence_cnt)):
        v = en_sentence_cnt[i][1]
        res = ds.sentence_count(en_sentence_cnt[i][0])
        assert v == res


def test_char_count():
    ru_char_cnt = [
        (["Привет, меня зовут Александр! Я создатель этой библиотеки.", "Пользуйтесь на здоровье!"], 82, 73),
        (["Пока"], 4, 4),
        (["Привет...это я...", "Как дела? Хорошо?"], 34, 31)
    ]

    en_char_cnt = [
        (["Hello, I'm Aleksandr! I'm the creator of this library.", "Enjoy using it!"], 69, 59),
        (["Bye"], 3, 3),
        (["Hello...it's me...", "How are you? Good!"], 36, 32)
    ]

    for i in range(len(ru_char_cnt)):
        spaces, no_spaces = ru_char_cnt[i][1], ru_char_cnt[i][2]
        spaces_res = ds.char_count(ru_char_cnt[i][0], ignore_spaces=False)
        no_spaces_res = ds.char_count(ru_char_cnt[i][0], ignore_spaces=True)

        assert spaces == spaces_res
        assert no_spaces == no_spaces_res

    for i in range(len(en_char_cnt)):
        spaces, no_spaces = en_char_cnt[i][1], en_char_cnt[i][2]
        spaces_res = ds.char_count(en_char_cnt[i][0], ignore_spaces=False)
        no_spaces_res = ds.char_count(en_char_cnt[i][0], ignore_spaces=True)

        assert spaces == spaces_res
        assert no_spaces == no_spaces_res


def test_tokenize_stopwords():
    ru_tokens = [
        ("Привет, меня зовут Александр! Я создатель этой библиотеки.",
         11,
         ['Привет', ',', 'меня', 'зовут', 'Александр', '!', 'Я', 'создатель', 'этой', 'библиотеки', '.']),
        ("Пользуйтесь на здоровье!",
         4,
         ['Пользуйтесь', 'на', 'здоровье', '!']),
        ("Пока",
         1,
         ['Пока']),
        ("Привет...это я...",
         5,
         ['Привет', '...', 'это', 'я', '...']),
        ("Как дела? Хорошо?",
         5,
         ['Как', 'дела', '?', 'Хорошо', '?'])
    ]

    en_tokens = [
        ("Hello, I'm Aleksandr! I'm the creator of this library.",
         14,
         ['Hello', ',', 'I', "'m", 'Aleksandr', '!', 'I', "'m", 'the', 'creator', 'of', 'this', 'library', '.']),
        ("Enjoy using it!",
         4,
         ['Enjoy', 'using', 'it', '!']),
        ("Bye",
         1,
         ["Bye"]),
        ("Hello...it's me...",
         6,
         ['Hello', '...', 'it', "'s", 'me', '...']),
        ("How are you? Good!",
         6,
         ['How', 'are', 'you', '?', 'Good', '!'])
    ]
    #German
    de_tokens = [
        ("Hallo, mein Name ist Aleksandr! Ich bin der Autor dieser Bibliothek.",
         14,
         ['Hallo', ',', 'mein', 'Name', 'ist', 'Aleksandr', '!', 'Ich', 'bin', 'der', 'Autor', 'dieser', 'Bibliothek', '.']),
        ("Viel Freude damit!",
         4,
         ['Viel', 'Freude', 'damit', '!']),
        ("Tschüs",
         1,
         ['Tschüs']),
        ("Hallo...ich bin's...",
         6,
         ['Hallo', '...', 'ich', 'bin', "'s", '...']),
        ("Wie geht es Ihnen? Gut!",
         7,
         ['Wie', 'geht', 'es', 'Ihnen', '?', 'Gut', '!'])
    ]
    #French (mt)
    fr_tokens = [
        ("Bonjour, je m'appelle Aleksandr ! Je suis l'auteur de cette bibliothèque.",
         13,
         ['Bonjour', ',', 'je', "m'appelle", 'Aleksandr', '!', 'Je', 'suis', "l'auteur", 'de', 'cette', 'bibliothèque', '.']),
        ("Amusez-vous bien!",
         3,
         ['Amusez-vous', 'bien', '!']),
        ("Salut",
         1,
         ["Salut"]),
        ("Bonjour...c'est moi...",
         5,
         ['Bonjour', '...', "c'est", 'moi', '...']),
        ("Comment vas-tu ? Bien!",
         5,
         ['Comment', 'vas-tu', '?', 'Bien', '!'])
    ]
    #Spanish (mt)
    es_tokens = [
        ("¡Hola, soy Aleksandr! Soy el autor de esta biblioteca.",
         12,
         ['¡Hola', ',', 'soy', 'Aleksandr', '!', 'Soy', 'el', 'autor', 'de', 'esta', 'biblioteca', '.']),
        # fails if word does not include '¡' -> is this intended?
        ("Disfruta usándolo.",
         3,
         ['Disfruta', 'usándolo', '.']),
        ("adiós",
         1,
         ['adiós']),
        ("Hola...soy yo...",
         5,
         ['Hola', '...', 'soy', 'yo', '...']),
        ("¿Cómo estás? Bien!",
         5,
         ['¿Cómo', 'estás', '?', 'Bien', '!'])
        # fails if word does not include '¿' -> is this intended?
    ]
    #Chinese (mt)
    zh_tokens = [
        ("大家好，我是亚历山大。 我是这个库的创建者",
         2,
         ['大家好，我是亚历山大。', '我是这个库的创建者']),
        # first two words counted as one? 
        # languge-specific signs? 
        # => alternative:
        ("大家好, 我是亚历山大. 我是这个库的创建者",
         5,
         ['大家好', ',', '我是亚历山大', '.', '我是这个库的创建者']),
        # this works as expected ....
        ("玩得开心",
         1,
         ['玩得开心']),
        ("见",
         1,
         ['见']),
        ("你好, 是我",
         3,
         ['你好', ',', '是我']),
        ("你好吗? 好!",
         4,
         ['你好吗', '?', '好', '!'])
    ]
    #Lithuanian
    lt_tokens = [
        ("Sveiki, aš esu Aleksandras! Aš esu šios bibliotekos kūrėjas.",
         12,
         ["Sveiki", ",", "aš", "esu", "Aleksandras", "!", "Aš", "esu", "šios", "bibliotekos", "kūrėjas", "."]),
        ("Mėgaukitės jo naudojimu!",
         4,
         ["Mėgaukitės", "jo", "naudojimu", "!"]),
        ("Iki",
         1,
         ["Iki"]),
        ("Sveiki...tai aš...",
         5,
         ["Sveiki", "...", "tai", "aš", "..."]),
        ("Kaip sekasi? Gerai!",
         5,
         ["Kaip", "sekasi", "?", "Gerai", "!"])
    ]
    #Ukrainian
    uk_tokens = [
        ("Привіт, я Александр! Я творець цієї бібліотеки.",
         10,
         ["Привіт", ",", "я", "Александр", "!", "Я", "творець", "цієї", "бібліотеки", "."]),
        ("Приємного користування!",
         3,
         ["Приємного", "користування", "!"]),
        ("Бувай",
         1,
         ["Бувай"]),
        ("Привіт...це я...",
         5,
         ["Привіт", "...", "це", "я", "..."]),
        ("Як справи? Добре!",
         5,
         ["Як", "справи", "?", "Добре", "!"])
    ]
    #Belarusian
    be_tokens = [
        ("Добры дзень, я Аляксандр! Я стваральнік гэтай бібліятэкі.",
         11,
         ["Добры", "дзень", ",", "я", "Аляксандр", "!", "Я", "стваральнік", "гэтай", "бібліятэкі", "."]),
        ("Прыемнага выкарыстання!",
         3,
         ["Прыемнага", "выкарыстання", "!"]),
        ("Бывай",
         1,
         ["Бывай"]),
        ("Прывітанне...гэта я...",
         5,
         ["Прывітанне", "...", "гэта", "я", "..."]),
        ("Як ты? Добра!",
         5,
         ["Як", "ты", "?", "Добра", "!"])
    ]
    #Armenian
    hy_tokens = [
        ("Բարև, ես Ալեքսանդրն եմ: Ես այս գրադարանի ստեղծողն եմ:",
         12,
         ["Բարև", ",", "ես", "Ալեքսանդրն", "եմ", ":", "Ես", "այս", "գրադարանի", "ստեղծողն", "եմ", ":"]),
        ("Վայելեք այն օգտագործելը:",
         4,
         ["Վայելեք", "այն", "օգտագործելը", ":"]),
        ("Ցտեսություն",
         1,
         ["Ցտեսություն"]),
        ("Բարև...ես եմ...",
         5,
         ["Բարև", "...", "ես", "եմ", "..."]),
        ("Ինչպես ես? Լավ!",
         5,
         ["Ինչպես", "ես", "?", "Լավ", "!"])
    ]

    check_tokenization(en_tokens, 'en')
    check_tokenization(ru_tokens, 'ru')
    check_tokenization(de_tokens, 'de')
    check_tokenization(fr_tokens, 'fr')
    check_tokenization(es_tokens, 'es')
    check_tokenization(zh_tokens, 'zh')
    check_tokenization(lt_tokens, 'lt')
    check_tokenization(uk_tokens, 'uk')
    check_tokenization(be_tokens, 'be')
    check_tokenization(hy_tokens, 'hy')



# helper function for test_tokenize_stopwords
def check_tokenization(token_list: list, lang: str):
    for i in range(len(token_list)):
        cnt = token_list[i][1]
        true_tokens = token_list[i][2]

        tokens = ds.tokenize(text=token_list[i][0], lang=lang, remove_stopwords=False)

        assert len(tokens) == cnt
        assert tokens == true_tokens



def test_tokenize_remove_stopwords():
    ru_tokens = [
        ("Привет, меня зовут Александр! Впрочем, это другая история.",
         10,
         ['Привет', ',', 'зовут', 'Александр', '!', ',', 'это', 'другая', 'история', '.']),
        ("Пользуйтесь на здоровье!",
         3,
         ['Пользуйтесь', 'здоровье', '!']),
        ("Пока",
         1,
         ['Пока']),
        ("Привет...это я...",
         4,
         ['Привет', '...', 'это', '...']),
        ("Как дела? Хорошо?",
         3,
         ['дела', '?', '?'])
    ]

    en_tokens = [
        ("Hello, I'm Aleksandr! I'm the creator of this library.",
         9,
         ['Hello', ',', "'m", 'Aleksandr', '!', "'m", 'creator', 'library', '.']),
        ("Enjoy using it!",
         3,
         ['Enjoy', 'using', '!']),
        ("Bye",
         1,
         ["Bye"]),
        ("Hello...it's me...",
         4,
         ['Hello', '...', "'s", '...']),
        ("How are you? Good!",
         3,
         ['?', 'Good', '!'])
    ]

    for i in range(len(ru_tokens)):
        cnt = ru_tokens[i][1]
        true_tokens = ru_tokens[i][2]

        tokens = ds.tokenize(text=ru_tokens[i][0], lang='ru', remove_stopwords=True)

        assert len(tokens) == cnt
        assert tokens == true_tokens

    for i in range(len(en_tokens)):
        cnt = en_tokens[i][1]
        true_tokens = en_tokens[i][2]

        tokens = ds.tokenize(text=en_tokens[i][0], lang='en', remove_stopwords=True)

        assert len(tokens) == cnt
        assert tokens == true_tokens


def test_get_words():
    # stopwords removal tested in test_tokenize_remove_stopwords
    #Russian
    ru_words = [
        (["Привет, меня зовут Александр! Я создатель этой библиотеки."],
         8,
         ['Привет', 'меня', 'зовут', 'Александр', 'Я', 'создатель', 'этой', 'библиотеки']),
        (["Пользуйтесь на здоровье!"],
         3,
         ['Пользуйтесь', 'на', 'здоровье']),
        (["Пока"],
         1,
         ['Пока']),
        (["Привет...это я..."],
         3,
         ['Привет', 'это', 'я']),
        (["Как дела? Хорошо?"],
         3,
         ['Как', 'дела', 'Хорошо'])
    ]
    #English
    en_words = [
        (["Hello, I'm Aleksandr! I'm the creator of this library."],
         11,
         ['Hello', 'I', "'m", 'Aleksandr', 'I', "'m", 'the', 'creator', 'of', 'this', 'library']),
        (["Enjoy using it!"],
         3,
         ['Enjoy', 'using', 'it']),
        (["Bye"],
         1,
         ["Bye"]),
        (["Hello...it's me..."],
         4,
         ['Hello', 'it', "'s", 'me']),
        (["How are you? Good!"],
         4,
         ['How', 'are', 'you', 'Good'])
    ]
    #German
    de_words = [
        (["Hallo, mein Name ist Aleksandr! Ich bin der Autor dieser Bibliothek."],
         11,
         ['Hallo', 'mein', 'Name', 'ist', 'Aleksandr', 'Ich', 'bin', 'der', 'Autor', 'dieser', 'Bibliothek']),
        (["Viel Freude damit!"],
         3,
         ['Viel', 'Freude', 'damit']),
        (["Tschüs"],
         1,
         ["Tschüs"]),
        (["Hallo...ich bin's..."],
         4,
         ['Hallo', 'ich', 'bin', "'s"]),
        (["Wie geht es Ihnen? Gut!"],
         5,
         ['Wie', 'geht', 'es', 'Ihnen', 'Gut'])
    ]
    #French (mt)
    fr_words = [
        (["Bonjour, je m'appelle Aleksandr ! Je suis l'auteur de cette bibliothèque."],
         10,
         ['Bonjour', 'je', "m'appelle", 'Aleksandr', 'Je', 'suis', "l'auteur", 'de', 'cette', 'bibliothèque']),
        (["Amusez-vous bien!"],
         2,
         ['Amusez-vous', 'bien']),
        (["Salut"],
         1,
         ["Salut"]),
        (["Bonjour...c'est moi..."],
         3,
         ['Bonjour', "c'est", 'moi']),
        (["Comment vas-tu ? Bien!"],
         3,
         ['Comment', 'vas-tu', 'Bien'])
    ]
    #Spanish (mt)
    es_words = [
        (["¡Hola, soy Aleksandr! Soy el autor de esta biblioteca."],
         9,
         ['¡Hola', 'soy', 'Aleksandr', 'Soy', 'el', 'autor', 'de', 'esta', 'biblioteca']),
        # fails if word does not include '¡' -> is this intended?
        (["Disfruta usándolo."],
         2,
         ['Disfruta', 'usándolo']),
        (["adiós"],
         1,
         ['adiós']),
        (["Hola...soy yo..."],
         3,
         ['Hola', 'soy', 'yo']),
        (["¿Cómo estás? Bien!"],
         3,
         ['¿Cómo', 'estás', 'Bien'])
        # fails if word does not include '¿' -> is this intended?
    ]
    #Chinese (mt)
    zh_words = [
        (["大家好，我是亚历山大。 我是这个库的创建者"],
         2,
         ['大家好，我是亚历山大。', '我是这个库的创建者']),
        # first two words counted as one? 
        # languge-specific signs? 
        # => alternative:
        (["大家好, 我是亚历山大. 我是这个库的创建者"],
         3,
         ['大家好', '我是亚历山大', '我是这个库的创建者']),
        # this works as expected ....
        (["玩得开心"],
         1,
         ['玩得开心']),
        (["见"],
         1,
         ['见']),
        (["你好, 是我"],
         2,
         ['你好', '是我']),
        (["你好吗? 好!"],
         2,
         ['你好吗', '好'])
    ]
    #Lithuanian
    lt_words = [
        (["Sveiki, aš esu Aleksandras! Aš esu šios bibliotekos kūrėjas."],
         9,
         ["Sveiki", "aš", "esu", "Aleksandras", "Aš", "esu", "šios", "bibliotekos", "kūrėjas"]),
        (["Mėgaukitės jo naudojimu!"],
         3,
         ["Mėgaukitės", "jo", "naudojimu"]),
        (["Iki"],
         1,
         ["Iki"]),
        (["Sveiki...tai aš..."],
         3,
         ["Sveiki", "tai", "aš"]),
        (["Kaip sekasi? Gerai!"],
         3,
         ["Kaip", "sekasi", "Gerai"])
    ]
    #Ukrainian
    uk_words = [
        (["Привіт, я Александр! Я творець цієї бібліотеки."],
         7,
         ["Привіт", "я", "Александр", "Я", "творець", "цієї", "бібліотеки"]),
        (["Приємного користування!"],
         2,
         ["Приємного", "користування"]),
        (["Бувай"],
         1,
         ["Бувай"]),
        (["Привіт...це я..."],
         3,
         ["Привіт", "це", "я"]),
        (["Як справи? Добре!"],
         3,
         ["Як", "справи", "Добре"])
    ]
    #Belarusian
    be_words = [
        (["Добры дзень, я Аляксандр! Я стваральнік гэтай бібліятэкі."],
         8,
         ["Добры", "дзень", "я", "Аляксандр", "Я", "стваральнік", "гэтай", "бібліятэкі"]),
        (["Прыемнага выкарыстання!"],
         2,
         ["Прыемнага", "выкарыстання"]),
        (["Бывай"],
         1,
         ["Бывай"]),
        (["Прывітанне...гэта я..."],
         3,
         ["Прывітанне", "гэта", "я"]),
        (["Як ты? Добра!"],
         3,
         ["Як", "ты", "Добра"])
    ]
    #Armenian
    hy_words = [
        (["Բարև, ես Ալեքսանդրն եմ: Ես այս գրադարանի ստեղծողն եմ:"],
         9,
         ["Բարև", "ես", "Ալեքսանդրն", "եմ", "Ես", "այս", "գրադարանի", "ստեղծողն", "եմ"]),
        (["Վայելեք այն օգտագործելը:"],
         3,
         ["Վայելեք", "այն", "օգտագործելը"]),
        (["Ցտեսություն"],
         1,
         ["Ցտեսություն"]),
        (["Բարև...ես եմ..."],
         3,
         ["Բարև", "ես", "եմ"]),
        (["Ինչպես ես? Լավ!"],
         3,
         ["Ինչպես", "ես", "Լավ"])
    ]

    check_found_words(ru_words, 'ru')
    check_found_words(en_words, 'en')
    check_found_words(de_words, 'de')
    check_found_words(fr_words, 'fr')
    check_found_words(es_words, 'es')
    check_found_words(zh_words, 'zh')

    check_found_words(lt_words, 'lt')
    check_found_words(uk_words, 'uk')
    check_found_words(be_words, 'be')
    check_found_words(hy_words, 'hy')


# helper function for test_get_words
def check_found_words(words_list: list, lang: str):
    for i in range(len(words_list)):
        cnt = words_list[i][1]
        true_words = words_list[i][2]

        words = ds.get_words(documents=words_list[i][0], lang=lang, remove_stopwords=False)

        assert len(words) == cnt
        assert words == true_words


def test_remove_punctuation():
    punctuation_data = [
        ("Hello, how are you?", "Hello how are you"),
        ("Привет, как дела?", "Привет как дела"),
        ("Hi...", "Hi"),
        ("Привет...", "Привет"),
    ]
    for i in range(len(punctuation_data)):
        removed = ds.remove_punctuation(punctuation_data[i][0])
        assert removed == punctuation_data[i][1]


def test_letter_count():
    letter_count_data = [
        (["Привет, как дела?", "Что делаешь?"], 23, 26),
        (["Hello, how are you?", "What are you doing?"], 29, 35),
    ]

    for d in letter_count_data:
        ignore_spaces_cnt = d[1]
        with_spaces_cnt = d[2]
        ignore_spaces_result = ds.letter_count(d[0], True)
        with_spaces_result = ds.letter_count(d[0], False)

        assert ignore_spaces_result == ignore_spaces_cnt
        assert with_spaces_result == with_spaces_cnt


def test_avg_sentence_length():
    avg_sentence_len_data = [
        (["Привет, меня зовут Александр! Я создатель этой библиотеки.", "Пользуйтесь на здоровье!"], 24, 27),
        (["Пока"], 4, 4),
        (["Привет...это я...", "Как дела? Хорошо?"], 7, 8),
        (["Hello, I'm Aleksandr! I'am the creator of this library.", "Enjoy using it!"], 20, 23),
        (["Bye"], 3, 3),
        (["Hello...it's me...", "How are you? Good!"], 8, 9)
    ]

    for d in avg_sentence_len_data:
        ignore_spaces_len = d[1]
        with_spaces_len = d[2]

        result_ignore_spaces_len = int(ds.avg_sentence_length(d[0], True))
        result_with_spaces_len = int(ds.avg_sentence_length(d[0], False))

        assert with_spaces_len == result_with_spaces_len
        assert ignore_spaces_len == result_ignore_spaces_len


def test_syllable_count():
    syllable_cnt_ru = [
        (["Ротор", "Дивергенция", "Матожидание"], 11)
    ]
    syllable_cnt_en = [
        (["Curl", "Divergence", "Expectation"], 8)
    ]

    for d in syllable_cnt_ru:
        cnt = d[1]
        res = ds.syllable_count(d[0], 'ru')

        assert res == cnt

    for d in syllable_cnt_en:
        cnt = d[1]
        res = ds.syllable_count(d[0], 'en')

    assert res == cnt


def test_avg_syllable_per_word():
    avg_syllables_per_word_ru = [
        (["Привет, меня зовут Александр! Я создатель этой библиотеки.", "Пользуйтесь на здоровье!"], 2),
        (["Пока"], 2),
        (["Привет...это я...", "Как дела? Хорошо?"], 1)
    ]

    avg_syllables_per_word_en = [
        (["Hello, I'm Aleksandr! I'am the creator of this library.", "Enjoy using it!"], 1),
        (["Bye"], 1),
        (["Hello...it's me...", "How are you? Good!"], 1)
    ]

    avg_syllables_per_word_de = [
        (["Hallo, mein Name ist Aleksandr! Ich bin der Autor dieser Bibliothek.", "Viel Freude damit!"], 1),
        (["Auf Wiedersehen"], 2),
        (["Hallo...ich bin's...", "Wie geht es Ihnen? Gut!"], 1),
    ]
    #French (mt)
    avg_syllables_per_word_fr = [
        (["Bonjour, je m'appelle Aleksandr ! Je suis l'auteur de cette bibliothèque.", "Amusez-vous bien!"], 1),
        (["Salut"], 2),
        (["Bonjour...c'est moi...", "Comment vas-tu ? Bien!"], 1)
    ]
    #Spanish (mt)
    avg_syllables_per_word_es = [
        (["¡Hola, soy Aleksandr! Soy el autor de esta biblioteca.", "Disfruta usándolo."], 2),
        (["adiós"], 1), # TODO: why is this only 1 syllable? 
        (["Hola...soy yo...", "¿Cómo estás? Bien!"], 1)
    ]
    #Chinese (mt)
    avg_syllables_per_word_zh = [
        # syllable counting is currently not supported.
        # instead, this tests for an exception
        (["大家好, 我是亚历山大. 我是这个库的创建者.", "玩得开心"], 0),
        (["见"], 1),
        (["你好, 是我","你好吗? 好!"], 0)
    ]
    #Lithuanian
    avg_syllables_per_word_lt = [
        (["Sveiki, aš esu Aleksandras! Aš esu šios bibliotekos kūrėjas.", "Mėgaukitės jo naudojimu!"], 2),
        (["Iki"], 1),
        (["Sveiki...tai aš...", "Kaip sekasi? Gerai!"], 1)
    ]
    #Ukrainian
    avg_syllables_per_word_uk = [
        (["Привіт, я Александр! Я творець цієї бібліотеки.", "Приємного користування!"], 3),
        (["Бувай"], 2),
        (["Привіт...це я...", "Як справи? Добре!"], 1)
    ]
    #Belarusian
    avg_syllables_per_word_be = [
        (["Добры дзень, я Аляксандр! Я стваральнік гэтай бібліятэкі.", "Прыемнага выкарыстання!"], 3),
        (["Бывай"], 2),
        (["Прывітанне...гэта я...", "Як ты? Добра!"], 2)
    ]
    #Armenian
    avg_syllables_per_word_hy = [
        # armenian is also not supported
        # test for an exception instead
        (["Բարև, ես Ալեքսանդրն եմ: Ես այս գրադարանի ստեղծողն եմ:", "Վայելեք այն օգտագործելը:"], 0),
        (["Ցտեսություն"], 0),
        (["Բարև...ես եմ...", "Ինչպես ես? Լավ!"], 0)
    ]

    check_avg_syllable_per_word(avg_syllables_per_word_ru, 'ru')
    check_avg_syllable_per_word(avg_syllables_per_word_en, 'en')
    check_avg_syllable_per_word(avg_syllables_per_word_de, 'de')
    check_avg_syllable_per_word(avg_syllables_per_word_fr, 'fr')
    check_avg_syllable_per_word(avg_syllables_per_word_es, 'es')
    check_avg_syllable_per_word(avg_syllables_per_word_lt, 'lt')
    check_avg_syllable_per_word(avg_syllables_per_word_uk, 'uk')
    check_avg_syllable_per_word(avg_syllables_per_word_be, 'be')
    # chinese is not supported; it should raise a ValueError
    with pytest.raises(ValueError):
        check_avg_syllable_per_word(avg_syllables_per_word_zh, 'zh')
    with pytest.raises(ValueError):
        check_avg_syllable_per_word(avg_syllables_per_word_hy, 'hy')


# helper function for test_avg_syllable_per_word
def check_avg_syllable_per_word(syllable_list: list, lang: str):
    for d in syllable_list:
        cnt = d[1]
        res = int(ds.avg_syllable_per_word(d[0], lang))

        assert cnt == res


def test_get_lexical_items():
    lexical_items_ru_data = [
        (["Привет, меня зовут Александр! Я создатель этой библиотеки.", "Пользуйтесь на здоровье!"],
         [('Привет', 'NOUN'), ('зовут', 'VERB'), ('Александр', 'NOUN'), ('создатель', 'NOUN'), ('этой', 'ADJF'),
          ('библиотеки', 'NOUN'), ('Пользуйтесь', 'VERB'), ('здоровье', 'NOUN')]),
        (["Пока"], [('Пока', 'ADVB')]),
        (["Привет...это я...", "Как дела? Хорошо?"], [('Привет', 'NOUN'), ('дела', 'NOUN'), ('Хорошо', 'ADVB')])
    ]

    lexical_items_en_data = [
        (["Hello, I'm Aleksandr! I'm the creator of this library.", "Enjoy using it!"],
         [('Hello', 'NNP'), ("'m", 'VBP'), ('Aleksandr', 'JJ'), ("'m", 'VBP'), ('creator', 'NN'), ('library', 'NN'),
          ('Enjoy', 'NNP'), ('using', 'VBG')]),
        (["Bye"], [('Bye', 'NN')]),
        (["Hello...it's me...", "How are you? Good!"],
         [('Hello', 'NNP'), ("'s", 'VBZ'), ('are', 'VBP'), ('Good', 'JJ')])
    ]

    lexical_items_de_data = [
        (["Hallo, mein Name ist Aleksandr! Ich bin der Autor dieser Bibliothek.", "Viel Freude damit!"],
          [('Hallo', 'PROPN'), ('mein', 'DET'), ('Name', 'NOUN'), ('ist', 'AUX'), ('Aleksandr', 'PROPN'),
           ('Ich', 'PRON'), ('bin', 'AUX'), ('der', 'DET'), ('Autor', 'NOUN'), ('dieser', 'DET'), ('Bibliothek', 'NOUN'),
           ('Viel', 'DET'), ('Freude', 'NOUN'), ('damit', 'ADV')]),
#          [('Hallo', 'PROPN'), (',', 'PUNCT'), ('mein', 'DET'), ('Name', 'NOUN'), ('ist', 'AUX'), ('Aleksandr', 'PROPN'),
#           ('!', 'PUNCT'), ('Ich', 'PRON'), ('bin', 'AUX'), ('der', 'DET'), ('Autor', 'NOUN'), ('dieser', 'DET'), ('Bibliothek', 'NOUN'),
#           ('.', 'PUNCT'), ('Viel', 'DET'), ('Freude', 'NOUN'), ('damit', 'ADV'), ('!', 'PUNCT')]),
        (["Auf Wiedersehen"],
         [('Auf', 'ADP'), ('Wiedersehen', 'NOUN')]),
        (["Hallo...ich bin's...", "Wie geht es Ihnen? Gut!"],
         [('Hallo', 'PROPN'), ('ich', 'PRON'), ("bin's", 'VERB'),
          ('Wie', 'ADV'), ('geht', 'VERB'), ('es', 'PRON'), ('Ihnen', 'PRON'), ('Gut', 'ADV')])
    ]

    lexical_items_fr_data = [
        (["Bonjour, je m'appelle Aleksandr ! Je suis l'auteur de cette bibliothèque.", "Amusez-vous bien!"],
         [('Bonjour', 'PROPN'), ('je', 'PRON'), ("m'", 'PRON'), ('appelle', 'VERB'), ('Aleksandr', 'PROPN'),
          ('Je', 'PRON'), ('suis', 'AUX'), ("l'", 'DET'), ('auteur', 'NOUN'), ('de', 'ADP'), ('cette', 'DET'),
          ('bibliothèque', 'NOUN'), ('Amusez', 'ADV'), ('-vous', 'NOUN'), ('bien', 'ADV')]),
        (["Salut"],
         [('Salut', 'PROPN')]),
        (["Bonjour...c'est moi...", "Comment vas-tu ? Bien!"],
         [('Bonjour', 'PROPN'), ("c'", 'PRON'), ('est', 'AUX'), ('moi', 'VERB'), ('Comment', 'ADV'),
          ('vas', 'PROPN'), ('-', 'NOUN'), ('tu', 'NOUN'), ('Bien', 'ADV')])
    ]

    lexical_items_es_data = [
        (["¡Hola, soy Aleksandr! Soy el autor de esta biblioteca.", "Disfruta usándolo."],
         [('Hola', 'PROPN'), ('soy', 'AUX'), ('Aleksandr', 'PROPN'), ('Soy', 'AUX'), ('el', 'DET'),
          ('autor', 'NOUN'), ('de', 'ADP'), ('esta', 'DET'), ('biblioteca', 'NOUN'), ('Disfruta', 'PROPN'), ('usándolo', 'ADJ')]),
        (["adiós"],
         [('adiós', 'INTJ')]),
        (["Hola...soy yo...", "¿Cómo estás? Bien!"],
         [('Hola', 'PROPN'), ('soy', 'AUX'), ('yo', 'PRON'), ('Cómo', 'PRON'), ('estás', 'VERB'), ('Bien', 'ADV')])
    ]

    lexical_items_zh_data = [
        (["大家好, 我是亚历山大. 我是这个库的创建者.", "玩得开心"],
         [('大家', 'PRON'), ('好', 'VERB'), ('我', 'PRON'), ('是', 'VERB'), ('亚历山大', 'PROPN'),
          ('我', 'PRON'), ('是', 'VERB',), ('这个', 'DET'), ('库', 'NOUN'), ('的', 'PART'),
          ('创建者', 'NOUN'), ('玩', 'VERB'), ('得', 'PART'), ('开心', 'VERB')]),
        (["见"],
         [('见', 'VERB')]),
        (["你好, 是我","你好吗? 好!"],
         [('你好', 'VERB'), ('是', 'VERB'), ('我', 'PRON'), ('你好', 'VERB'), ('吗', 'PART'),
          ('好', 'VERB') ])
    ]

    lexical_items_lt_data = [
        (["Sveiki, aš esu Aleksandras! Aš esu šios bibliotekos kūrėjas.", "Mėgaukitės jo naudojimu!"],
         [('Sveiki', 'ADJ'), ('aš','PRON'), ('esu', 'VERB'), ('Aleksandras', 'PROPN'),
          ('Aš', 'PRON'), ('esu', 'AUX'), ('šios', 'DET'), ('bibliotekos', 'NOUN'),
          ('kūrėjas', 'NOUN'), ('Mėgaukitės', 'NOUN'), ('jo', 'PRON'), ('naudojimu', 'NOUN')]),
        (["Iki"],
         [('Iki', 'ADP')]),
        (["Sveiki...tai aš...", "Kaip sekasi? Gerai!"],
         [('Sveiki', 'ADJ'), ('tai', 'PART'), ('aš', 'PRON'), ('Kaip', 'SCONJ'),
          ('sekasi', 'VERB'), ('Gerai', 'ADV')])
    ]

    lexical_items_uk_data = [
        (["Привіт, я Александр! Я творець цієї бібліотеки.", "Приємного користування!"],
         [('Привіт', 'NOUN'), ('Александр', 'NOUN'), ('творець', 'NOUN'), ('бібліотеки', 'VERB'),
          ('Приємного', 'ADVB'), ('користування', 'ADJS')]),
        (["Бувай"],
         [('Бувай', 'VERB')]),
        (["Привіт...це я...", "Як справи? Добре!"],
         [('Привіт', 'NOUN'), ('Як', 'NOUN'), ('справи', 'VERB'), ('Добре', 'NOUN')])
    ]

    lexical_items_be_data = [
        (["Добры дзень, я Аляксандр! Я стваральнік гэтай бібліятэкі.", "Прыемнага выкарыстання!"],
         []),
        (["Бывай"],
         []),
        (["Прывітанне...гэта я...", "Як ты? Добра!"],
         [])
    ]

    lexical_items_hy_data = [
        (["Բարև, ես Ալեքսանդրն եմ: Ես այս գրադարանի ստեղծողն եմ:", "Վայելեք այն օգտագործելը:"],
         []),
        (["Ցտեսություն"],
         []),
        (["Բարև...ես եմ...", "Ինչպես ես? Լավ!"],
         [])
    ]

    check_lexical_items(lexical_items_ru_data, 'ru')
    check_lexical_items(lexical_items_en_data, 'en')
    check_lexical_items(lexical_items_de_data, 'de')
    check_lexical_items(lexical_items_fr_data, 'fr')
    check_lexical_items(lexical_items_es_data, 'es')
    check_lexical_items(lexical_items_zh_data, 'zh')
    check_lexical_items(lexical_items_lt_data, 'lt')
    check_lexical_items(lexical_items_uk_data, 'uk')

    with pytest.raises(ValueError):
        check_lexical_items(lexical_items_hy_data, 'hy')
    with pytest.raises(ValueError):
        check_lexical_items(lexical_items_be_data, 'be')

# helper function for test_get_lexical_items
def check_lexical_items(lexical_items, lang):
    for d in lexical_items:
        lex_items = d[1]
        result = ds.get_lexical_items(d[0], False, lang)
        assert result == lex_items

