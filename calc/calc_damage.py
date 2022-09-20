# -----------------------------------------------------------
# Класс предназначен для расчета ущерба
#
# (C) 2021 Kuznetsov Konstantin, Kazan , Russian Federation
# email kuznetsovkm@yandex.ru

# -----------------------------------------------------------
import random

from prettytable import PrettyTable
import math

CONST = 0.5  # часть ущерба


class Damage:

    def direct_damage(self, volume=0, diametr=114,  # полный ущерб
                      lenght=1000, cost_sub=0.012,
                      part_sub=1):
        """
        Для стационарного объекта
        :@param volume: объем в м3
        Для линейного объекта объекта
        :@param diametr, диаметр трубы в мм
        :@param length: длина, м
        For all
        :@param cost_sub, стоимость млн.руб/м3
        :@param part_sub, часть утерянного вещества

        :@return:
        - ущерб, млн
        """
        if diametr == 0 and lenght == 0:  # если расчитываем стац.объект
            new_obj = (0.0036 * volume + 0.6061)  # стоимость нового объекта, млн
            # данные апроксимировал с коэф.0.2 с http://rezervuarstroy.ru/page/prajs-listy.html
            sub_loss = cost_sub * volume * part_sub  # стомость вещества с потерей доли
            # (т.к. бывают разные сценарии (пожар, взрыв, шар и пр.)
            dis_obj = new_obj * 0.2  # примерно 20% на демонтаж объекта

            direct_damage = new_obj + sub_loss + dis_obj  # строительство + потеря вещества + демонтаж

        elif volume == 0:  # если расчитываем линейный объект
            new_obj = \
                ((0.0195 * diametr + 1.0519) * lenght / 1000)  # стоимость нового объекта, млн
            # данные апроксимировал с коэф.0.2 с http://www.ozti.org/upload/iblock/637/COSTS.pdf
            volume_lin = \
                math.pi * math.pow(diametr / 2000, 2) * lenght

            sub_loss = cost_sub * volume_lin * part_sub  # стомость вещества с потерей доли
            # (т.к. бывают разные сценарии (пожар, взрыв, шар и пр.)
            dis_obj = new_obj * 0.2  # примерно 20% на демонтаж объекта

            direct_damage = new_obj + sub_loss + dis_obj  # строительство + потеря вещества + демонтаж
        else:
            direct_damage = 3  # если все вызвано с 0 то ущерб принять 3 млн.

        direct_damage = round(direct_damage * CONST, 2)  # уменьшим ущерб
        # если ущерб меньше 0.1 млн, то
        if direct_damage < 0.1:
            direct_damage = round(random.uniform(0.21, 0.22), 2)

        return direct_damage

    def se_damage(self, death_person=1, injured_person=1):  # (социально-экономический)
        """
        :@param: death_person - погибшие
        :@param: injured_person - пострадавшие

        :@return:
        - ущерб, млн.руб
        """
        se_damage = (death_person *
                     (6000 * 18 * 12 + 2000000) +  # ФЗ-225
                     injured_person * 150000) * math.pow(10, -6)

        se_damage = round(se_damage*CONST, 2)
        return se_damage

    def damage_air(self, m_out_spill=3.4):
        """
        :@param: m_out_spill,  сколько испарилось тонны;
        :@return:
        - ущерб, млн.руб

        При расчете ущерба от загрязнения воздуха при расчете ущерба
        принимались следующие коэффициенты:
        Загрязняющее вещество - Углеводороды С1-С5
        Норматив платы, руб./т (Мсрi) - 108
        Коэффициент за 2021 г. (Нплi) - 1,08
        Коэффициент Кср - 25 (ПРИКАЗ Минприроды) от 9 января 2017 г. N 3



        См. Постановление Правительства РФ от 11.09.2020 N 1393
        "О применении в 2021 году ставок платы за негативное
        воздействие на окружающую среду"

        Постановление Правительства РФ от 13.09.2016 № 913
        «О ставках платы за негативное воздействие на окружающую
        среду и дополнительных коэффициентах»
        """

        tax_1_tonn = 108 * 1 * 1.08 * 25
        damage_air = round(m_out_spill * tax_1_tonn * pow(10, -6), 4)

        return damage_air

    def damage_air_fire(self, m_in_spill=50.5):
        """
        :@param: m_in_spill,  сколько осталось гореть тонны;
        :@return:
        - ущерб, млн.руб

        ____________________________________________________
        Ущерб от загрязнения атмосферного воздуха
        при сгорании 1 тонны нефти:
        ____________________________________________________
        Загрязняющее вещество - Оксид углерода (СО)* (0,798т)
        Норматив платы, руб./т (Мсрi) - 1.6
        ____________________________________________________
        Загрязняющее вещество - Оксиды азота (NОx)* (0,066т)
        Норматив платы, руб./т (Мсрi) - 138,8
        ____________________________________________________
        Загрязняющее вещество - Оксиды серы (SO2)** (0,26т)
        Норматив платы, руб./т (Мсрi) - 45,4
        ____________________________________________________
        Загрязняющее вещество - Сероводород (H2S)* (0,001т)
        Норматив платы, руб./т (Мсрi) - 686,2
        ____________________________________________________
        Загрязняющее вещество - Сажа (С)** (1.615т)
        Норматив платы, руб./т (Мсрi) - 109,5
        ____________________________________________________
        Загрязняющее вещество - Синильная кислота (НСN)* (0,01т)
        Норматив платы, руб./т (Мсрi) - 547,4
        ____________________________________________________
        Загрязняющее вещество - Формальдегид (HCHO)* (0,01т)
        Норматив платы, руб./т (Мсрi) - 1823,6
        ____________________________________________________
        Загрязняющее вещество - Органич. к-ты (на СН3СООН)* (0,14т)
        Норматив платы, руб./т (Мсрi) - 93,5

        Коэффициент за 2021 г. (Нплi) - 1,08
        Коэффициент Кср - 25 (ПРИКАЗ Минприроды от 9 января 2017 г. N 3)



        См. Постановление Правительства РФ от 11.09.2020 N 1393
        "О применении в 2021 году ставок платы за негативное
        воздействие на окружающую среду"

        Постановление Правительства РФ от 13.09.2016 № 913
        «О ставках платы за негативное воздействие на окружающую
        среду и дополнительных коэффициентах»
        """

        tax_CO = 1.6 * 1.08 * 25 * 0.798
        tax_NOx = 138.8 * 1.08 * 25 * 0.066
        tax_SO2 = 45.4 * 1.08 * 25 * 0.26
        tax_H2S = 686.2 * 1.08 * 25 * 0.001
        tax_C = 109.5 * 1.08 * 25 * 1.615
        tax_HCN = 547.4 * 1.08 * 25 * 0.01
        tax_HCHO = 1823.6 * 1.08 * 25 * 0.01
        tax_CH3COOH = 93.5 * 1.08 * 25 * 0.14

        tax_all_1_tonn = tax_CO + tax_NOx + tax_SO2 + tax_H2S + tax_C + tax_HCN + tax_HCHO + tax_CH3COOH

        damage_air_fire = round(m_in_spill * tax_all_1_tonn * pow(10, -6), 4)

        return damage_air_fire

    def damage_earth(self, S_spill=1124):
        """
        :@param: S_spill,  площадь пролива, м2;
        :@return:
        - ущерб, млн.руб

        При расчете ущерба от загрязнения почвы при расчете ущерба
        принимались следующие коэффициенты СЗ =1,5 (степень загрязнения),
        Kr = 1 (показатель в зависимости от глубины загрязнения),
        Кисх=1,6 (показатель в зависимости от кат.земель и
        целевого назначения),
        Тх = 500 руб/м2 (расценка для исчисления размера вреда).
        Итого за 1 м2: 1200 руб.

        См. Методика исчисления размера вреда,
        причиненного почвам как объекту охраны окружающей среды
        (утверждена Приказом Минприроды России от 08.07.2010 № 238
        (ред. от 25.04.2014)
        (Зарегистрировано в Минюсте России 07.09.2010 № 18364)
        """

        tax_1m2 = 1.5 * 1 * 1.6 * 500
        damage_earth = round(S_spill * tax_1m2 * pow(10, -6), 3)

        return damage_earth

    def damage_array(self, volume=0, diametr=114,
                     lenght=1000, cost_sub=0.012,
                     part_sub=1,
                     death_person=1, injured_person=1,
                     m_out_spill=3, m_in_spill=50.5, S_spill=1124):
        """
        Для стационарного объекта
        :@param volume: объем в м3
        Для линейного объекта объекта
        :@param diametr, диаметр трубы в мм
        :@param length: длина, м
        For all
        :@param cost_sub, стоимость млн.руб/м3
        :@param part_sub, часть утерянного вещества
        :@param: death_person - погибшие
        :@param: injured_person - пострадавшие
        :@param: m_out_spill,  сколько испарилось тонны;
        :@param: m_in_spill,  сколько осталось гореть тонны;
        :@param: S_spill,  площадь пролива, м2;

        :@return:
        - ущерб массив, млн
        """
        direct_damage = self.direct_damage(volume, diametr, lenght, cost_sub, part_sub)
        liquidation_failures = round(direct_damage * 0.1, 2)
        se_damage = self.se_damage(death_person, injured_person)
        consequential_damage = round((se_damage + direct_damage) * 0.125, 2)
        # ________________Ecological____________________________________
        damage_air = self.damage_air(m_out_spill)  # от испарения
        damage_air_fire = self.damage_air_fire(m_in_spill)  # от горения
        damage_earth = self.damage_earth(S_spill)  # от пролива
        ecological_damage = round(damage_air +
                                  damage_air_fire +
                                  damage_earth, 2)
        # __________________________________________________________________
        new_man = round(direct_damage*0.56, 2)

        sum_damage = round(round(direct_damage * CONST, 2) + liquidation_failures + se_damage +
                           consequential_damage +
                           damage_air + damage_air_fire + damage_earth +
                           ecological_damage +
                           new_man, 2)

        damage_array = (direct_damage, liquidation_failures, se_damage, consequential_damage,
                        damage_air, damage_air_fire, damage_earth, ecological_damage,
                        new_man, sum_damage)

        return damage_array

