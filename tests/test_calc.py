import random
from unittest import TestCase, main
from calc import calc_strait_fire, calc_probit, calc_sp_explosion, calc_tvs_explosion, calc_fireball, \
    calc_lower_concentration, calc_liguid_evaporation, calc_light_gas_disp, calc_heavy_gas_disp


class ServerTest(TestCase):

    # START 1.Тестирование пожара пролива (strait_fire)
    def test_strait_fire_liguid(self):
        self.assertEqual(
            round(calc_strait_fire.Strait_fire().termal_radiation_point(S_spill=918, m_sg=0.06, mol_mass=95,
                                                                        t_boiling=68, wind_velocity=2, radius=40), 1),
            6.3)

    def test_strait_fire_greater_than_zero(self):
        for _ in range(1, 5):
            s = random.randint(20, 50)
            v = random.choice((1, 2, 3, 4, 5))
            self.assertGreater(
                round(calc_strait_fire.Strait_fire().termal_radiation_point(S_spill=s, m_sg=0.06, mol_mass=95,
                                                                            t_boiling=68, wind_velocity=v, radius=40),
                      1),
                0)

    def test_strait_fire_lpg(self):
        self.assertEqual(
            round(calc_strait_fire.Strait_fire().termal_radiation_point(S_spill=20, m_sg=0.1, mol_mass=44,
                                                                        t_boiling=-15, wind_velocity=1, radius=50), 1),
            0.8)

    def test_strait_fire_with_null_param(self):
        with self.assertRaises(ValueError) as e:
            calc_strait_fire.Strait_fire().termal_radiation_point(S_spill=0, m_sg=0.1, mol_mass=44,
                                                                  t_boiling=0, wind_velocity=1, radius=50)

        self.assertEqual('Фукнция не может принимать нулевые параметры', e.exception.args[0])

        with self.assertRaises(ValueError) as e:
            calc_strait_fire.Strait_fire().termal_radiation_point(S_spill=20, m_sg=0, mol_mass=0,
                                                                  t_boiling=200, wind_velocity=0, radius=50)

        self.assertEqual('Фукнция не может принимать нулевые параметры', e.exception.args[0])

    def test_count_array_result(self):
        for s in range(20, 200, 25):
            v = random.choice((1, 2, 3, 4, 5))
            self.assertEqual(len(calc_strait_fire.Strait_fire().termal_radiation_array(S_spill=s, m_sg=0.1, mol_mass=44,
                                                                                       t_boiling=-15, wind_velocity=v)[
                                     0]),
                             len(calc_strait_fire.Strait_fire().termal_radiation_array(S_spill=s, m_sg=0.1, mol_mass=44,
                                                                                       t_boiling=-15, wind_velocity=v)[
                                     1]))

            self.assertEqual(
                len(calc_strait_fire.Strait_fire().termal_radiation_array(S_spill=s, m_sg=0.3, mol_mass=144,
                                                                          t_boiling=-10, wind_velocity=v)[2]),
                len(calc_strait_fire.Strait_fire().termal_radiation_array(S_spill=s, m_sg=0.3, mol_mass=144,
                                                                          t_boiling=-10, wind_velocity=v)[3]))
        # END

    # START 2. Тестирование пробит-функции

    def test_probit_check(self):
        self.assertEqual(calc_probit.Probit().probit_check(probit=11), 8.09)
        self.assertEqual(calc_probit.Probit().probit_check(probit=2), 0)
        self.assertEqual(calc_probit.Probit().probit_check(probit=3.33), 3.33)

    def test_probability(self):
        self.assertEqual(calc_probit.Probit().probability(probit=8.99), 0.99)
        self.assertEqual(calc_probit.Probit().probability(probit=-12), 0)
        self.assertEqual(round(calc_probit.Probit().probability(probit=3.35), 2), 0.06)

    def test_probit_explosion_with_null_param(self):
        with self.assertRaises(ValueError) as e:
            calc_probit.Probit().probit_explosion(delta_P=0, impuls=161)
        self.assertEqual('Фукнция не может принимать нулевые параметры', e.exception.args[0])

        with self.assertRaises(ValueError) as e:
            calc_probit.Probit().probit_explosion(delta_P=0, impuls=0)
        self.assertEqual('Фукнция не может принимать нулевые параметры', e.exception.args[0])

    def test_probit_fireball_with_null_param(self):
        with self.assertRaises(ValueError) as e:
            calc_probit.Probit().probit_fireball(time=0, q_ball=125)
        self.assertEqual('Фукнция не может принимать нулевые параметры', e.exception.args[0])

        with self.assertRaises(ValueError) as e:
            calc_probit.Probit().probit_fireball(time=0, q_ball=0)
        self.assertEqual('Фукнция не может принимать нулевые параметры', e.exception.args[0])

    def test_probit_strait_fire_with_null_param(self):
        with self.assertRaises(ValueError) as e:
            calc_probit.Probit().probit_strait_fire(dist=0, q_max=0)
        self.assertEqual('math domain error', e.exception.args[0])

        with self.assertRaises(ValueError) as e:
            calc_probit.Probit().probit_strait_fire(dist=10, q_max=0)
        self.assertEqual('math domain error', e.exception.args[0])

    # END

    # START 3. Тестирование взрыва (СП 12.13130-2009)
    def test_explosion_point(self):
        self.assertEqual(
            round(
                calc_sp_explosion.Explosion().explosion_point(mass=254400, heat_of_combustion=46000, z=0.1, radius=500)[
                    0], 2), 15.5)

    def test_explosion_point_greater_than_zero(self):
        for m in range(100, 1000, 250):
            h = random.randint(46000, 101000)
            z = random.choice((0.1, 0.3, 0.5))
            r = random.randint(10, 60)
            self.assertGreater(
                round(
                    calc_sp_explosion.Explosion().explosion_point(mass=m, heat_of_combustion=h, z=z,
                                                                  radius=r)[0], 1), 0)

    def test_explosion_with_null_param(self):
        with self.assertRaises(ValueError) as e:
            calc_sp_explosion.Explosion().explosion_point(mass=0, heat_of_combustion=101000, z=0.1, radius=50)
        self.assertEqual('Фукнция не может принимать нулевые параметры', e.exception.args[0])

        with self.assertRaises(ValueError) as e:
            calc_sp_explosion.Explosion().explosion_point(mass=0, heat_of_combustion=0, z=0.1, radius=0)
        self.assertEqual('Фукнция не может принимать нулевые параметры', e.exception.args[0])

    def test_count_array_result_explosion(self):
        for m in range(100, 1000, 250):
            h = random.randint(46000, 101000)
            z = random.choice((0.1, 0.3, 0.5))

            self.assertEqual(
                len(calc_sp_explosion.Explosion().explosion_array(mass=m, heat_of_combustion=h, z=z)[0]),
                len(calc_sp_explosion.Explosion().explosion_array(mass=m, heat_of_combustion=h, z=z)[1]))

            self.assertEqual(
                len(calc_sp_explosion.Explosion().explosion_array(mass=m, heat_of_combustion=h, z=z)[2]),
                len(calc_sp_explosion.Explosion().explosion_array(mass=m, heat_of_combustion=h, z=z)[3]))
        # END

    # END

    # START 4. Тестирование взрыва (ТВС методика)
    def test_v_burn_point(self):
        tmp = (500, 500, 300, 200)
        for view in range(1, 5):
            self.assertEqual(calc_tvs_explosion.Explosion().burn_rate(class_substance=1, view_space=view, mass=200),
                             tmp[view - 1])

        tmp = (500, 300, 200, 150)
        for view in range(1, 5):
            self.assertEqual(calc_tvs_explosion.Explosion().burn_rate(class_substance=2, view_space=view, mass=200),
                             tmp[view - 1])
        mass = 2000
        tmp = (300, 200, 150, 43 * pow(mass, 1 / 6))
        for view in range(1, 5):
            self.assertEqual(calc_tvs_explosion.Explosion().burn_rate(class_substance=3, view_space=view, mass=mass),
                             tmp[view - 1])

        mass = 2000
        tmp = (200, 150, 43 * pow(mass, 1 / 6), 26 * pow(mass, 1 / 6))
        for view in range(1, 5):
            self.assertEqual(calc_tvs_explosion.Explosion().burn_rate(class_substance=4, view_space=view, mass=mass),
                             tmp[view - 1])

    def test_explosion_tvs_point(self):
        self.assertEqual(
            round(
                calc_tvs_explosion.Explosion().explosion_point(class_substance=1, view_space=2,
                                                               mass=2000, heat_of_combustion=46000, sigma=7,
                                                               energy_level=2, radius=200)[
                    0], 2), 85.3)

    def test_explosion_tvs_point_greater_than_zero(self):
        for m in range(100, 1000, 250):
            c = random.randint(1, 4)
            v = random.randint(1, 4)
            e = random.randint(1, 2)
            r = random.randint(10, 50)
            self.assertGreater(
                round(calc_tvs_explosion.Explosion().explosion_point(class_substance=c,
                                                                     view_space=v, mass=m,
                                                                     heat_of_combustion=46000, sigma=7,
                                                                     energy_level=e,
                                                                     radius=r)[0], 1), 0)

    def test_explosion_tvs_with_null_param(self):
        with self.assertRaises(ValueError) as e:
            calc_tvs_explosion.Explosion().explosion_point(class_substance=10,
                                                           view_space=1, mass=0,
                                                           heat_of_combustion=0, sigma=7,
                                                           energy_level=2,
                                                           radius=10)
        self.assertEqual('Фукнция не может принимать нулевые параметры', e.exception.args[0])

        with self.assertRaises(ValueError) as e:
            calc_tvs_explosion.Explosion().explosion_point(class_substance=0,
                                                           view_space=1, mass=0,
                                                           heat_of_combustion=0, sigma=7,
                                                           energy_level=10,
                                                           radius=0)
        self.assertEqual('Фукнция не может принимать нулевые параметры', e.exception.args[0])

    def test_count_array_result_explosion_tvs(self):
        for m in range(10, 100, 25):
            self.assertEqual(
                len(calc_tvs_explosion.Explosion().explosion_array(class_substance=1, view_space=1, mass=m,
                                                                   heat_of_combustion=46000, sigma=7, energy_level=2)[
                        0]),
                len(calc_tvs_explosion.Explosion().explosion_array(class_substance=1, view_space=1, mass=m,
                                                                   heat_of_combustion=46000, sigma=7, energy_level=2)[
                        1]))

            self.assertEqual(
                len(calc_tvs_explosion.Explosion().explosion_array(class_substance=1, view_space=1, mass=m,
                                                                   heat_of_combustion=46000, sigma=7, energy_level=2)[
                        2]),
                len(calc_tvs_explosion.Explosion().explosion_array(class_substance=1, view_space=1, mass=m,
                                                                   heat_of_combustion=46000, sigma=7, energy_level=2)[
                        3]))

    # END

    # START 5. Тестирование огненного шара
    def test_fireball_point(self):
        self.assertEqual(
            round(calc_fireball.Fireball().fireball_point(mass=2.54 * pow(10, 5), ef=450, radius=500)[0], 2), 12.9)

    def test_fireball_greater_than_zero(self):
        for m in range(100, 1000, 250):
            e = random.choice((350, 450))
            r = random.randint(100, 200)
            self.assertGreater(round(calc_fireball.Fireball().fireball_point(mass=m, ef=e, radius=r)[0], 1), 0)

    def test_fireball_with_null_param(self):
        with self.assertRaises(ValueError) as e:
            calc_fireball.Fireball().fireball_point(mass=0, ef=0, radius=0)
        self.assertEqual('Фукнция не может принимать нулевые параметры', e.exception.args[0])

        with self.assertRaises(ValueError) as e:
            calc_fireball.Fireball().fireball_point(mass=0, ef=450, radius=10)
        self.assertEqual('Фукнция не может принимать нулевые параметры', e.exception.args[0])

    def test_fireball(self):
        for m in range(1000, 10000, 250):
            self.assertEqual(len(calc_fireball.Fireball().fireball_array(mass=m, ef=450)[0]),
                             len(calc_fireball.Fireball().fireball_array(mass=m, ef=450)[1]))

            self.assertEqual(len(calc_fireball.Fireball().fireball_array(mass=m, ef=450)[2]),
                             len(calc_fireball.Fireball().fireball_array(mass=m, ef=450)[3]))

    # END

    # START 5. Тестирование НКПР и пожара-вспышки
    def test_lclp(self):
        self.assertEqual(
            round(calc_lower_concentration.LCLP().lower_concentration_limit(mass=200, mol_mass=100, t_boiling=63,
                                                                            lower_concentration=1.8)[0], 2), 24.14)

    def test_lclp_greater_than_zero(self):
        for m in range(100, 1000, 250):
            t = random.choice((10, 100))
            l = random.randint(1, 10)
            self.assertGreater(
                round(calc_lower_concentration.LCLP().lower_concentration_limit(mass=m, mol_mass=100, t_boiling=t,
                                                                                lower_concentration=l)[0], 1), 0)

    # END

    # START 6. Тестирование испарения ненагретой жидкости
    def test_evaporation(self):
        self.assertEqual(
            round(calc_liguid_evaporation.Liquid_evaporation().evaporation_in_moment(time=3600, steam_pressure=35,
                                                                                     molar_mass=100, strait_area=200)[
                      0],
                  0),
            252)

    def test_evaporation_greater_than_zero(self):
        for time in range(100, 3600, 100):
            steam_pressure = random.randint(20, 100)
            molar_mass = random.randint(20, 200)
            strait_area = random.randint(20, 20000)
            self.assertGreater(calc_liguid_evaporation.Liquid_evaporation().evaporation_in_moment(time, steam_pressure,
                                                                                                  molar_mass,
                                                                                                  strait_area)[0], 0)

    def test_evaporation_with_null_param(self):
        with self.assertRaises(ValueError) as e:
            calc_liguid_evaporation.Liquid_evaporation().evaporation_in_moment(time=0, steam_pressure=0,
                                                                               molar_mass=0, strait_area=0)
        self.assertEqual('Фукнция не может принимать нулевые параметры', e.exception.args[0])

        with self.assertRaises(ValueError) as e:
            calc_liguid_evaporation.Liquid_evaporation().evaporation_array(steam_pressure=0, molar_mass=0,
                                                                           strait_area=0)
        self.assertEqual('Фукнция не может принимать нулевые параметры', e.exception.args[0])

    def test_evaporation_eq_len(self):
        for time in range(1000, 10000, 250):
            self.assertEqual(
                len(calc_liguid_evaporation.Liquid_evaporation().evaporation_array(steam_pressure=20, molar_mass=210,
                                                                                   strait_area=2000)[0]),
                len(calc_liguid_evaporation.Liquid_evaporation().evaporation_array(steam_pressure=20, molar_mass=210,
                                                                                   strait_area=2000)[1]))

    # END

    # START 7. Тестирование рассеивания легкого газа
    # 7.1. Table C5.2. Pasquill Atmospheric Stability Classes p.222
    def test_pasquill(self):
        self.assertEqual(
            calc_light_gas_disp.Instantaneous_source(ambient_temperature=30, cloud=0, wind_speed=3, density_air=1.21,
                                                     is_night=False,
                                                     is_urban_area=False).pasquill_atmospheric_stability_classes(), 'B')

        self.assertEqual(
            calc_light_gas_disp.Instantaneous_source(ambient_temperature=30, cloud=8, wind_speed=7, density_air=1.21,
                                                     is_night=False,
                                                     is_urban_area=False).pasquill_atmospheric_stability_classes(), 'D')

        self.assertEqual(
            calc_light_gas_disp.Continuous_source(ambient_temperature=7, cloud=5,
                                                  wind_speed=2, density_air=1.21,
                                                  is_night=True,
                                                  is_urban_area=False).pasquill_atmospheric_stability_classes(), 'F')

        self.assertEqual(
            calc_light_gas_disp.Continuous_source(ambient_temperature=7, cloud=1,
                                                  wind_speed=2, density_air=1.21,
                                                  is_night=True,
                                                  is_urban_area=False).pasquill_atmospheric_stability_classes(), 'E')

    def test_wind_profile(self):
        self.assertEqual(
            calc_light_gas_disp.Instantaneous_source(ambient_temperature=30, cloud=7, wind_speed=4, density_air=1.21,
                                                     is_night=True,
                                                     is_urban_area=False).wind_profile(), 0.35)
        self.assertEqual(
            calc_light_gas_disp.Continuous_source(ambient_temperature=7, cloud=5,
                                                  wind_speed=2, density_air=1.21,
                                                  is_night=True, is_urban_area=False).wind_profile(), 0.55)

    def test_wind_power_law(self):
        self.assertEqual(
            round(calc_light_gas_disp.Instantaneous_source(ambient_temperature=30, cloud=0,
                                                           wind_speed=4, density_air=1.21,
                                                           is_night=False, is_urban_area=False).wind_power_law(2),
                  2), 3.57)

        self.assertEqual(
            round(calc_light_gas_disp.Continuous_source(ambient_temperature=7, cloud=5,
                                                        wind_speed=2, density_air=1.21,
                                                        is_night=True, is_urban_area=False).wind_power_law(25),
                  2), 3.31)

    def test_height_source_correction(self):
        # Только вторичное облако
        cls = calc_light_gas_disp.Continuous_source(ambient_temperature=7, cloud=5,
                                                    wind_speed=2, density_air=1.21,
                                                    is_night=True, is_urban_area=False)
        us = (cls.wind_power_law(25))

        self.assertEqual(round(cls.height_source_correction(us, 4, 1, 25), 1), 24.4)

    def test_selecting_plume_rise(self):
        # Только вторичное облако
        cls = calc_light_gas_disp.Continuous_source(ambient_temperature=7, cloud=5,
                                                    wind_speed=2, density_air=1.21,
                                                    is_night=True, is_urban_area=False)
        pasquill = (cls.pasquill_atmospheric_stability_classes())

        self.assertEqual(round(cls.selecting_plume_rise(pasquill, 4, 127, 1), 1), 1.1)

    def test_source_buoyancy_flux_parameter(self):
        self.assertEqual(
            round(calc_light_gas_disp.Instantaneous_source(ambient_temperature=25, cloud=0,
                                                           wind_speed=4, density_air=1.21,
                                                           is_night=False,
                                                           is_urban_area=False).source_buoyancy_flux_parameter(147,
                                                                                                               500),
                  0), 528)

    def test_maximum_distance_x(self):
        # первичное облако
        cls = calc_light_gas_disp.Instantaneous_source(ambient_temperature=25, cloud=0, wind_speed=4, density_air=1.21,
                                                       is_night=False, is_urban_area=False)
        pasquill = (cls.pasquill_atmospheric_stability_classes())
        us = (cls.wind_power_law(ejection_height=2))
        Fbi = (cls.source_buoyancy_flux_parameter(147, 500))
        self.assertEqual(round(cls.maximum_distance_x(pasquill, us, Fbi), 0), 422)
        # вторичное облако
        cls = calc_light_gas_disp.Continuous_source(ambient_temperature=7, cloud=5,
                                                    wind_speed=2, density_air=1.21,
                                                    is_night=True, is_urban_area=False)

        pasquill = (cls.pasquill_atmospheric_stability_classes())
        us = (cls.wind_power_law(25))
        dt = cls.selecting_plume_rise(pasquill, 4, 127, 1)
        self.assertEqual(round(cls.maximum_distance_x(pasquill, 4, 127, 1, dt, us), 0), 196)

    def test_gradual_puff_rise(self):
        cls = calc_light_gas_disp.Instantaneous_source(ambient_temperature=25, cloud=0, wind_speed=4, density_air=1.21,
                                                       is_night=False, is_urban_area=False)
        pasquill = (cls.pasquill_atmospheric_stability_classes())
        us = (cls.wind_power_law(ejection_height=2))
        Fbi = (cls.source_buoyancy_flux_parameter(147, 500))
        self.assertEqual(round(cls.gradual_puff_rise(ejection_height=2, pasquill=pasquill, us=us,
                                                     Fbi=Fbi, gas_weight=500, po_gas=3.15, x_dist=300), 0), 75)
        self.assertEqual(round(cls.gradual_puff_rise(ejection_height=2, pasquill=pasquill, us=us,
                                                     Fbi=Fbi, gas_weight=500, po_gas=3.15, x_dist=100), 0), 44)
        self.assertEqual(round(cls.gradual_puff_rise(ejection_height=2, pasquill=pasquill, us=us,
                                                     Fbi=Fbi, gas_weight=500, po_gas=3.15, x_dist=200), 0), 62)

        # вторичное облако
        cls = calc_light_gas_disp.Continuous_source(ambient_temperature=7, cloud=5,
                                                    wind_speed=2, density_air=1.21,
                                                    is_night=True, is_urban_area=False)

        pasquill = (cls.pasquill_atmospheric_stability_classes())
        us = (cls.wind_power_law(25))
        hs_with_steak = cls.height_source_correction(us, 4, 1, 25)
        dt = cls.selecting_plume_rise(pasquill, 4, 127, 1)
        self.assertEqual(round(cls.gradual_puff_rise(pasquill, 4, 127, 1, dt, us, hs_with_steak, 50), 2), 33.82)
        self.assertEqual(round(cls.gradual_puff_rise(pasquill, 4, 127, 1, dt, us, hs_with_steak, 100), 2), 39.34)

    def test_final_puff_rise(self):
        # первичное облако
        cls = calc_light_gas_disp.Instantaneous_source(ambient_temperature=25, cloud=0, wind_speed=4, density_air=1.21,
                                                       is_night=False, is_urban_area=False)
        pasquill = (cls.pasquill_atmospheric_stability_classes())
        us = (cls.wind_power_law(ejection_height=2))
        Fbi = (cls.source_buoyancy_flux_parameter(147, 500))
        self.assertEqual(round(cls.final_puff_rise(ejection_height=2, pasquill=pasquill, us=us,
                                                   Fbi=Fbi, gas_weight=500, po_gas=3.15, x_dist=500), 0), 89)
        self.assertEqual(round(cls.final_puff_rise(ejection_height=2, pasquill=pasquill, us=us,
                                                   Fbi=Fbi, gas_weight=500, po_gas=3.15, x_dist=600), 0), 89)
        self.assertEqual(round(cls.final_puff_rise(ejection_height=2, pasquill=pasquill, us=us,
                                                   Fbi=Fbi, gas_weight=500, po_gas=3.15, x_dist=700), 0), 89)
        # вторичное облако
        cls = calc_light_gas_disp.Continuous_source(ambient_temperature=7, cloud=5,
                                                    wind_speed=2, density_air=1.21,
                                                    is_night=True, is_urban_area=False)

        pasquill = (cls.pasquill_atmospheric_stability_classes())
        us = (cls.wind_power_law(25))
        hs_with_steak = cls.height_source_correction(us, 4, 1, 25)
        dt = cls.selecting_plume_rise(pasquill, 4, 127, 1)
        self.assertEqual(round(cls.final_puff_rise(pasquill, 4, 127, 1, dt, us, hs_with_steak), 0), 48)

    def test_dispersion_param(self):
        cls = calc_light_gas_disp.Instantaneous_source(ambient_temperature=25, cloud=0, wind_speed=4, density_air=1.21,
                                                       is_night=False, is_urban_area=False)
        pasquill = (cls.pasquill_atmospheric_stability_classes())
        self.assertEqual(round(cls.dispersion_param(pasquill=pasquill, x_dist=100)[0], 0), 10)
        self.assertEqual(round(cls.dispersion_param(pasquill=pasquill, x_dist=100)[1], 0), 10)
        self.assertEqual(round(cls.dispersion_param(pasquill=pasquill, x_dist=100)[2], 0), 15)
        # только вторичное облако (параметры a-h)
        cls = calc_light_gas_disp.Continuous_source(ambient_temperature=7, cloud=5,
                                                    wind_speed=2, density_air=1.21,
                                                    is_night=True, is_urban_area=False)
        self.assertEqual(cls.a_b_param('F', 350), (14.457, 0.78407))
        self.assertEqual(cls.c_h_param('F'), (4.1667, 0.3619, 0.11, 0.08, 0.0015, -0.05))
        # вторичное облако сигма x и сигма z
        self.assertEqual(round(cls.dispersion_param('F', 50)[0], 2), 2.14)
        self.assertEqual(round(cls.dispersion_param('F', 50)[1], 2), 1.32)

    def test_mean_wind_speed(self):
        cls = calc_light_gas_disp.Instantaneous_source(ambient_temperature=25, cloud=0,
                                                       wind_speed=4, density_air=1.21,
                                                       is_night=False, is_urban_area=False)
        pasquill = (cls.pasquill_atmospheric_stability_classes())
        us = (cls.wind_power_law(ejection_height=2))
        Fbi = (cls.source_buoyancy_flux_parameter(147, 500))
        x_max = cls.maximum_distance_x(pasquill, us, Fbi)
        he_max = cls.gradual_puff_rise(ejection_height=2, pasquill=pasquill, us=us,
                                       Fbi=Fbi, gas_weight=500, po_gas=3.15, x_dist=x_max)

        x = 100
        he_r = cls.gradual_puff_rise(ejection_height=2, pasquill=pasquill, us=us,
                                     Fbi=Fbi, gas_weight=500, po_gas=3.15, x_dist=x)

        _, _, sigma_z = cls.dispersion_param(pasquill=pasquill, x_dist=100)
        self.assertEqual(round(cls.mean_wind_speed(he_r, he_max, sigma_z)[0], 0), 11)
        self.assertEqual(round(cls.mean_wind_speed(he_r, he_max, sigma_z)[1], 0), 77)
        self.assertEqual(round(cls.mean_wind_speed(he_r, he_max, sigma_z)[2], 0), 4)

    def test_time_in_out_peak(self):
        cls = calc_light_gas_disp.Instantaneous_source(ambient_temperature=25, cloud=0,
                                                       wind_speed=4, density_air=1.21,
                                                       is_night=False, is_urban_area=False)
        pasquill = (cls.pasquill_atmospheric_stability_classes())
        us = (cls.wind_power_law(ejection_height=2))
        Fbi = (cls.source_buoyancy_flux_parameter(147, 500))
        x_max = cls.maximum_distance_x(pasquill, us, Fbi)
        he_max = cls.gradual_puff_rise(ejection_height=2, pasquill=pasquill, us=us,
                                       Fbi=Fbi, gas_weight=500, po_gas=3.15, x_dist=x_max)

        x = 100
        he_r = cls.gradual_puff_rise(ejection_height=2, pasquill=pasquill, us=us,
                                     Fbi=Fbi, gas_weight=500, po_gas=3.15, x_dist=x)

        sigma_x, _, sigma_z = cls.dispersion_param(pasquill=pasquill, x_dist=x)
        u_mean = cls.mean_wind_speed(he_r, he_max, sigma_z)[2]
        self.assertEqual(round(cls.time_in_out_peak(sigma_x, u_mean, x)[0], 0), 17)
        self.assertEqual(round(cls.time_in_out_peak(sigma_x, u_mean, x)[1], 0), 28)
        self.assertEqual(round(cls.time_in_out_peak(sigma_x, u_mean, x)[2], 0), 23)

    def test_concentration(self):
        cls = calc_light_gas_disp.Instantaneous_source(ambient_temperature=25, cloud=0,
                                                       wind_speed=4, density_air=1.21,
                                                       is_night=False, is_urban_area=False)
        pasquill = (cls.pasquill_atmospheric_stability_classes())
        us = (cls.wind_power_law(ejection_height=2))
        Fbi = (cls.source_buoyancy_flux_parameter(147, 500))
        x_max = cls.maximum_distance_x(pasquill, us, Fbi)
        he_max = cls.gradual_puff_rise(ejection_height=2, pasquill=pasquill, us=us,
                                       Fbi=Fbi, gas_weight=500, po_gas=3.15, x_dist=x_max)
        x = 1000
        he_r = cls.gradual_puff_rise(ejection_height=2, pasquill=pasquill, us=us, Fbi=Fbi, gas_weight=500, po_gas=3.15,
                                     x_dist=x) if x <= he_max else cls.final_puff_rise(ejection_height=2,
                                                                                       pasquill=pasquill,
                                                                                       us=us, Fbi=Fbi, gas_weight=500,
                                                                                       po_gas=3.15, x_dist=x)
        sigma_x, sigma_y, sigma_z = cls.dispersion_param(pasquill=pasquill, x_dist=x)
        u_mean = cls.mean_wind_speed(he_r, he_max, sigma_z)[2]
        t_in, t_out, t_peak = cls.time_in_out_peak(sigma_x, u_mean, x)
        self.assertEqual(round(cls.concentration(500, pasquill, u_mean, he_r, t_peak, x, 0, 2), 0), 133)
        # Вторичное облако
        cls = calc_light_gas_disp.Continuous_source(ambient_temperature=7, cloud=5,
                                                      wind_speed=2, density_air=1.21,
                                                      is_night=True, is_urban_area=False)

        pasquill = (cls.pasquill_atmospheric_stability_classes())
        us = (cls.wind_power_law(25))
        hs_with_steak = cls.height_source_correction(us, 4, 1, 25)
        dt = cls.selecting_plume_rise(pasquill, 4, 127, 1)
        x_max = 60000
        he_2 = (cls.final_puff_rise(pasquill, 4, 127, 1, dt, us, hs_with_steak))
        self.assertEqual(round(cls.concentration(0.02, us, pasquill, he_2, x_max, 0, 2),3),0.015)

    # END

    # START 8. Тестирование рассеивания тяжелого газа
    def test_alpha_beta(self):
        # первичное облако
        cls = calc_heavy_gas_disp.Instantaneous_source(1, 1.21)
        self.assertEqual(round(cls.alpha(6,10), 2), 0.96)
        self.assertEqual(round(cls.beta(0.96, 0.6), 2), 1.79)
        # второричное облако
        cls = calc_heavy_gas_disp.Continuous_source(4, 1.21)
        self.assertEqual(round(cls.alpha(6,1), 3), 0.034)
        self.assertEqual(round(cls.beta(0.033,0.01), 2), 2.37)

    def test_find_distance(self):
        # первичное облако
        cls = calc_heavy_gas_disp.Instantaneous_source(1, 1.21)
        self.assertEqual(round(cls.find_distance(1.79,10), 0), 133)
        # второричное облако
        cls = calc_heavy_gas_disp.Continuous_source(4, 1.21)
        self.assertEqual(round(cls.find_distance(2.37,1), 0), 117)

    def test_find_time(self):
        cls = calc_heavy_gas_disp.Instantaneous_source(1, 1.21)
        self.assertEqual(round(cls.find_time(132,10,6,1)[0], 0), 171)
        self.assertEqual(round(cls.find_time(163,10,6,1)[0], 0), 225)
        self.assertEqual(round(cls.find_time(132,10,6,1)[1], 0), 64)
        self.assertEqual(round(cls.find_time(163,10,6,1)[1], 0), 73)
    # END
