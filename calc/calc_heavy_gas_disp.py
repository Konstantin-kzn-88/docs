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

TEMP_TO_KELVIN = 273
WIND_HEIGHT = 10  # высота определения характеристик ветра
GRAVITY = 9.81  # ускорение свободного падения м/с2
MKG_TO_MG = 0.001  # мкг в мг


class Instantaneous_source:
    def __init__(self, wind_speed: int, density_air: float):
        """
        wind_speed - скорость ветра, м/с
        density_air - плотность воздуха, кг/м3
        """
        self.wind_speed = wind_speed
        self.density_air = density_air

    def alpha(self, density_init: float, volume_gas: float):
        g0 = (9.81 * (density_init - 1.21)) / 1.21
        alpha_aprox = (1 / 2) * math.log10(g0 * math.pow(volume_gas, 1 / 3) / math.pow(self.wind_speed, 2))
        return alpha_aprox

    def beta(self, alpha_aprox, concentration_ratio):
        if concentration_ratio == 0.1:
            if alpha_aprox <= -0.44:
                beta_aprox = 0.7
            elif alpha_aprox > -0.44 and alpha_aprox <= 0.43:
                beta_aprox = 0.26 * alpha_aprox + 0.81
            elif alpha_aprox > 0.43 and alpha_aprox <= 1:
                beta_aprox = 0.93
            else:
                beta_aprox = 0.93

        elif concentration_ratio == 0.05:
            if alpha_aprox <= -0.56:
                beta_aprox = 0.85
            elif alpha_aprox > -0.56 and alpha_aprox <= 0.31:
                beta_aprox = 0.26 * alpha_aprox + 1
            elif alpha_aprox > 0.31 and alpha_aprox <= 1:
                beta_aprox = -0.12 * alpha_aprox + 1.12
            else:
                beta_aprox = -0.12 * alpha_aprox + 1.12

        elif concentration_ratio == 0.02:
            if alpha_aprox <= -0.66:
                beta_aprox = 0.95
            elif alpha_aprox > -0.66 and alpha_aprox <= 0.32:
                beta_aprox = 0.36 * alpha_aprox + 1.19
            elif alpha_aprox > 0.32 and alpha_aprox <= 1:
                beta_aprox = -0.26 * alpha_aprox + 1.38
            else:
                beta_aprox = -0.26 * alpha_aprox + 1.38

        elif concentration_ratio == 0.01:
            if alpha_aprox <= -0.71:
                beta_aprox = 1.15
            elif alpha_aprox > -0.71 and alpha_aprox <= 0.37:
                beta_aprox = 0.34 * alpha_aprox + 1.39
            elif alpha_aprox > 0.37 and alpha_aprox <= 1:
                beta_aprox = -0.38 * alpha_aprox + 1.66
            else:
                beta_aprox = -0.38 * alpha_aprox + 1.66

        elif concentration_ratio == 0.005:
            if alpha_aprox <= -0.52:
                beta_aprox = 1.48
            elif alpha_aprox > -0.52 and alpha_aprox <= 0.24:
                beta_aprox = 0.26 * alpha_aprox + 1.62
            elif alpha_aprox > 0.24 and alpha_aprox <= 1:
                beta_aprox = -0.30 * alpha_aprox + 1.75
            else:
                beta_aprox = -0.30 * alpha_aprox + 1.75

        elif concentration_ratio == 0.002:
            if alpha_aprox <= 0.27:
                beta_aprox = 1.83
            elif alpha_aprox > 0.27 and alpha_aprox <= 1:
                beta_aprox = -0.32 * alpha_aprox + 1.92
            else:
                beta_aprox = -0.32 * alpha_aprox + 1.92

        elif concentration_ratio == 0.001:
            if alpha_aprox <= -0.1:
                beta_aprox = 2.075
            elif alpha_aprox > 0.1 and alpha_aprox <= 1:
                beta_aprox = -0.27 * alpha_aprox + 2.05
            else:
                beta_aprox = -0.27 * alpha_aprox + 2.05

        else:
            beta_aprox = -0.27 * alpha_aprox + 2.05

        return beta_aprox

    def find_distance(self,beta_aprox:float, volume_gas: float):
        return math.pow(10,beta_aprox) * math.pow(volume_gas,1/3)

