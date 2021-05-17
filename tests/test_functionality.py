from linguaf import linguaf


def test_sentence_count():
    lm = linguaf.LinguisticMeasures()
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
        res = lm.sentence_count(ru_sentence_cnt[i][0])
        assert v == res

    for i in range(len(en_sentence_cnt)):
        v = en_sentence_cnt[i][1]
        res = lm.sentence_count(en_sentence_cnt[i][0])
        assert v == res


def test_char_count():
    lm = linguaf.LinguisticMeasures()
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
        spaces_res = lm.char_count(ru_char_cnt[i][0], ignore_spaces=False)
        no_spaces_res = lm.char_count(ru_char_cnt[i][0], ignore_spaces=True)

        assert spaces == spaces_res
        assert no_spaces == no_spaces_res

    for i in range(len(en_char_cnt)):
        spaces, no_spaces = en_char_cnt[i][1], en_char_cnt[i][2]
        spaces_res = lm.char_count(en_char_cnt[i][0], ignore_spaces=False)
        no_spaces_res = lm.char_count(en_char_cnt[i][0], ignore_spaces=True)

        assert spaces == spaces_res
        assert no_spaces == no_spaces_res


def test_tokenize_stopwords():
    lm = linguaf.LinguisticMeasures()
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

    for i in range(len(ru_tokens)):
        cnt = ru_tokens[i][1]
        true_tokens = ru_tokens[i][2]

        lm.set_remove_stopwords(False)
        tokens = lm.tokenize(document=ru_tokens[i][0], lang='ru')

        assert len(tokens) == cnt
        assert tokens == true_tokens

    for i in range(len(en_tokens)):
        cnt = en_tokens[i][1]
        true_tokens = en_tokens[i][2]

        lm.set_remove_stopwords(False)
        tokens = lm.tokenize(document=en_tokens[i][0], lang='en')

        assert len(tokens) == cnt
        assert tokens == true_tokens


def test_tokenize_remove_stopwords():
    lm = linguaf.LinguisticMeasures()
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

        lm.set_remove_stopwords(True)
        tokens = lm.tokenize(document=ru_tokens[i][0], lang='ru')

        assert len(tokens) == cnt
        assert tokens == true_tokens

    for i in range(len(en_tokens)):
        cnt = en_tokens[i][1]
        true_tokens = en_tokens[i][2]

        lm.set_remove_stopwords(True)
        tokens = lm.tokenize(document=en_tokens[i][0], lang='en')

        assert len(tokens) == cnt
        assert tokens == true_tokens


def test_get_words():
    lm = linguaf.LinguisticMeasures()
    # stopwords removal tested in test_tokenize_remove_stopwords
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

    for i in range(len(ru_words)):
        cnt = ru_words[i][1]
        true_words = ru_words[i][2]

        lm.set_remove_stopwords(False)
        words = lm.get_words(documents=ru_words[i][0], lang='ru')

        assert len(words) == cnt
        assert words == true_words

    for i in range(len(en_words)):
        cnt = en_words[i][1]
        true_words = en_words[i][2]

        lm.set_remove_stopwords(False)
        words = lm.get_words(documents=en_words[i][0], lang='en')

        assert len(words) == cnt
        assert words == true_words


def test_remove_punctuation():
    lm = linguaf.LinguisticMeasures()
    punctuation_data = [
        ("Hello, how are you?", "Hello how are you"),
        ("Привет, как дела?", "Привет как дела"),
        ("Hi...", "Hi"),
        ("Привет...", "Привет"),
    ]
    for i in range(len(punctuation_data)):
        removed = lm.remove_punctuation(punctuation_data[i][0])
        assert removed == punctuation_data[i][1]


def test_letter_count():
    lm = linguaf.LinguisticMeasures()
    letter_count_data = [
        (["Привет, как дела?", "Что делаешь?"], 23, 26),
        (["Hello, how are you?", "What are you doing?"], 29, 35),
    ]

    for d in letter_count_data:
        ignore_spaces_cnt = d[1]
        with_spaces_cnt = d[2]
        ignore_spaces_result = lm.letter_count(d[0], True)
        with_spaces_result = lm.letter_count(d[0], False)

        assert ignore_spaces_result == ignore_spaces_cnt
        assert with_spaces_result == with_spaces_cnt


def test_avg_sentence_length():
    lm = linguaf.LinguisticMeasures()
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

        result_ignore_spaces_len = int(lm.avg_sentence_length(d[0], True))
        result_with_spaces_len = int(lm.avg_sentence_length(d[0], False))

        assert with_spaces_len == result_with_spaces_len
        assert ignore_spaces_len == result_ignore_spaces_len


def test_get_lexical_items():
    lm = linguaf.LinguisticMeasures()
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

    for d in lexical_items_ru_data:
        lex_items = d[1]
        result = lm.get_lexical_items(d[0], 'ru')

        assert result == lex_items

    for d in lexical_items_en_data:
        lex_items = d[1]
        result = lm.get_lexical_items(d[0], 'en')

        assert result == lex_items


def test_syllable_count():
    lm = linguaf.LinguisticMeasures()
    syllable_cnt_ru = [
        (["Ротор", "Дивергенция", "Матожидание"], 11)
    ]
    syllable_cnt_en = [
        (["Curl", "Divergence", "Expectation"], 8)
    ]

    for d in syllable_cnt_ru:
        cnt = d[1]
        res = lm.syllable_count(d[0], 'ru')

        assert res == cnt

    for d in syllable_cnt_en:
        cnt = d[1]
        res = lm.syllable_count(d[0], 'en')

    assert res == cnt


def test_avg_syllables_per_word():
    lm = linguaf.LinguisticMeasures()
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

    for d in avg_syllables_per_word_ru:
        cnt = d[1]
        res = int(lm.avg_syllables_per_word(d[0], 'ru'))

        assert cnt == res

    for d in avg_syllables_per_word_en:
        cnt = d[1]
        res = int(lm.avg_syllables_per_word(d[0], 'en'))

        assert cnt == res


def test_flesh_reading_ease():
    lm = linguaf.LinguisticMeasures()
    fre_data_ru = [
        ([
             "Дивергенция — дифференциальный оператор, отображающий векторное поле на скалярное.",
             "То есть, в результате применения к векторному полю операции дифференцирования получается скалярное поле.",
             "Она определяет (для каждой точки), «насколько расходится входящее и исходящее из малой окрестности данной точки поле»",
             "Точнее, насколько расходятся входящий и исходящий потоки."
         ], 15),
        ([
             "«Лунтик и его друзья» — российский мультсериал, ориентированный на семейную и детскую аудиторию.",
             "Транслируется на телевидении с 1 сентября 2006 года по настоящее время.",
             "Ключевой темой стали приключения маленького пушистого существа Лунтика — космического пришельца, который родился на Луне."
         ], 25)
    ]

    fre_data_en = [
        ([
             "In vector calculus, divergence is a vector operator that operates on a vector field, producing a scalar field giving the quantity of the vector field's source at each point.",
             "More technically, the divergence represents the volume density of the outward flux of a vector field from an infinitesimal volume around a given point."
         ], 44),
        ([
             "Luntik and his friends (Russian: Лунтик и его друзья) or simply Luntik (Russian: Лунтик), in its English version better known as Moonzy, is a Russian animated series for children.",
             "The title character is a purple furry alien named Luntik/Moonzy.",
             "In the first episode Moonzy is shown hatching from an egg on the moon and then falling to Earth.",
             "All of the following series take place at a forest glade near a pond where Moonzy finds a new home."
         ], 79)
    ]

    for d in fre_data_ru:
        fre = d[1]
        res = int(lm.flesh_reading_ease(d[0], 'ru'))

        assert fre == res

    for d in fre_data_en:
        fre = d[1]
        res = int(lm.flesh_reading_ease(d[0], 'en'))

        assert fre == res


def test_lexical_density():
    lm = linguaf.LinguisticMeasures()
    ld_data_ru = [
        ([
             "Дивергенция — дифференциальный оператор, отображающий векторное поле на скалярное.",
             "То есть, в результате применения к векторному полю операции дифференцирования получается скалярное поле.",
             "Она определяет (для каждой точки), «насколько расходится входящее и исходящее из малой окрестности данной точки поле»",
             "Точнее, насколько расходятся входящий и исходящий потоки."
         ], 65),
        ([
             "«Лунтик и его друзья» — российский мультсериал, ориентированный на семейную и детскую аудиторию.",
             "Транслируется на телевидении с 1 сентября 2006 года по настоящее время.",
             "Ключевой темой стали приключения маленького пушистого существа Лунтика — космического пришельца, который родился на Луне."
         ], 63)
    ]

    ld_data_en = [
        ([
             "In vector calculus, divergence is a vector operator that operates on a vector field, producing a scalar field giving the quantity of the vector field's source at each point.",
             "More technically, the divergence represents the volume density of the outward flux of a vector field from an infinitesimal volume around a given point."
         ], 59),
        ([
             "Luntik and his friends (Russian: Лунтик и его друзья) or simply Luntik (Russian: Лунтик), in its English version better known as Moonzy, is a Russian animated series for children.",
             "The title character is a purple furry alien named Luntik/Moonzy.",
             "In the first episode Moonzy is shown hatching from an egg on the moon and then falling to Earth.",
             "All of the following series take place at a forest glade near a pond where Moonzy finds a new home."
         ], 65)
    ]

    for d in ld_data_ru:
        cnt = d[1]
        res = int(lm.lexical_density(d[0], 'ru'))

        assert cnt == res

    for d in ld_data_en:
        cnt = d[1]
        res = int(lm.lexical_density(d[0], 'en'))

        assert cnt == res


def test_type_token_ratio():
    lm = linguaf.LinguisticMeasures()
    ttr_data_ru = [
        ([
             "Дивергенция — дифференциальный оператор, отображающий векторное поле на скалярное.",
             "То есть, в результате применения к векторному полю операции дифференцирования получается скалярное поле.",
             "Она определяет (для каждой точки), «насколько расходится входящее и исходящее из малой окрестности данной точки поле»",
             "Точнее, насколько расходятся входящий и исходящий потоки."
         ], 87),
        ([
             "«Лунтик и его друзья» — российский мультсериал, ориентированный на семейную и детскую аудиторию.",
             "Транслируется на телевидении с 1 сентября 2006 года по настоящее время.",
             "Ключевой темой стали приключения маленького пушистого существа Лунтика — космического пришельца, который родился на Луне."
         ], 90)
    ]

    ttr_data_en = [
        ([
             "In vector calculus, divergence is a vector operator that operates on a vector field, producing a scalar field giving the quantity of the vector field's source at each point.",
             "More technically, the divergence represents the volume density of the outward flux of a vector field from an infinitesimal volume around a given point."
         ], 62),
        ([
             "Luntik and his friends (Russian: Лунтик и его друзья) or simply Luntik (Russian: Лунтик), in its English version better known as Moonzy, is a Russian animated series for children.",
             "The title character is a purple furry alien named Luntik/Moonzy.",
             "In the first episode Moonzy is shown hatching from an egg on the moon and then falling to Earth.",
             "All of the following series take place at a forest glade near a pond where Moonzy finds a new home."
         ], 79)
    ]

    for d in ttr_data_ru:
        cnt = d[1]
        res = int(lm.type_toke_ratio(d[0], 'ru'))

        assert cnt == res

    for d in ttr_data_en:
        cnt = d[1]
        res = int(lm.type_toke_ratio(d[0], 'en'))

        assert cnt == res


def test_mean_dependency_distance():
    lm = linguaf.LinguisticMeasures()
    ttr_data_ru = [
        ([
             "Дивергенция — дифференциальный оператор, отображающий векторное поле на скалярное.",
             "То есть, в результате применения к векторному полю операции дифференцирования получается скалярное поле.",
             "Она определяет (для каждой точки), «насколько расходится входящее и исходящее из малой окрестности данной точки поле»",
             "Точнее, насколько расходятся входящий и исходящий потоки."
         ], 3),
        ([
             "«Лунтик и его друзья» — российский мультсериал, ориентированный на семейную и детскую аудиторию.",
             "Транслируется на телевидении с 1 сентября 2006 года по настоящее время.",
             "Ключевой темой стали приключения маленького пушистого существа Лунтика — космического пришельца, который родился на Луне."
         ], 3)
    ]

    ttr_data_en = [
        ([
             "In vector calculus, divergence is a vector operator that operates on a vector field, producing a scalar field giving the quantity of the vector field's source at each point.",
             "More technically, the divergence represents the volume density of the outward flux of a vector field from an infinitesimal volume around a given point."
         ], 3),
        ([
             "Luntik and his friends (Russian: Лунтик и его друзья) or simply Luntik (Russian: Лунтик), in its English version better known as Moonzy, is a Russian animated series for children.",
             "The title character is a purple furry alien named Luntik/Moonzy.",
             "In the first episode Moonzy is shown hatching from an egg on the moon and then falling to Earth.",
             "All of the following series take place at a forest glade near a pond where Moonzy finds a new home."
         ], 3)
    ]

    for d in ttr_data_ru:
        cnt = d[1]
        res = int(lm.mean_dependency_distance(d[0], 'ru'))

        assert cnt == res

    for d in ttr_data_en:
        cnt = d[1]
        res = int(lm.mean_dependency_distance(d[0], 'en'))

        assert cnt == res
