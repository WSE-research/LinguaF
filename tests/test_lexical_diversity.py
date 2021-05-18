from linguaf import lexical_diversity as ld


def test_lexical_density():
    ld_data_ru = [
        ([
             "Дивергенция — дифференциальный оператор, отображающий векторное поле на скалярное.",
             "То есть, в результате применения к векторному полю операции дифференцирования получается скалярное поле.",
             "Она определяет (для каждой точки), «насколько расходится входящее и исходящее из малой окрестности данной точки поле»",
             "Точнее, насколько расходятся входящий и исходящий потоки."
         ], 70),
        ([
             "«Лунтик и его друзья» — российский мультсериал, ориентированный на семейную и детскую аудиторию.",
             "Транслируется на телевидении с 1 сентября 2006 года по настоящее время.",
             "Ключевой темой стали приключения маленького пушистого существа Лунтика — космического пришельца, который родился на Луне."
         ], 70)
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
        res = int(ld.lexical_density(d[0], 'ru'))

        assert cnt == res

    for d in ld_data_en:
        cnt = d[1]
        res = int(ld.lexical_density(d[0], 'en'))

        assert cnt == res


def test_type_token_ratio():
    ttr_data_ru = [
        ([
             "Дивергенция — дифференциальный оператор, отображающий векторное поле на скалярное.",
             "То есть, в результате применения к векторному полю операции дифференцирования получается скалярное поле.",
             "Она определяет (для каждой точки), «насколько расходится входящее и исходящее из малой окрестности данной точки поле»",
             "Точнее, насколько расходятся входящий и исходящий потоки."
         ], 85),
        ([
             "«Лунтик и его друзья» — российский мультсериал, ориентированный на семейную и детскую аудиторию.",
             "Транслируется на телевидении с 1 сентября 2006 года по настоящее время.",
             "Ключевой темой стали приключения маленького пушистого существа Лунтика — космического пришельца, который родился на Луне."
         ], 100)
    ]

    ttr_data_en = [
        ([
             "In vector calculus, divergence is a vector operator that operates on a vector field, producing a scalar field giving the quantity of the vector field's source at each point.",
             "More technically, the divergence represents the volume density of the outward flux of a vector field from an infinitesimal volume around a given point."
         ], 68),
        ([
             "Luntik and his friends (Russian: Лунтик и его друзья) or simply Luntik (Russian: Лунтик), in its English version better known as Moonzy, is a Russian animated series for children.",
             "The title character is a purple furry alien named Luntik/Moonzy.",
             "In the first episode Moonzy is shown hatching from an egg on the moon and then falling to Earth.",
             "All of the following series take place at a forest glade near a pond where Moonzy finds a new home."
         ], 85)
    ]

    for d in ttr_data_ru:
        cnt = d[1]
        res = int(ld.type_toke_ratio(d[0], 'ru', True))

        assert cnt == res

    for d in ttr_data_en:
        cnt = d[1]
        res = int(ld.type_toke_ratio(d[0], 'en', True))

        assert cnt == res


def test_mean_dependency_distance():
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
        res = int(ld.mean_dependency_distance(d[0], 'ru'))

        assert cnt == res

    for d in ttr_data_en:
        cnt = d[1]
        res = int(ld.mean_dependency_distance(d[0], 'en'))

        assert cnt == res
