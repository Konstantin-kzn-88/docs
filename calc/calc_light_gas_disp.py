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
WIND_HEIGHT = 10  # высота определения характеристик ветра
GRAVITY = 9.81  # ускорение свободного падения м/с2


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
        :@papam: ejection_height - высота выброса, м
        :@return: : us: float: закон силы ветра от высоты выброса
        """
        p = self.wind_profile()
        us = self.wind_speed * math.pow(ejection_height / WIND_HEIGHT, p)
        return us

    def source_buoyancy_flux_parameter(self, gas_temperature: int, gas_weight: int) -> float:
        """
        Параметр плавучести
        (C5.33) p.243
        :@papam: gas_temperature - температура газа, град.С
        :@papam: gas_weight - масса газа, кг
        :@return: : Fbi: float: параметр плавучести газа, м4/с2
        """
        a = (GRAVITY * gas_weight) / (math.pi * self.density_air)
        b = (gas_temperature + TEMP_TO_KELVIN - self.ambient_temperature) / self.ambient_temperature
        Fbi = a * b
        return Fbi

    def maximum_distance_x(self, pasquill: str, us: float, Fbi: float) -> float:
        '''
        Функция расчета максимальной дистанции
        :@papam: pasquill - класс атмосферы по Паскуиллу
        :@papam: us - сила ветра от высоты выброса (см. def wind_power_law)
        :@papam: Fbi - параметр плавучести (см. def source_buoyancy_flux_parameter)
        :@return: x_max: float: расстояние, м
        '''
        if pasquill in ('A', 'B', 'C', 'D'):
            if Fbi <= 300 * math.pow(us, 2 / 3):
                x_max = 12 * math.pow(Fbi, 1 / 2) * math.pow(us, 1 / 3)
            else:
                x_max = 50 * math.pow(Fbi, 1 / 4) * math.pow(us, 1 / 2)
        else:
            # 0.02  и 0.035 эмпирические коэф. p.245
            k = 0.02 if pasquill == 'E' else 0.035
            s = (GRAVITY / self.ambient_temperature) * k
            x_max = math.pi * us / math.sqrt(s)
        return x_max

    def gradual_puff_rise(self, ejection_height: int, pasquill: str, us: float,
                          Fbi: float, gas_weight: int, po_gas: float, x_dist) -> float:
        '''
        Функция постепенного подъема выброса (he - параметр),
        до величины максимальной дистанции x_max (def maximum_distance_x)

        :@papam: ejection_height - высота выброса, м
        :@papam: pasquill - класс атмосферы по Паскуиллу
        :@papam: us - сила ветра от высоты выброса (см. def wind_power_law)
        :@papam: Fbi - параметр плавучести (см. def source_buoyancy_flux_parameter)
        :@papam: gas_weight - масса газа, кг
        :@papam: po_gas - плотность газа, кг/м3
        :@papam: x_dist - дистанция м
        :@return: he: float: подъем, м
        '''
        x_max = self.maximum_distance_x(pasquill, us, Fbi)
        x_dist = x_dist if x_dist < x_max else x_max
        C_CONST = 0.64  # эмпирический коэф. p.245 (коэф. поглощения)
        # 0.02  и 0.035 эмпирические коэф. p.245
        k = 0.02 if pasquill == 'E' else 0.035
        s = (GRAVITY / self.ambient_temperature) * k

        if pasquill in ('A', 'B', 'C', 'D'):
            a = 2 * Fbi * math.pow(x_dist, 2)
            b = math.pow(C_CONST, 3) * math.pow(us, 2)
            he = ejection_height + math.pow(a / b, 1 / 4)
        else:
            r_cloud = math.pow(3 * gas_weight / (4 * math.pi * po_gas), 1 / 3)
            a = (4 * Fbi) / (math.pow(C_CONST, 3) * s)
            b = 1 - math.cos(x_dist * math.sqrt(s) / us)
            c = a * b
            d = math.pow(r_cloud / C_CONST, 4)
            he = ejection_height + math.pow(c + d, 1 / 4) - (r_cloud / C_CONST)
        return he

    def final_puff_rise(self, ejection_height: int, pasquill: str, us: float,
                        Fbi: float, gas_weight: int, po_gas: float, x_dist) -> float:
        '''
        Функция финальной высоты выброса (he - параметр),
        после величины максимальной дистанции x_max (def maximum_distance_x)

        :@papam: ejection_height - высота выброса, м
        :@papam: pasquill - класс атмосферы по Паскуиллу
        :@papam: us - сила ветра от высоты выброса (см. def wind_power_law)
        :@papam: Fbi - параметр плавучести (см. def source_buoyancy_flux_parameter)
        :@papam: gas_weight - масса газа, кг
        :@papam: po_gas - плотность газа, кг/м3
        :@papam: x_dist - дистанция м
        :@return: he: float: подъем, м
        '''
        x_max = self.maximum_distance_x(pasquill, us, Fbi)
        x_dist = x_dist if x_dist < x_max else x_max
        C_CONST = 0.64  # эмпирический коэф. p.245 (коэф. поглощения)
        # 0.02  и 0.035 эмпирические коэф. p.245
        k = 0.02 if pasquill == 'E' else 0.035
        s = (GRAVITY / self.ambient_temperature) * k
        if pasquill in ('A', 'B', 'C', 'D'):
            a = 2 * Fbi * math.pow(x_dist, 2)
            b = math.pow(C_CONST, 3) * math.pow(us, 2)
            he = ejection_height + math.pow(a / b, 1 / 4)
        else:
            r_cloud = math.pow(3 * gas_weight / (4 * math.pi * po_gas), 1 / 3)
            a = (8 * Fbi) / (math.pow(C_CONST, 3) * s)
            d = math.pow(r_cloud / C_CONST, 4)
            he = ejection_height + math.pow(a + d, 1 / 4) - (r_cloud / C_CONST)
        return he

    def atmospheric_stability_param(self, pasquill: str) -> tuple:
        '''
        Параметры атмосферной стабильности
        Table C5.11. Parameters of Eq. (C5.44) as a
        Function of Atmospheric Stability. p247

        :@papam: pasquill - класс атмосферы по Паскуиллу
        :@return: : tuple: кортеж параметров (a,b,c,d)
        '''

        # Table C5.11. Parameters of Eq. (C5.44) as a
        # Function of Atmospheric Stability. p247
        data = {
            "A": (0.18, 0.92, 0.72, 0.76),
            "B": (0.14, 0.92, 0.53, 0.73),
            "C": (0.10, 0.92, 0.34, 0.72),
            "D": (0.06, 0.92, 0.15, 0.70),
            "E": (0.045, 0.91, 0.12, 0.67),
            "F": (0.03, 0.90, 0.08, 0.64),
        }

        return data[pasquill] if pasquill in data.keys() else data['F']

    def dispersion_param(self, pasquill: str, x_dist: int):
        '''
        Функция параметров дисперсии
        :@papam: pasquill - класс атмосферы по Паскуиллу
        :@papam: x_dist - дистанция м
        :@return: sigma: tuple: кортеж параметров (sigma_x, sigma_y, sigma_z)
        '''
        a, b, c, d = self.atmospheric_stability_param(pasquill)
        sigma_x = a * math.pow(x_dist / 1, b)
        sigma_y = sigma_x
        sigma_z = c * math.pow(x_dist / 1, d)
        return (sigma_x, sigma_y, sigma_z)

    def mean_wind_speed(self, height_rise: float, height_rise_max: float, sigma_z: float) -> tuple:
        '''
        Функция средней скорости ветра
        :@papam: height_rise - высота выброса, м (см. def gradual_puff_rise и final_puff_rise)
        :@papam: height_rise_max - высота выброса при расстоянии для
                                   максимального подъема, м (см. def gradual_puff_rise)
        :@papam: sigma_z - коэф. дисперсии (см. def dispersion_param)

        :@return: (z_b,z_t,u_with_streak): tuple: - средняя скорость ветра, м/с

        '''
        p = self.wind_profile()

        if height_rise - 2.15 * sigma_z > 2:
            z_b = height_rise - 2.15 * sigma_z
        else:
            z_b = 2

        if height_rise + 2.15 * sigma_z < height_rise_max:
            z_t = height_rise + 2.15 * sigma_z
        else:
            z_t = height_rise_max

        a = (z_t - z_b) * math.pow(WIND_HEIGHT, p) * (1 + p)
        b = self.wind_speed / a
        c = math.pow(z_t, 1 + p) - math.pow(z_b, 1 + p)
        u_with_streak = b * c

        return (z_b, z_t, u_with_streak)


if __name__ == '__main__':
    cls = Instantaneous_source(ambient_temperature=25, cloud=0,
                               wind_speed=4, density_air=1.21,
                               is_night=False, is_urban_area=False)
    pasquill = (cls.pasquill_atmospheric_stability_classes())
    p = (cls.wind_profile())
    us = (cls.wind_power_law(ejection_height=2))
    Fbi = (cls.source_buoyancy_flux_parameter(147, 500))
    x_max = cls.maximum_distance_x(pasquill, us, Fbi)
    he_max = cls.gradual_puff_rise(ejection_height=2, pasquill=pasquill, us=us,
                                Fbi=Fbi, gas_weight=500, po_gas=3.15, x_dist=x_max)

    he_100 = cls.gradual_puff_rise(ejection_height=2, pasquill=pasquill, us=us,
                                Fbi=Fbi, gas_weight=500, po_gas=3.15, x_dist=100)

    sigma_z = cls.dispersion_param(pasquill=pasquill, x_dist=100)[2]

    print(cls.mean_wind_speed(he_100, he_max, sigma_z))
