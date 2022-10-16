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
MKG_TO_MG = 0.001  # мкг в мг


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
                        Fbi: float, gas_weight: int, po_gas: float, x_dist: int) -> float:
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

        :@return: (z_b,z_t,u_with_streak): tuple: - эмп. коэфциенты расслоения, средняя скорость ветра, м/с

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

    def time_in_out_peak(self, sigma_x: float, u_with_streak: float, x_dist: int) -> tuple:
        '''
        :@papam: sigma_x - коэф. дисперсии (см. def dispersion_param)
        :@papam: u_with_streak - средняя скорость ветра (см. def mean_wind_speed)
        :@papam: x_dist - дистанция м

        :@return: (t_in,t_out,t_peak): tuple: - время приходо, ухода, максимального присутвия в точке, с

        '''
        t_in = (x_dist - 2.45 * sigma_x) / u_with_streak
        t_out = (x_dist + 2.45 * sigma_x) / u_with_streak
        t_peak = x_dist / u_with_streak
        return (t_in, t_out, t_peak)

    def concentration(self, gas_weight: int, pasquill: str, mean_wind_speed: float,
                      height_rise: float, time: float, x_dist: int, y: int, z: int) -> float:
        '''
        :@papam: gas_weight - масса газа, кг
        :@papam: pasquill - класс атмосферы по Паскуиллу
        :@papam: u_with_streak - средняя скорость ветра (см. def mean_wind_speed)
        :@papam: height_rise - высота выброса, м (см. def gradual_puff_rise и final_puff_rise)
        :@papam: time - время с мщмента выброса, с (для максимального значения принять t_peak)
        :@papam: x_dist, y, z - пространственные координаты, м

        :@return: (concentration): float: - концентрация, мг/м3

        '''

        sigma_x, sigma_y, sigma_z = self.dispersion_param(pasquill, x_dist)

        first_add = 2 * gas_weight * math.pow(10, 9)
        second_add = math.pow(2 * math.pi, 3 / 2) * sigma_x * sigma_y * sigma_z
        third_add = math.exp(-(math.pow(x_dist - mean_wind_speed * time, 2)) / (2 * math.pow(sigma_x, 2)))
        fourth_add = math.exp(-(math.pow(y, 2)) / (2 * math.pow(sigma_y, 2)))
        fifth_add = math.exp(-(math.pow(height_rise - z, 2)) / (2 * math.pow(sigma_z, 2)))
        six_add = math.exp(-(math.pow(height_rise + z, 2)) / (2 * math.pow(sigma_z, 2)))

        concentration = (first_add / second_add) * third_add * fourth_add * (fifth_add + six_add)
        return concentration * MKG_TO_MG


class Continuous_source:
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

    def height_source_correction(self, us: float, gas_exit_speed: float,
                                 ejection_diametr: int, ejection_height: int):
        '''
        Функция корректироваки высоты выброса

        :@papam: us - сила ветра, м/с (см. def wind_power_law)
        :@papam: gas_exit_speed - скорость выброса газа, м/с
        :@papam: ejection_diametr - диаметр выброса, м
        :@papam: hs_with_steak - корректированная высота выброса, м

        :@return: : us: float: закон силы ветра от высоты выброса
        '''
        if gas_exit_speed / us < 1.5:
            hs_with_steak = ejection_height + 2 * ejection_diametr * (gas_exit_speed / us - 1.5)
        else:
            hs_with_steak = ejection_height
        return hs_with_steak

    def selecting_plume_rise(self, pasquill: str, gas_exit_speed: float,
                             gas_temperature: int, ejection_diametr: int) -> float:
        '''
        Функция для опредления, что больше воздействует импульс или плавучесть
        Table C5.4. Equations for Selecting Plume Rise Because of Buoyancy or Momentum
        :@papam: pasquill - класс атмосферы по Паскуиллу
        :@papam: gas_exit_speed - скорость выброса газа, м/с
        :@papam: gas_temperature - температура выброса газа, град.С
        :@papam: ejection_diametr - диаметр выброса, м
        :@return: delta_T_c: float: температура, К (для опредления, что больше воздействует импульс или плавучесть)
        '''
        gas_temperature = gas_temperature + TEMP_TO_KELVIN
        Fb = GRAVITY * gas_exit_speed * math.pow(ejection_diametr, 2) * (
                (gas_temperature - self.ambient_temperature) / (4 * gas_temperature))
        if pasquill in ('A', 'B', 'C', 'D'):
            if Fb < 55:
                delta_T_c = 0.0297 * gas_temperature * math.pow(gas_exit_speed / math.pow(ejection_diametr, 2), 1 / 3)
            else:
                delta_T_c = 0.00575 * gas_temperature * math.pow(gas_exit_speed / math.pow(ejection_diametr, 2), 1 / 3)
        else:
            # 0.02  и 0.035 эмпирические коэф. p.245
            k = 0.02 if pasquill == 'E' else 0.035
            s = (GRAVITY / self.ambient_temperature) * k
            delta_T_c = 0.019582 * gas_temperature * gas_exit_speed * math.sqrt(s)
        return delta_T_c

    def maximum_distance_x(self, pasquill: str, gas_exit_speed: float,
                           gas_temperature: int, ejection_diametr: int, delta_T_c: float, us: float) -> float:
        '''
        Функция расчета максимальной дистанции
        Table C5.5. Equations for Calculating Distance, xf, of Maximum Plume Rise
        :@papam: pasquill - класс атмосферы по Паскуиллу
        :@papam: gas_exit_speed - скорость выброса газа, м/с
        :@papam: gas_temperature - температура выброса газа, град.С
        :@papam: ejection_diametr - диаметр выброса, м
        :@delta_T_c: nt - диаметр выброса, м
        :@papam: us - сила ветра от высоты выброса (см. def wind_power_law)
        :@return: x_max: float: расстояние, м
        '''
        gas_temperature = gas_temperature + TEMP_TO_KELVIN
        Fb = GRAVITY * gas_exit_speed * math.pow(ejection_diametr, 2) * (
                (gas_temperature - self.ambient_temperature) / (4 * gas_temperature))

        if pasquill in ('A', 'B', 'C', 'D'):
            if Fb < 55:
                x_max = 49 * math.pow(Fb, 5 / 8)
            else:
                x_max = 119 * math.pow(Fb, 2 / 5)
            if (gas_temperature - self.ambient_temperature) < delta_T_c and Fb == 0:
                x_max = 4 * ejection_diametr * math.pow(gas_exit_speed + 3 * us, 2) / (gas_exit_speed * us)
        else:
            # 0.02  и 0.035 эмпирические коэф. p.245
            k = 0.02 if pasquill == 'E' else 0.035
            s = (GRAVITY / self.ambient_temperature) * k
            if (gas_temperature - self.ambient_temperature) < delta_T_c:
                x_max = math.pi * 0.50 * us / math.sqrt(s)
            else:
                x_max = 2.0715 * us / math.sqrt(s)
        return x_max

    def gradual_puff_rise(self, pasquill: str, gas_exit_speed: float,
                          gas_temperature: int, ejection_diametr: int,
                          delta_T_c: float, us: float, hs_with_steak: float, x_dist: float) -> float:
        '''
        Функция постепенного подъема выброса (he - параметр),
        до величины максимальной дистанции x_max (def maximum_distance_x)

        :@papam: pasquill - класс атмосферы по Паскуиллу
        :@papam: gas_exit_speed - скорость выброса газа, м/с
        :@papam: gas_temperature - температура выброса газа, град.С
        :@papam: ejection_diametr - диаметр выброса, м
        :@delta_T_c: nt - диаметр выброса, м
        :@papam: us - сила ветра от высоты выброса (см. def wind_power_law)
        :@papam: hs_with_steak - откорректированная высота выброса, м (см. def height_source_correction)
        :@papam: x_dist - дистанция м
        :@return: he: float: подъем, м
        '''
        gas_temperature = gas_temperature + TEMP_TO_KELVIN

        Fb = GRAVITY * gas_exit_speed * math.pow(ejection_diametr, 2) * (
                (gas_temperature - self.ambient_temperature) / (4 * gas_temperature))

        x_max = self.maximum_distance_x(pasquill, gas_exit_speed, gas_temperature, ejection_diametr, delta_T_c, us)
        x_dist = x_dist if x_dist < x_max else x_max

        # 0.02  и 0.035 эмпирические коэф. p.245
        k = 0.02 if pasquill == 'E' else 0.035
        s = (GRAVITY / self.ambient_temperature) * k

        Fm = math.pow(gas_exit_speed, 2) * math.pow(ejection_diametr, 2) * (
                self.ambient_temperature / (4 * gas_temperature))

        betta_j = (1 / 3) + us / gas_exit_speed


        if pasquill in ('A', 'B', 'C', 'D', 'E', 'F') and (gas_temperature - self.ambient_temperature) >= delta_T_c:
            a = 1.60 * math.pow(Fb * math.pow(x_dist, 2), 1 / 3) / us
            he = hs_with_steak + a
        else:
            if pasquill in ('A', 'B', 'C', 'D'):
                a = math.pow(betta_j, 2) * math.pow(us, 2)
                b = 1.60 * math.pow(3 * Fm * x_dist / a, 1 / 3)
                he = hs_with_steak + b
            else:
                a = 3 * Fm
                b = math.sin(x_dist * math.sqrt(s) / us)
                c = math.pow(betta_j, 2) * us * math.sqrt(s)

                he = hs_with_steak + math.pow(a * (b / c), 1 / 3)

        return he


if __name__ == '__main__':
    # #instantaneous_source
    # cls = Instantaneous_source(ambient_temperature=25, cloud=0,
    #                            wind_speed=4, density_air=1.21,
    #                            is_night=False, is_urban_area=False)
    # pasquill = (cls.pasquill_atmospheric_stability_classes())
    # p = (cls.wind_profile())
    # us = (cls.wind_power_law(ejection_height=2))
    # Fbi = (cls.source_buoyancy_flux_parameter(147, 500))
    # x_max = cls.maximum_distance_x(pasquill, us, Fbi)
    # he_max = cls.gradual_puff_rise(ejection_height=2, pasquill=pasquill, us=us,
    #                                Fbi=Fbi, gas_weight=500, po_gas=3.15, x_dist=x_max)
    #
    # x = 1000
    # he_r = cls.gradual_puff_rise(ejection_height=2, pasquill=pasquill, us=us, Fbi=Fbi, gas_weight=500, po_gas=3.15,
    #                              x_dist=x) if x <= he_max else cls.final_puff_rise(ejection_height=2, pasquill=pasquill,
    #                                                                                us=us, Fbi=Fbi, gas_weight=500,
    #                                                                                po_gas=3.15, x_dist=x)
    #
    # sigma_x, sigma_y, sigma_z = cls.dispersion_param(pasquill=pasquill, x_dist=x)
    #
    # u_mean = cls.mean_wind_speed(he_r, he_max, sigma_z)[2]
    #
    # t_in, t_out, t_peak = cls.time_in_out_peak(sigma_x, u_mean, x)
    #
    # print(cls.concentration(500, pasquill, u_mean, he_r, t_peak, x, 0, 2))

    # Continuous
    cls = Continuous_source(ambient_temperature=7, cloud=5,
                            wind_speed=2, density_air=1.21,
                            is_night=True, is_urban_area=False)

    pasquill = (cls.pasquill_atmospheric_stability_classes())
    print(cls.wind_profile())
    us = (cls.wind_power_law(25))
    hs_with_steak = cls.height_source_correction(us, 4, 1, 25)
    dt = cls.selecting_plume_rise(pasquill, 4, 127, 1)
    x_max = cls.maximum_distance_x(pasquill, 4, 127, 1, dt, us)
    print(cls.gradual_puff_rise(pasquill, 4, 127, 1, dt, us, hs_with_steak, 50))
