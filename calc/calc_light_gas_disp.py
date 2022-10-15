# -----------------------------------------------------------
# Класс предназначен для расчета выброса легкого газа
#
# Fires, explosions, and toxic gas dispersions :
# effects calculation and risk analysis /
# Marc J. Assael, Konstantinos E. Kakosimos.

# (C) 2022 Kuznetsov Konstantin, Kazan , Russian Federation
# email kuznetsovkm@yandex.ru
# -----------------------------------------------------------

import math

TEMP_TO_KELVIN = 273
WIND_HEIGHT = 10 # высота определения характеристик ветра
GRAVITY = 9.81 # ускорение свободного падения м/с2

class Instantaneous_source:

    def __init__(self, ambient_temperature: int, cloud: int,
                 wind_speed: int, density_air: float,
                 is_night: bool, is_urban_area: bool):
        """
        ambient_temperature - температура окружающего воздуха, град. С
        cloud - облачность от 0 до 8, -
        wind_speed - скорость ветра, м/с
        density_air - плотность воздуха, кг/м3
        is_night - ночное время суток, -
        is_urban_area - городская застройка, -
        """
        self.ambient_temperature = ambient_temperature + TEMP_TO_KELVIN
        self.cloud = cloud if cloud in [i for i in range(0, 9)] else 0
        self.wind_speed = wind_speed
        self.density_air = density_air
        self.is_night = is_night
        self.is_urban_area = is_urban_area

    def pasquill_atmospheric_stability_classes(self) -> str:
        """
        Классы стабильности атмосферы по Паскуиллу
        Table C5.2. Pasquill Atmospheric Stability Classes. p.222
        :@return: : pasquill_class: str: класс атмосферы
        """

        table_data = (
            ('A', 'B', 'B', 'F', 'F'),
            ('B', 'B', 'C', 'E', 'F'),
            ('B', 'B', 'C', 'D', 'E'),
            ('C', 'D', 'D', 'D', 'D'),
            ('C', 'D', 'D', 'D', 'D')
        )

        if self.wind_speed < 2:
            wind_ind = 0
        elif self.wind_speed >= 2 and self.wind_speed < 3:
            wind_ind = 1
        elif self.wind_speed >= 3 and self.wind_speed < 5:
            wind_ind = 2
        elif self.wind_speed >= 5 and self.wind_speed < 6:
            wind_ind = 3
        else:
            wind_ind = 4

        if self.cloud <= 2 and not self.is_night:
            cloud_ind = 0
        elif self.cloud <= 5 and self.cloud > 2 and not self.is_night:
            cloud_ind = 1
        elif self.cloud <= 8 and self.cloud > 5 and not self.is_night:
            cloud_ind = 2
        elif self.cloud <= 3 and self.is_night:
            cloud_ind = 3
        else:
            cloud_ind = 4

        pasquill_class = table_data[wind_ind][cloud_ind]
        return pasquill_class

    def wind_profile(self):
        """
        Экспонента профиля ветра
         Table C5.3. Wind Profile Exponent p, Eq. (C5.1).
         :@return: : p: float: экспонента профиля ветра
        """
        pasquill = ('A', 'B', 'C', 'D', 'E', 'F').index(self.pasquill_atmospheric_stability_classes())
        table_data = (
            (0.07, 0.07, 0.10, 0.15, 0.35, 0.55),
            (0.15, 0.15, 0.20, 0.25, 0.30, 0.30),
        )
        p = table_data[int(self.is_urban_area)][pasquill]
        return p

    def wind_power_law(self, ejection_height: int) -> float:
        """
        Зависимость закона силы ветра от высоты выброса
        (C5.1) p.223
        :papam: ejection_height - высота выброса, м
        :@return: : us: float: закон силы ветра от высоты выброса
        """
        p = self.wind_profile()
        us = self.wind_speed * math.pow(ejection_height / WIND_HEIGHT, p)
        return us

    def source_buoyancy_flux_parameter(self, gas_temperature: int, gas_weight: int):
        """
        Параметр плавучести
        (C5.33) p.243
        :papam: gas_temperature - температура газа, град.С
        :papam: gas_weight - масса газа, кг
        :@return: : Fbi: float: параметр плавучести газа, м4/с2
        """
        a = (GRAVITY*gas_weight)/(math.pi*self.density_air)
        b = (gas_temperature+TEMP_TO_KELVIN-self.ambient_temperature)/self.ambient_temperature
        Fbi = a*b
        return Fbi




# def atmospheric_stability(self, stability_class: str):
#     # Table C5.11. Parameters of Eq. (C5.44) as a
#     # Function of Atmospheric Stability. p247
#     data = {
#         "A": (0.18, 0.92, 0.72, 0.76),
#         "B": (0.14, 0.92, 0.53, 0.73),
#         "C": (0.10, 0.92, 0.34, 0.72),
#         "D": (0.06, 0.92, 0.15, 0.70),
#         "E": (0.045, 0.91, 0.12, 0.67),
#         "F": (0.03, 0.90, 0.08, 0.64),
#     }
#
#     return data[stability_class] if stability_class in data.keys() else data['F']


if __name__ == '__main__':
    cls = Instantaneous_source(ambient_temperature=25, cloud=0,
                               wind_speed=4, density_air=1.21,
                               is_night=False, is_urban_area=False)
    print(cls.pasquill_atmospheric_stability_classes())
    print(cls.wind_profile())
    print(cls.wind_power_law(ejection_height=2))
    print(cls.source_buoyancy_flux_parameter(147,500))
