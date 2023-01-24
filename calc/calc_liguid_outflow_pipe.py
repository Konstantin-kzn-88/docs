# скорость жидкости в трубе, м/с
# https://calculatorium.ru/physics/liquid-speed-in-the-pipeline
# v = (4Q)/(pi*D^2) - где Q - расход, м3/ч; D - диаметр в мм

# https://gidrotgv.ru/spravka-po-koefficientu-gidravlicheskogo-treniya-kalkulyatory-onlajn/
# коэф.гидравлического трения


# Re = v*D /mu - где v - скорость жидкости в трубе, м/с; D - диаметр в мм; mu - кинематическая вязкость м2/c (0.00006)
# https://petrodigest.ru/terms/vyazkost-nefti

# 1. Расход в точке за время отключения
# 2. Расход в безнапорном режиме (за время приезда бригады)
# 3. Условия перетока по учаасткам


# -----------------------------------------------------------
# Класс предназначен для исчтечения жидкости из небольшого отверстия
# трубопровод с профилем
#
# (C) 2023 Kuznetsov Konstantin, Kazan , Russian Federation
# email kuznetsovkm@yandex.ru
# -----------------------------------------------------------

import math

DISCHARGE = 0.62  # коэф.истечения, допускается брать 0.62 (p.53)
TEMP_TO_KELVIN = 273
MPA_TO_PA = math.pow(10, 6)  # МПа в Па
MM_TO_M = math.pow(10, -3)  # мм в м
PRESSURE_ATM = 101325  # атмосферное давление, Па
GRAVITY = 9.81  # ускорение свободного падения м/с2
PERSENT_BREAK = 0.99  # процент при котором остановить расчет


class Outflow:
    def __init__(self, diametr: float, lenght: float, height: float, pressure: float, temperature: int,
                 hole_diametr: float, density: float, time_step: int):
        '''
        Класс предназначен для расчета истечения газа
        :param diametr: - диаметр трубопровода, м
        :param lenght: - длина участка, м
        :param height: - высота (модуль разницы между двумя нивелирными отметками участка), м
        :param pressure: - избыточное давление давление, МПа
        :param temperature: - температура, град.С
        :param hole_diametr: - диаметр отверстия, мм
        :param density: - плотность вещества, кг/м3
        :param time_step: - временной шаг истечения, с
        :param volume: - объем, м3
        '''
        self.diametr = diametr
        self.lenght = lenght
        self.height = height
        self.pressure = pressure * MPA_TO_PA + PRESSURE_ATM  # перевод в абсолютное
        self.temperature = temperature + TEMP_TO_KELVIN
        self.fill_factor = 1 #:param fill_factor: - степень заполнения, м3/м3
        self.hole_diametr = hole_diametr * MM_TO_M
        self.density = density
        self.time_step = time_step

        self.volume = math.pi * math.pow(self.diametr / 2, 2) * self.lenght

    def result(self):
        mass_liquid = []  # масса жидкости в емкости, кг
        time = []  # время истечения, с
        fill_tank = []  # степень заполнения емкости при истачении, -
        height = []  # высота взлива, м
        pressure = []  # давление жидкости, Па
        flow_rate = []  # расход, кг/с
        delta_mass = []  # масса истечения за шаг времени, кг
        mass_leaking = []  # масса жидкости в проливе, кг

        time_init = 0

        while True:
            Ah = (math.pi / 4) * math.pow(self.hole_diametr, 2)
            if time_init == 0:
                mass_liquid.append(round(self.fill_factor * self.volume * self.density, 2))
                time.append(time_init)
                fill_tank.append(self.fill_factor)
                height.append(round(self.fill_factor * self.height, 2))
                pressure.append(round(self.density * GRAVITY * height[-1] + self.pressure, 2))
                flow_rate.append(round(DISCHARGE * Ah * math.sqrt(2 * (pressure[-1] - PRESSURE_ATM) * self.density), 10))
                delta_mass.append(round(flow_rate[-1] * self.time_step, 10))
                mass_leaking.append(0)

                time_init += self.time_step

            else:
                height.append(round(height[-1] * (mass_liquid[-1] - delta_mass[-1]) / mass_liquid[-1], 2))
                mass_liquid.append(round(mass_liquid[-1] - delta_mass[-1], 2))
                time.append(time_init)
                fill_tank.append(round(height[-1] / self.height, 2))
                pressure.append(round(self.density * GRAVITY * height[-1] + self.pressure, 2))
                flow_rate.append(round(DISCHARGE * Ah * math.sqrt(2 * (pressure[-1] - PRESSURE_ATM) * self.density), 10))
                delta_mass.append(round(flow_rate[-1] * self.time_step, 10))
                mass_leaking.append(sum(delta_mass))

                time_init += self.time_step

            print(mass_leaking[0])
            if mass_leaking[-1] >= PERSENT_BREAK * mass_liquid[0]:
                break

        return (mass_liquid,
                time,
                fill_tank,
                height,
                pressure,
                flow_rate,
                delta_mass,
                mass_leaking)


if __name__ == '__main__':
    cls = Outflow(diametr=0.15, lenght=100, height=30, pressure=0.8, temperature=5,
                 hole_diametr=0.01, density=900, time_step=1)
    print(cls.result())
