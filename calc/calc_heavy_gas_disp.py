# -----------------------------------------------------------
# Класс предназначен для расчета выброса тяжелого газа
#
# Fires, explosions, and toxic gas dispersions :
# effects calculation and risk analysis /
# Marc J. Assael, Konstantinos E. Kakosimos.

# (C) 2022 Kuznetsov Konstantin, Kazan , Russian Federation
# email kuznetsovkm@yandex.ru
# -----------------------------------------------------------

import math

GRAVITY = 9.81  # ускорение свободного падения м/с2


class Instantaneous_source:
    def __init__(self, wind_speed: int, density_air: float):
        """
        Класс предназначен для расчета выброса тяжелого газа

        wind_speed - скорость ветра, м/с
        density_air - плотность воздуха, кг/м3
        """
        self.wind_speed = wind_speed
        self.density_air = density_air

    def alpha(self, density_init: float, volume_gas: float) -> float:
        '''
        Britter and McQuaid diagram - апроксимация
        :param density_init: - плотность газа, кг/м3
        :param volume_gas: - объем газа, м3
        :return: alpha_aprox - параметр для апроксимации графика (альфа-параметр)
        Figure C5.20. Britter and McQuaid diagram [Britter & McQuaid 1988]
        '''
        g0 = (9.81 * (density_init - 1.21)) / 1.21
        alpha_aprox = (1 / 2) * math.log10(g0 * math.pow(volume_gas, 1 / 3) / math.pow(self.wind_speed, 2))
        return alpha_aprox

    def beta(self, alpha_aprox: float, concentration: float) -> float:
        '''
        Britter and McQuaid diagram - апроксимация
        :param alpha_aprox: - параметр для апроксимации графика (альфа-параметр)
        :param concentration: - концентрация, кг/м3
        :return: beta_aprox - параметр для апроксимации графика (бета-параметр)
        Figure C5.20. Britter and McQuaid diagram [Britter & McQuaid 1988]
        '''
        if concentration == 0.1:
            if alpha_aprox <= -0.44:
                beta_aprox = 0.7
            elif alpha_aprox > -0.44 and alpha_aprox <= 0.43:
                beta_aprox = 0.26 * alpha_aprox + 0.81
            elif alpha_aprox > 0.43 and alpha_aprox <= 1:
                beta_aprox = 0.93
            else:
                beta_aprox = 0.93

        elif concentration == 0.05:
            if alpha_aprox <= -0.56:
                beta_aprox = 0.85
            elif alpha_aprox > -0.56 and alpha_aprox <= 0.31:
                beta_aprox = 0.26 * alpha_aprox + 1
            elif alpha_aprox > 0.31 and alpha_aprox <= 1:
                beta_aprox = -0.12 * alpha_aprox + 1.12
            else:
                beta_aprox = -0.12 * alpha_aprox + 1.12

        elif concentration == 0.02:
            if alpha_aprox <= -0.66:
                beta_aprox = 0.95
            elif alpha_aprox > -0.66 and alpha_aprox <= 0.32:
                beta_aprox = 0.36 * alpha_aprox + 1.19
            elif alpha_aprox > 0.32 and alpha_aprox <= 1:
                beta_aprox = -0.26 * alpha_aprox + 1.38
            else:
                beta_aprox = -0.26 * alpha_aprox + 1.38

        elif concentration == 0.01:
            if alpha_aprox <= -0.71:
                beta_aprox = 1.15
            elif alpha_aprox > -0.71 and alpha_aprox <= 0.37:
                beta_aprox = 0.34 * alpha_aprox + 1.39
            elif alpha_aprox > 0.37 and alpha_aprox <= 1:
                beta_aprox = -0.38 * alpha_aprox + 1.66
            else:
                beta_aprox = -0.38 * alpha_aprox + 1.66

        elif concentration == 0.005:
            if alpha_aprox <= -0.52:
                beta_aprox = 1.48
            elif alpha_aprox > -0.52 and alpha_aprox <= 0.24:
                beta_aprox = 0.26 * alpha_aprox + 1.62
            elif alpha_aprox > 0.24 and alpha_aprox <= 1:
                beta_aprox = -0.30 * alpha_aprox + 1.75
            else:
                beta_aprox = -0.30 * alpha_aprox + 1.75

        elif concentration == 0.002:
            if alpha_aprox <= 0.27:
                beta_aprox = 1.83
            elif alpha_aprox > 0.27 and alpha_aprox <= 1:
                beta_aprox = -0.32 * alpha_aprox + 1.92
            else:
                beta_aprox = -0.32 * alpha_aprox + 1.92

        elif concentration == 0.001:
            if alpha_aprox <= -0.1:
                beta_aprox = 2.075
            elif alpha_aprox > 0.1 and alpha_aprox <= 1:
                beta_aprox = -0.27 * alpha_aprox + 2.05
            else:
                beta_aprox = -0.27 * alpha_aprox + 2.05

        else:
            beta_aprox = -0.27 * alpha_aprox + 2.05

        return beta_aprox

    def find_distance(self, beta_aprox: float, volume_gas: float) -> float:
        '''
        Функция поиска расстояния для облака
        :param beta_aprox: - параметр для апроксимации графика (бета-параметр)
        :param volume_gas: - объем газа, м3
        :return: x_dist - расстояние, м
        '''
        x_dist = math.pow(10, beta_aprox) * math.pow(volume_gas, 1 / 3)
        return x_dist

    def find_time(self, x_dist: float, volume_gas: float, density_gas: float, diametr_cloud: float):
        '''

        :param x_dist: - расстояние, м
        :param volume_gas: - объем газа, м3
        :param density_gas: - плотность газа, кг/м3
        :param diametr_cloud: - диаметр облака начальный, м
        :return: (time, b_param) - время, с и ширина облака, м
        '''
        g0 = (GRAVITY * (density_gas - self.density_air)) / self.density_air
        time = 0
        while True:
            if math.fabs((math.sqrt(diametr_cloud * diametr_cloud + 1.2 * time * math.sqrt(g0 * volume_gas))) - (
                    x_dist - 0.4 * self.wind_speed * time)) < 0.1:
                return (time, x_dist - 0.4 * self.wind_speed * time)
            time += 0.01




    def concentration(self, volume_gas: float, density_gas: float, diametr_cloud: float):
        '''

        :param volume_gas: - объем газа, м3
        :param density_gas: - плотность газа, кг/м3
        :param diametr_cloud: - диаметр облака начальный, м
        :return: (data_concentration, data_x_dist, data_width, data_time)
        концентрации кг/м3;
        расстояние, м
        ширина облака, м
        время подхода облака, с

        '''
        data_concentration = []
        data_x_dist = []
        data_width = []
        data_time = []

        limit_concentration = (0.1, 0.05, 0.02, 0.01, 0.005, 0.002, 0.001)

        for item_concentration in limit_concentration:
            alpha = self.alpha(density_gas, volume_gas)
            beta = self.beta(alpha, item_concentration)
            x_dist = self.find_distance(beta, volume_gas)
            conc_in_dist = density_gas * item_concentration
            time_arr = self.find_time(x_dist, volume_gas, density_gas, diametr_cloud)
            time_cloud = time_arr[0]
            b_eq = time_arr[1]

            data_concentration.append(conc_in_dist)
            data_x_dist.append(x_dist)
            data_width.append(b_eq)
            data_time.append(time_cloud)

        return (data_concentration, data_x_dist, data_width, data_time)


if __name__ == '__main__':
    cls = Instantaneous_source(1, 1.21)
    print(cls.concentration(10, 6, 5))
