from linguaf import syntactical_complexity as lc


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
         ], 2),
        ([
             "Luntik and his friends (Russian: Лунтик и его друзья) or simply Luntik (Russian: Лунтик), in its English version better known as Moonzy, is a Russian animated series for children.",
             "The title character is a purple furry alien named Luntik/Moonzy.",
             "In the first episode Moonzy is shown hatching from an egg on the moon and then falling to Earth.",
             "All of the following series take place at a forest glade near a pond where Moonzy finds a new home."
         ], 3)
    ]

    for d in ttr_data_ru:
        cnt = d[1]
        res = int(lc.mean_dependency_distance(d[0], 'ru'))

        assert cnt == res

    for d in ttr_data_en:
        cnt = d[1]
        res = int(lc.mean_dependency_distance(d[0], 'en'))

        assert cnt == res
