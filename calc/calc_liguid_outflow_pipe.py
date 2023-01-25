# -----------------------------------------------------------
# Класс предназначен для исчтечения жидкости из небольшого отверстия
# трубопровод с профилем
#
# (C) 2023 Kuznetsov Konstantin, Kazan , Russian Federation
# email kuznetsovkm@yandex.ru
# -----------------------------------------------------------

import math

GRAVITY = 9.81  # ускорение свободного падения м/с2
DISCHARGE = 0.6  # коэф.истечения, допускается брать 0.6 (p.31 РБ оценка риска на нефтедобыче)
PRESSURE_ATM = 101325  # атмосферное давление, Па


class Outflow_in_one_section_pipe:
    def __init__(self, common_rate: float, z1: int, z2: int, diametr, density, dynamic_viscosity: float, lenght: int,
                 hole: float, time_shutdown: int):
        '''
        Класс предназначен для оценки количества опасного вещества
        истекающего из трубопровода в напорном и безнапорном режиме
        :param common_rate: начальный расход,м3/ч
        :param z1: высотная отметка, м
        :param z2: высотная отметка, м
        :param diametr: диаметр, м
        :param density: плотность, кг/м3
        :param dynamic_viscosity: динамическая вязкость, кг/м*с
        :param lenght: длина участка трубопровода, м
        :param hole: отверстие истечения, м
        :param time_shutdown: время отключения, с
        '''
        self.common_rate = common_rate
        self.z1 = z1
        self.z2 = z2
        self.diametr = diametr
        self.density = density
        self.dynamic_viscosity = dynamic_viscosity
        self.lenght = lenght
        self.hole = hole
        self.time_shutdown = time_shutdown

    def __velocity(self):
        'Скорость потока при расходе, м/с'
        return (4 * self.common_rate) / (math.pi * math.pow(self.diametr, 2))

    def __reinolds(self):
        'Число Рейнольдса'
        v = self.__velocity()
        return self.density * v * self.diametr / self.dynamic_viscosity

    def __friction_factor(self):
        'Коэф.трения'
        re = self.__reinolds()
        if re < 2000:
            return 16 / re
        else:
            return 0.0791 * math.pow(re, -0.25)

    def __pressure(self):
        'Давление в месте истечения, Па'
        f = self.__friction_factor()
        v = self.__velocity()
        return 2 * f * self.density * pow(v, 2) * (self.lenght / self.diametr)

    def pressure_flow_rate(self):
        'Напорный расход, кг/с'
        delta_p = self.__pressure()
        f = self.__friction_factor()
        Ah = (math.pi / 4) * math.pow(self.hole, 2)
        return Ah * math.sqrt((delta_p * self.diametr * self.density) / (2 * f * self.lenght))

    def hydrostatic_pressure(self, z1, z2):
        'Гидростатическое давление, Па'
        return self.density * GRAVITY * (z1 - z2)

    def non_pressure_flow_rate(self, z1, z2):
        'Расход в безнапорном режиме, кг/с'
        Ah = (math.pi / 4) * math.pow(self.hole, 2)
        p1 = self.hydrostatic_pressure(z1, z2)
        return DISCHARGE * Ah * self.density * math.sqrt(2 * (p1 - PRESSURE_ATM) / self.density)


if __name__ == '__main__':
    cls = Outflow_in_one_section_pipe(common_rate=5, z1=170, z2=120, diametr=0.1, density=900,
                                      dynamic_viscosity=0.001519, lenght=1000,
                                      hole=0.01, time_shutdown=3600)
    print(cls.pressure_flow_rate())
    print(cls.hydrostatic_pressure(z1=170, z2=120))
    print(cls.non_pressure_flow_rate(z1=170, z2=120))
