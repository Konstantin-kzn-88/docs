# -----------------------------------------------------------
# Класс предназначен для исчтечения газа
#
# Fires, explosions, and toxic gas dispersions :
# effects calculation and risk analysis /
# Marc J. Assael, Konstantinos E. Kakosimos.

# (C) 2022 Kuznetsov Konstantin, Kazan , Russian Federation
# email kuznetsovkm@yandex.ru
# -----------------------------------------------------------
import math

TEMP_TO_KELVIN = 273
KMOL_TO_MOL = 0.001
R = 8.413  # газовая постоянная
PRESSURE_ATM = 0.101325  # атмосферное давление, МПа
DISCHARGE = 0.62  # коэф.истечения, допускается брать 0.62 (p.37)
MPA_TO_PA = math.pow(10, 6)  # МПа в Па
PA_TO_MPA = math.pow(10, -6)  # Па в МПа
CP = 0.01 # теплоемкость при постоянном объеме


class Outflow:
    def __init__(self, volume: float, pressure: float, temperature: int,
                 mol_weight: float, poisson_ratio: float):
        '''
        Класс предназначен для расчета истечения газа
        :param volume: - объем, м3
        :param pressure: - давление, МПа
        :param temperature: - температура, град.С
        :param mol_weight: - молекулярная масса, кг/кмоль
        :param poisson_ratio: - адиабата газа, -
        '''
        self.volume = volume
        self.pressure = pressure
        self.temperature = temperature + TEMP_TO_KELVIN
        self.mol_weight = mol_weight * KMOL_TO_MOL
        self.poisson_ratio = poisson_ratio

    def density(self) -> float:
        '''
        Плотность газа, кг/м3
        :return: плотность газа, кг/м3
        '''
        a = self.pressure * math.pow(10, 6) * self.mol_weight
        b = R * self.temperature
        return a / b

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
        square = (1 / 4) * math.pi * math.pow(hole_diameter, 2)
        k = self.coefficient_K()
        a = DISCHARGE * square * pressure * MPA_TO_PA * k
        b = math.pow(self.mol_weight / (self.poisson_ratio * R * temperature), 1 / 2)
        return float(a * b)

    def result(self, hole_diameter: float):
        weight = []  # кг
        time = []  # с
        temperature = []  # град.С
        density_gas = []  # кг/м3
        pressure = []  # МПа
        mass_flow_rate = []  # кг/с
        delta_density = []  # кг/м3
        delta_temperature = []  # град.С

        t = 0
        while True:
            time.append(t)
            if t == 0:
                temperature.append(self.temperature)
                pressure.append(self.pressure)
                density_gas.append(round(self.density(),2))
                po = round(self.flow_rate_init(hole_diameter, self.pressure, self.temperature),2)
                mass_flow_rate.append(po)
                d_po = round(-po / self.volume,2)
                delta_density.append(d_po)
                d_t = round((self.pressure / (math.pow(density_gas[0], 2) * CP)) * delta_density[0],2)
                delta_temperature.append(d_t)
            else:
                temp = round(temperature[t-1] + delta_temperature[t-1],2)
                den = round(density_gas[t-1] + delta_density[t-1],2)
                pres = round(R*temp*(den/self.mol_weight)*PA_TO_MPA,2)

                temperature.append(temp)
                pressure.append(pres)
                density_gas.append(den)

                po = round(self.flow_rate_init(hole_diameter, pressure[t], temperature[t]),2)
                mass_flow_rate.append(po)
                d_po = round(-po / self.volume,2)
                delta_density.append(d_po)
                d_t = round((self.pressure / (math.pow(density_gas[0], 2) * CP)) * delta_density[t],2)
                delta_temperature.append(d_t)


            t += 1
            if t > 5: break
        return (weight, time, temperature, density_gas, pressure, mass_flow_rate, delta_density, delta_temperature)


if __name__ == '__main__':
    cls = Outflow(50, 5, 15, 2, 1.4)
    print(cls.density())
    print(cls.coefficient_K())
    for i in cls.result(0.1):
        print(i)
