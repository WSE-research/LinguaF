from linguaf import descriptive_statistics as ds


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

    for i in range(len(ru_tokens)):
        cnt = ru_tokens[i][1]
        true_tokens = ru_tokens[i][2]

        tokens = ds.tokenize(text=ru_tokens[i][0], lang='ru', remove_stopwords=False)

        assert len(tokens) == cnt
        assert tokens == true_tokens

    for i in range(len(en_tokens)):
        cnt = en_tokens[i][1]
        true_tokens = en_tokens[i][2]

        tokens = ds.tokenize(text=en_tokens[i][0], lang='en', remove_stopwords=False)

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

        words = ds.get_words(documents=ru_words[i][0], lang='ru', remove_stopwords=False)

        assert len(words) == cnt
        assert words == true_words

    for i in range(len(en_words)):
        cnt = en_words[i][1]
        true_words = en_words[i][2]

        words = ds.get_words(documents=en_words[i][0], lang='en', remove_stopwords=False)

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

    for d in avg_syllables_per_word_ru:
        cnt = d[1]
        res = int(ds.avg_syllable_per_word(d[0], 'ru'))

        assert cnt == res

    for d in avg_syllables_per_word_en:
        cnt = d[1]
        res = int(ds.avg_syllable_per_word(d[0], 'en'))

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

    for d in lexical_items_ru_data:
        lex_items = d[1]
        result = ds.get_lexical_items(d[0], False, 'ru')

        assert result == lex_items

    for d in lexical_items_en_data:
        lex_items = d[1]
        result = ds.get_lexical_items(d[0], False, 'en')

        assert result == lex_items
