# -----------------------------------------------------------
# Класс предназначен для исчтечения жидкости из небольшого отверстия
# вертикальный цилиндрический резервуар
#
# Fires, explosions, and toxic gas dispersions :
# effects calculation and risk analysis /
# Marc J. Assael, Konstantinos E. Kakosimos.

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


class Outflow:
    def __init__(self, volume: float, height: float, pressure: float, temperature: int,
                 fill_factor: float, hole_diametr: float, density: float):
        '''
        Класс предназначен для расчета истечения газа
        :param volume: - объем, м3
        :param height: - высота, м
        :param pressure: - избыточное давление давление, МПа
        :param temperature: - температура, град.С
        :param fill_factor: - степень заполнения, м3/м3
        :param hole_diametr: - диаметр отверстия, мм
        :param density: - плотность вещества, кг/м3
        '''
        self.volume = volume
        self.height = height
        self.pressure = pressure * MPA_TO_PA + PRESSURE_ATM # перевод в абсолютное
        self.temperature = temperature + TEMP_TO_KELVIN
        self.fill_factor = fill_factor
        self.hole_diametr = hole_diametr * MM_TO_M
        self.density = density

    def flow_rate(self):
        # Начальная масса вещества в оборудовании, кг
        mass_init = self.fill_factor * self.volume * self.density
        # Начальная высота взлива, м
        height_init = self.fill_factor * self.height
        # Начальный расход жидкости
        Ah = (math.pi / 4) * math.pow(self.hole_diametr,2)
        P = self.density * GRAVITY * height_init + self.pressure
        flow_rate_init = DISCHARGE*(math.pi/4)*self.hole_diametr*self.hole_diametr*math.sqrt(2*(P-PRESSURE_ATM)*773)
        print(mass_init, height_init, flow_rate_init)
        print(P)


if __name__ == '__main__':
    cls = Outflow(6000, 15, 0, 14, 0.75, 0.1, 773)
    cls.flow_rate()


    # import math
    #
    # 0.62 * (math.pi / 4) * 0.1 * 0.1 * math.sqrt(2 * (186646 - 101325) * 773)
    # 55.92606770483945