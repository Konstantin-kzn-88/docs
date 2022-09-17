# -----------------------------------------------------------
# Класс предназначен для получения вероятности инициирующего события

#
# МЧС РФ от 10.07.2009 N 404
# РТН от 17.08.2015 N 317
# (C) 2022 Kuznetsov Konstantin, Kazan , Russian Federation
# email kuznetsovkm@yandex.ru
# -----------------------------------------------------------

class Probability:
    @staticmethod
    def probability_rosteh_device(type_obj: int) -> tuple:
        """

        Parametrs:
        :param type_obj: тип оборудования
        0 - емкость под давлением
        1 - насос герметичный
        2 - колонны конденсаторы фильтры
        3 - резервуар хранения
        4 - теплообменники
        5 - цистерны
        Return:
        probability_array множество вероятностей инициирующих событий (приказ РТН от 11 апреля 2016 г. N 144)
        """
        type_obj = -1 if type_obj > 5 else type_obj
        probabality_tuple = (
            ("{:.2e}".format(1E-6), "{:.2e}".format(1E-5)),
            ("{:.2e}".format(1E-5), "{:.2e}".format(5E-5)),
            ("{:.2e}".format(1E-5), "{:.2e}".format(1E-4)),
            ("{:.2e}".format(1E-5), "{:.2e}".format(1E-4)),
            ("{:.2e}".format(1.5E-5), "{:.2e}".format(1E-3)),
            ("{:.2e}".format(5E-7), "{:.2e}".format(4E-5))
        )
        return probabality_tuple[type_obj]

    @staticmethod
    def probability_rosteh_tube(lenght: int, diametr: int) -> tuple:
        """

        Parametrs:
        :param lenght: - длина, м
        :param lenght: - diametr, м

        Return:
        probability_tuple кортеж вероятностей инициирующих событий (приказ РТН от 11 апреля 2016 г. N 144)
        """
        if diametr < 75:
            return ("{:.2e}".format(1E-6 * lenght), "{:.2e}".format(5E-6 * lenght))
        elif diametr > 150:
            return ("{:.2e}".format(1E-7 * lenght), "{:.2e}".format(5E-7 * lenght))
        else:
            return ("{:.2e}".format(3E-7 * lenght), "{:.2e}".format(2E-7 * lenght))

    @staticmethod
    def probability_mchs_device(type_obj: int) -> tuple:
        """

        Parametrs:
        :param type_obj: тип оборудования
        0 - емкость под давлением (разрушение, 100, 50, 25, 12.5)
        1 - резервуар атм.(разрушение, 100, 25 мм)

        Return:
        probability_array множество вероятностей инициирующих событий (приказ МЧС РФ от 10.07.2009 N 404)
        """
        type_obj = -1 if type_obj > 1 else type_obj
        probabality_tuple = (
            ('1e-05', '6.2e-06', '3.8e-06', '1.7e-06', '3e-07'),
            ('3.6e-04', '1.6e-04', '8.8e-05', '1.2e-05', '5e-06')
        )
        return probabality_tuple[type_obj]

    @staticmethod
    def probability_mchs_tube(lenght: int, diametr: int) -> tuple:
        """

        Parametrs:
        :param lenght: - длина, м
        :param lenght: - diametr, м

        Return:
        probability_tuple кортеж вероятностей инициирующих событий (приказ РТН от 11 апреля 2016 г. N 144)
        """
        set_tuple = ((5.7E-6, 2.4E-6, 0, 0, 1.4E-6),
                     (2.8E-6, 1.2E-6, 4.7E-7, 0, 2.4E-7),
                     (1.9E-6, 7.9E-7, 3.1E-7, 1.3E-7, 2.5E-8),
                     (1.1E-6, 4.7E-7, 1.9E-7, 7.8E-8, 1.5E-8),
                     (4.7E-7, 2E-7, 7.9E-8, 3.4E-8, 6.4E-9),
                     (3.1E-7, 1.3E-7, 5.2E-8, 2.2E-8, 4.2E-9),
                     (2.4E-7, 9.8E-8, 3.9E-8, 1.7E-8, 3.2E-9)
                     )

        if diametr <= 50:
            probabality_tuple = tuple("{:.2e}".format(i * lenght) for i in set_tuple[0])
        elif diametr > 50 and diametr <= 100:
            probabality_tuple = tuple("{:.2e}".format(i * lenght) for i in set_tuple[1])
        elif diametr > 100 and diametr <= 150:
            probabality_tuple = tuple("{:.2e}".format(i * lenght) for i in set_tuple[2])
        elif diametr > 150 and diametr <= 250:
            probabality_tuple = tuple("{:.2e}".format(i * lenght) for i in set_tuple[3])
        elif diametr > 250 and diametr <= 600:
            probabality_tuple = tuple("{:.2e}".format(i * lenght) for i in set_tuple[4])
        elif diametr > 600 and diametr <= 900:
            probabality_tuple = tuple("{:.2e}".format(i * lenght) for i in set_tuple[5])
        elif diametr > 900:
            probabality_tuple = tuple("{:.2e}".format(i * lenght) for i in set_tuple[6])
        else:
            probabality_tuple = tuple("{:.2e}".format(i * lenght) for i in set_tuple[6])

        return probabality_tuple


if __name__ == '__main__':
    print(Probability.probability_mchs_tube(1, 100))
    print(Probability.probability_mchs_tube(1, 600))
