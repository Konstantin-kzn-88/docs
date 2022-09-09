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
    def probability_rosteh(type_obj: int, length: float) -> tuple:
        """

        Parametrs:
        :param type_obj: тип оборудования
        0 - трубопровод
        1 - емкость под давлением
        2 - насос герметичный
        3 - колонны конденсаторы фильтры
        4 - резервуар хранения
        5 - теплообменники
        6 - цистерны
        Return:
        probability_array множество вероятностей инициирующих событий (приказ РТН от 11 апреля 2016 г. N 144)
        """
        type_obj = -1 if type_obj > 6 else type_obj
        probabality_tuple = (
            ("{:.2e}".format(3 * pow(10, -7) * length), "{:.2e}".format(2 * pow(10, -6) * length)),
            ("{:.2e}".format(1 * pow(10, -6)), "{:.2e}".format(1 * pow(10, -5))),
            ("{:.2e}".format(1 * pow(10, -5)), "{:.2e}".format(5 * pow(10, -5))),
            ("{:.2e}".format(1 * pow(10, -5)), "{:.2e}".format(1 * pow(10, -4))),
            ("{:.2e}".format(1 * pow(10, -5)), "{:.2e}".format(1 * pow(10, -4))),
            ("{:.2e}".format(1.5 * pow(10, -5)), "{:.2e}".format(1 * pow(10, -3))),
            ("{:.2e}".format(5 * pow(10, -7)), "{:.2e}".format(4 * pow(10, -5)))
        )
        return probabality_tuple[type_obj]


if __name__ == '__main__':
    print(Probability.probability_rosteh(0, 25))
    print(Probability.probability_rosteh(1, 0))
    print(Probability.probability_rosteh(2, 0))
    print(Probability.probability_rosteh(3, 0))
    print(Probability.probability_rosteh(4, 0))
    print(Probability.probability_rosteh(5, 0))
    print(Probability.probability_rosteh(6, 0))
