from linguaf import linguaf

lm = linguaf.LinguisticMeasures()


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
        res = lm.sentence_count(ru_sentence_cnt[i][0])
        assert v == res

    for i in range(len(en_sentence_cnt)):
        v = en_sentence_cnt[i][1]
        res = lm.sentence_count(en_sentence_cnt[i][0])
        assert v == res


def test_char_count():
    ru_char_cnt = [
        (["Привет, меня зовут Александр! Я создатель этой библиотеки.", "Пользуйтесь на здоровье!"], 82, 73),
        (["Пока"], 4, 4),
        (["Привет...это я...", "Как дела? Хорошо?"], 34, 31)
    ]

    en_char_cnt = [
        (["Hello, I'm Aleksandr! I'm the creator of this library.", "Enjoy using it!"], 70, 60),
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

