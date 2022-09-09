class Event_tree:
    @staticmethod
    def mchs(flash_temperature: float, flow_rate: float, probability: float) -> tuple:
        """
        "Дерево собьтий" для ЛВЖ и ГЖ по приказу МЧС РФ от 10.07.2009 N 404
        "Об утверждении методики определения расчетных величин пожарного риска на производственных объектах"

        Parametrs:
        :param flash_temperature: температура вспышки, град.С
        :param flow_rate: аварийный расход, кг/с (0 - полняй разрыв)
        :param probability: частота первичного события, 1/год (например probability = 20)

        Return:
        probability scenarios
        """
        i = 0 if flash_temperature < 28 else 1

        ratio_tuple = (
            (0.2, 0.24, 0.6),
            (0.05, 0.061, 0.1),
            (0.005, 0.005, 0.08),
            (0.005, 0.005, 0.05),
            (0.035, 0.036, 0.24),
            (0.015, 0.015, 0.05),
            (0.15, 0.176, 0.6),
            (0.04, 0.042, 0.05)
        )

        if flow_rate == 0:  # gap (разрыв)
            a, b, c = ratio_tuple[i]
        elif flow_rate <= 0.5:
            a, b, c = ratio_tuple[i + 2]
        elif 0.5 < flow_rate <= 10:
            a, b, c = ratio_tuple[i + 4]
        elif flow_rate > 10:  # очень большой расход
            a, b, c = ratio_tuple[i + 6]
        else:
            a, b, c = ratio_tuple[i]

        return ("{:.2e}".format(probability * a),
                "{:.2e}".format(probability * (1 - a) * b * c),
                "{:.2e}".format(probability * (1 - a) * b * (1 - c)),
                "{:.2e}".format(probability * (1 - a) * (1 - b)))

if __name__ == '__main__':
    print(Event_tree.mchs(30, 0.3, 0.000007))
