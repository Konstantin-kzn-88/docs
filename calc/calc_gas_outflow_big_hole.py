# -----------------------------------------------------------
# Класс предназначен для исчтечения газа из трубопровода на разрыв
#
# Fires, explosions, and toxic gas dispersions :
# effects calculation and risk analysis /
# Marc J. Assael, Konstantinos E. Kakosimos.

# (C) 2022 Kuznetsov Konstantin, Kazan , Russian Federation
# email kuznetsovkm@yandex.ru
# -----------------------------------------------------------
import math

DISCHARGE = 1  # коэф.истечения, допускается брать 0.95-1 при разрыве на сечение (p.37)
TEMP_TO_KELVIN = 273
KMOL_TO_MOL = 0.001
PRESSURE_ATM = 0.101325  # атмосферное давление, МПа
R = 8.413  # газовая постоянная
MPA_TO_PA = math.pow(10, 6)  # МПа в Па
VISCOSITY = 82  # Па*с (вязкость по пропану)


class Outflow:
    def __init__(self, pipe_diameter: float, pipe_length: float, pressure: float, temperature: int,
                 mol_weight: float, poisson_ratio: float):
        '''
        Класс предназначен для расчета истечения газа
        :param рipe_diameter: - диаметр трубы, м
        :param pipe_length: - длина трубы, м
        :param pressure: - давление, МПа
        :param temperature: - температура, град.С
        :param mol_weight: - молекулярная масса, кг/кмоль
        :param poisson_ratio: - адиабата газа, -
        '''
        self.pipe_diameter = pipe_diameter
        self.pipe_length = pipe_length
        self.pressure = pressure
        self.temperature = temperature + TEMP_TO_KELVIN
        self.mol_weight = mol_weight * KMOL_TO_MOL
        self.poisson_ratio = poisson_ratio

    def coefficient_K(self) -> float:
        '''
        Вычисление коэф.истечения
        :return: коэф.истечения K (p.36)
        '''
        a = self.pressure / PRESSURE_ATM
        b = math.pow((self.poisson_ratio + 1) / 2, self.poisson_ratio / (self.poisson_ratio - 1))
        # дозвуковое истечение
        if a < b:
            i = 2 * math.pow(self.poisson_ratio, 2) / (self.poisson_ratio - 1)
            j = math.pow(PRESSURE_ATM / self.pressure, 2 / self.poisson_ratio)
            k = math.pow(PRESSURE_ATM / self.pressure, (self.poisson_ratio - 1) / self.poisson_ratio)
            return math.pow(i * j * (1 - k), 1 / 2)
        # сверхзвуковое истечение
        else:
            i = 2 / (self.poisson_ratio + 1)
            j = (self.poisson_ratio + 1) / (2 * (self.poisson_ratio - 1))
            return self.poisson_ratio * math.pow(i, j)

    def flow_rate_init(self, hole_diameter: float, pressure: float, temperature: int):
        '''
        Функция расчета начального значения расхода
        :param hole_diameter: - диаметр отверстия, мм
        :param pressure: - давление, МПа
        :param temperature: - температура, град. K
        :return: расход, кг/с
        '''
        square = (1 / 4) * math.pi * math.pow(hole_diameter, 2)
        k = self.coefficient_K()
        a = DISCHARGE * square * pressure * MPA_TO_PA * k
        b = math.pow(math.fabs(self.mol_weight / (self.poisson_ratio * R * temperature)), 1 / 2)
        return float(a * b)

    def u_sound(self):
        return math.pow(self.poisson_ratio * R * self.temperature / self.mol_weight, 1 / 2)

    def reinolds(self):
        square = (1 / 4) * math.pi * math.pow(self.pipe_diameter, 2)
        po = self.pressure * MPA_TO_PA * self.mol_weight / (R * self.temperature)
        m = self.flow_rate_init(self.pipe_diameter, self.pressure, self.temperature)
        u = m / (po * square)

        return (po * u * self.pipe_diameter / VISCOSITY) * math.pow(10, 6)

    def fanning_factor(self):
        re = self.reinolds()
        if re < 2000:
            return 16 / re
        return 0.0791 * math.pow(re, -0.25)

    def time_base(self):
        us = self.u_sound()
        f = self.fanning_factor()
        a = (4/3)*(self.pipe_length/us)
        b = math.pow()

# TODO!!!!!_____________________________________

if __name__ == '__main__':
    cls = Outflow(1, 10000, 0.5, 15, 44, 1.19)
    print(cls.coefficient_K())
    print(cls.flow_rate_init(1, 0.5, 273))
    print(cls.u_sound())
    print(cls.reinolds())
    print(cls.fanning_factor())
