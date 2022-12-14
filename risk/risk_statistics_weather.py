class Weather:
    """
    Parametrs:
    :wind_speed: - кортеж вероятностей скоростей ветра (для скоростей 1,2,3 м/с)
    :temperature: - кортеж вероятностей температур  (для температур 10-20,20-30 и 30-максимальная)
    :cloud_cover: - вероятность облачности (0%, 60-90%, 100%)
    :wind direction: - вероятность направлений ветра Север, С - В, Восток, Ю - В, Юг,Ю - З, Запад, С - З
    """

    # базовые данные
    wind_speed = (0.04, 0.22, 0.72)
    temperature = (0.84, 0.05, 0.01)
    cloud_cover = (0.53, 0.25, 0.22)
    wind_direction = (0.06, 0.01, 0.26, 0.2, 0.1, 0.03, 0.32, 0.02)

    district = ('Агрызский', 'Азнакаевский', 'Аксубаевский', 'Актанышский', 'Алексеевский',
                'Алькеевский', 'Альметьевский', 'Апастовский', 'Арский', 'Атнинский',
                'Бавлинский', 'Балтасинский', 'Бугульминиский', 'Буинский', 'Верхнеуслонский',
                'Высокогорский', 'Дрожжановский', 'Елабужский', 'Заинский', 'Зеленодольский',
                'Кайбицкий', 'Камско-Устьинский', 'Кукморский', 'Лаишевский', 'Лениногорский',
                'Мамадышский', 'Менделеевский', 'Мензелинский', 'Муслюмовский', 'Нижнекамский',
                'Новошешминский', 'Нурлатский', 'Пестречинский', 'Рыбно-Слободский', 'Сабинский',
                'Сармановский', 'Спасский', 'Тетюшский', 'Тукаевский', 'Тюлячинский',
                'Черемшанский', 'Чистопольский', 'Ютазинский')

    @staticmethod
    def get_statistic_weather(district):
        if district in ('Бавлинский', 'Бугульминиский', 'Ютазинский',
                        'Азнакаевский', 'Лениногорский', 'Альметьевский'):
            wind_speed = (0.03, 0.25, 0.72)
            temperature = (0.87, 0.12, 0.01)
            cloud_cover = (0.50, 0.28, 0.22)
            wind_direction = (0.1, 0.15, 0.23, 0.14, 0.1, 0.02, 0.24, 0.02)
        elif district in ('Черемшанский', 'Новошешминский', 'Чистопольский',
                          'Алексеевский', 'Алькеевский', 'Спасский'):
            wind_speed = (0.05, 0.20, 0.75)
            temperature = (0.93, 0.06, 0.01)
            cloud_cover = (0.49, 0.26, 0.25)
            wind_direction = (0.09, 0.01, 0.19, 0.16, 0.1, 0.08, 0.35, 0.02)
        elif district in ('Заинский', 'Нижнекамский', 'Тукаевский',
                          'Муслюмовский', 'Мензелинский', 'Актанышский', 'Сармановский'):
            wind_speed = (0.04, 0.22, 0.74)
            temperature = (0.94, 0.05, 0.01)
            cloud_cover = (0.53, 0.25, 0.22)
            wind_direction = (0.06, 0.01, 0.26, 0.2, 0.1, 0.03, 0.32, 0.02)
        else:
            wind_speed = (0.06, 0.20, 0.74)
            temperature = (0.92, 0.07, 0.01)
            cloud_cover = (0.53, 0.25, 0.22)
            wind_direction = (0.06, 0.01, 0.26, 0.2, 0.1, 0.03, 0.32, 0.02)

        return (wind_speed, temperature, cloud_cover, wind_direction)


if __name__ == '__main__':
    print(len(Weather.district))
