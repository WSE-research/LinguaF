from linguaf import readability as r


def test_flesh_reading_ease():
    fre_data_ru = [
        ([
             "Дивергенция — дифференциальный оператор, отображающий векторное поле на скалярное.",
             "То есть, в результате применения к векторному полю операции дифференцирования получается скалярное поле.",
             "Она определяет (для каждой точки), «насколько расходится входящее и исходящее из малой окрестности данной точки поле»",
             "Точнее, насколько расходятся входящий и исходящий потоки."
         ], 25),
        ([
             "«Лунтик и его друзья» — российский мультсериал, ориентированный на семейную и детскую аудиторию.",
             "Транслируется на телевидении с 1 сентября 2006 года по настоящее время.",
             "Ключевой темой стали приключения маленького пушистого существа Лунтика — космического пришельца, который родился на Луне."
         ], 33)
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
        res = int(r.flesch_reading_ease(d[0], 'ru', False))

        assert fre == res

    for d in fre_data_en:
        fre = d[1]
        res = int(r.flesch_reading_ease(d[0], 'en', False))

        assert fre == res


def test_flesh_kincaid_grade():
    read_data_ru = [
        ([
             "Дивергенция — дифференциальный оператор, отображающий векторное поле на скалярное.",
             "То есть, в результате применения к векторному полю операции дифференцирования получается скалярное поле.",
             "Она определяет (для каждой точки), «насколько расходится входящее и исходящее из малой окрестности данной точки поле»",
             "Точнее, насколько расходятся входящий и исходящий потоки."
         ], 13),
        ([
             "«Лунтик и его друзья» — российский мультсериал, ориентированный на семейную и детскую аудиторию.",
             "Транслируется на телевидении с 1 сентября 2006 года по настоящее время.",
             "Ключевой темой стали приключения маленького пушистого существа Лунтика — космического пришельца, который родился на Луне."
         ], 12)
    ]

    read_data_en = [
        ([
             "In vector calculus, divergence is a vector operator that operates on a vector field, producing a scalar field giving the quantity of the vector field's source at each point.",
             "More technically, the divergence represents the volume density of the outward flux of a vector field from an infinitesimal volume around a given point."
         ], 13),
        ([
             "Luntik and his friends (Russian: Лунтик и его друзья) or simply Luntik (Russian: Лунтик), in its English version better known as Moonzy, is a Russian animated series for children.",
             "The title character is a purple furry alien named Luntik/Moonzy.",
             "In the first episode Moonzy is shown hatching from an egg on the moon and then falling to Earth.",
             "All of the following series take place at a forest glade near a pond where Moonzy finds a new home."
         ], 6)
    ]

    for d in read_data_ru:
        score = d[1]
        res = int(r.flesch_kincaid_grade(d[0], 'ru', False))

        assert score == res

    for d in read_data_en:
        score = d[1]
        res = int(r.flesch_kincaid_grade(d[0], 'en', False))

        assert score == res


def test_automated_readability_index():
    read_data_ru = [
        ([
             "Дивергенция — дифференциальный оператор, отображающий векторное поле на скалярное.",
             "То есть, в результате применения к векторному полю операции дифференцирования получается скалярное поле.",
             "Она определяет (для каждой точки), «насколько расходится входящее и исходящее из малой окрестности данной точки поле»",
             "Точнее, насколько расходятся входящий и исходящий потоки."
         ], 18),
        ([
             "«Лунтик и его друзья» — российский мультсериал, ориентированный на семейную и детскую аудиторию.",
             "Транслируется на телевидении с 1 сентября 2006 года по настоящее время.",
             "Ключевой темой стали приключения маленького пушистого существа Лунтика — космического пришельца, который родился на Луне."
         ], 16)
    ]

    read_data_en = [
        ([
             "In vector calculus, divergence is a vector operator that operates on a vector field, producing a scalar field giving the quantity of the vector field's source at each point.",
             "More technically, the divergence represents the volume density of the outward flux of a vector field from an infinitesimal volume around a given point."
         ], 15),
        ([
             "Luntik and his friends (Russian: Лунтик и его друзья) or simply Luntik (Russian: Лунтик), in its English version better known as Moonzy, is a Russian animated series for children.",
             "The title character is a purple furry alien named Luntik/Moonzy.",
             "In the first episode Moonzy is shown hatching from an egg on the moon and then falling to Earth.",
             "All of the following series take place at a forest glade near a pond where Moonzy finds a new home."
         ], 10)
    ]

    for d in read_data_ru:
        score = d[1]
        res = int(r.automated_readability_index(d[0], 'ru', False))

        assert score == res

    for d in read_data_en:
        score = d[1]
        res = int(r.automated_readability_index(d[0], 'en', False))

        assert score == res


def test_automated_readability_index_simple():
    read_data_ru = [
        ([
             "Дивергенция — дифференциальный оператор, отображающий векторное поле на скалярное.",
             "То есть, в результате применения к векторному полю операции дифференцирования получается скалярное поле.",
             "Она определяет (для каждой точки), «насколько расходится входящее и исходящее из малой окрестности данной точки поле»",
             "Точнее, насколько расходятся входящий и исходящий потоки."
         ], 76),
        ([
             "«Лунтик и его друзья» — российский мультсериал, ориентированный на семейную и детскую аудиторию.",
             "Транслируется на телевидении с 1 сентября 2006 года по настоящее время.",
             "Ключевой темой стали приключения маленького пушистого существа Лунтика — космического пришельца, который родился на Луне."
         ], 73)
    ]

    read_data_en = [
        ([
             "In vector calculus, divergence is a vector operator that operates on a vector field, producing a scalar field giving the quantity of the vector field's source at each point.",
             "More technically, the divergence represents the volume density of the outward flux of a vector field from an infinitesimal volume around a given point."
         ], 72),
        ([
             "Luntik and his friends (Russian: Лунтик и его друзья) or simply Luntik (Russian: Лунтик), in its English version better known as Moonzy, is a Russian animated series for children.",
             "The title character is a purple furry alien named Luntik/Moonzy.",
             "In the first episode Moonzy is shown hatching from an egg on the moon and then falling to Earth.",
             "All of the following series take place at a forest glade near a pond where Moonzy finds a new home."
         ], 61)
    ]

    for d in read_data_ru:
        score = d[1]
        res = int(r.automated_readability_index_simple(d[0], 'ru', False))

        assert score == res

    for d in read_data_en:
        score = d[1]
        res = int(r.automated_readability_index_simple(d[0], 'en', False))

        assert score == res


def test_coleman_readability():
    read_data_ru = [
        ([
             "Дивергенция — дифференциальный оператор, отображающий векторное поле на скалярное.",
             "То есть, в результате применения к векторному полю операции дифференцирования получается скалярное поле.",
             "Она определяет (для каждой точки), «насколько расходится входящее и исходящее из малой окрестности данной точки поле»",
             "Точнее, насколько расходятся входящий и исходящий потоки."
         ], -9),
        ([
             "«Лунтик и его друзья» — российский мультсериал, ориентированный на семейную и детскую аудиторию.",
             "Транслируется на телевидении с 1 сентября 2006 года по настоящее время.",
             "Ключевой темой стали приключения маленького пушистого существа Лунтика — космического пришельца, который родился на Луне."
         ], -3)
    ]

    read_data_en = [
        ([
             "In vector calculus, divergence is a vector operator that operates on a vector field, producing a scalar field giving the quantity of the vector field's source at each point.",
             "More technically, the divergence represents the volume density of the outward flux of a vector field from an infinitesimal volume around a given point."
         ], 42),
        ([
             "Luntik and his friends (Russian: Лунтик и его друзья) or simply Luntik (Russian: Лунтик), in its English version better known as Moonzy, is a Russian animated series for children.",
             "The title character is a purple furry alien named Luntik/Moonzy.",
             "In the first episode Moonzy is shown hatching from an egg on the moon and then falling to Earth.",
             "All of the following series take place at a forest glade near a pond where Moonzy finds a new home."
         ], 65)
    ]

    for d in read_data_ru:
        score = d[1]
        res = int(r.coleman_readability(d[0], 'ru', False))

        assert score == res

    for d in read_data_en:
        score = d[1]
        res = int(r.coleman_readability(d[0], 'en', False))

        assert score == res


def test_easy_listening():
    read_data_ru = [
        ([
             "Дивергенция — дифференциальный оператор, отображающий векторное поле на скалярное.",
             "То есть, в результате применения к векторному полю операции дифференцирования получается скалярное поле.",
             "Она определяет (для каждой точки), «насколько расходится входящее и исходящее из малой окрестности данной точки поле»",
             "Точнее, насколько расходятся входящий и исходящий потоки."
         ], 8),
        ([
             "«Лунтик и его друзья» — российский мультсериал, ориентированный на семейную и детскую аудиторию.",
             "Транслируется на телевидении с 1 сентября 2006 года по настоящее время.",
             "Ключевой темой стали приключения маленького пушистого существа Лунтика — космического пришельца, который родился на Луне."
         ], 9)
    ]

    read_data_en = [
        ([
             "In vector calculus, divergence is a vector operator that operates on a vector field, producing a scalar field giving the quantity of the vector field's source at each point.",
             "More technically, the divergence represents the volume density of the outward flux of a vector field from an infinitesimal volume around a given point."
         ], 10),
        ([
             "Luntik and his friends (Russian: Лунтик и его друзья) or simply Luntik (Russian: Лунтик), in its English version better known as Moonzy, is a Russian animated series for children.",
             "The title character is a purple furry alien named Luntik/Moonzy.",
             "In the first episode Moonzy is shown hatching from an egg on the moon and then falling to Earth.",
             "All of the following series take place at a forest glade near a pond where Moonzy finds a new home."
         ], 3)
    ]

    for d in read_data_ru:
        score = d[1]
        res = int(r.easy_listening(d[0], 'ru', False))

        assert score == res

    for d in read_data_en:
        score = d[1]
        res = int(r.easy_listening(d[0], 'en', False))

        assert score == res
