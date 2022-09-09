import random
from unittest import TestCase, main
from risk import risk_event_tree, risk_probability


class ServerTest(TestCase):

    def test_risk_event_tree_mchs(self):
        # vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
        # mchs_liquid
        self.assertEqual(
            risk_event_tree.Event_tree().mchs_liquid(flash_temperature=10, flow_rate=0, probability=0.000007),
            ('1.40e-06', '8.06e-07', '5.38e-07', '4.26e-06'))
        self.assertEqual(
            risk_event_tree.Event_tree().mchs_liquid(flash_temperature=10, flow_rate=1, probability=0.000007),
            ('2.45e-07', '5.84e-08', '1.85e-07', '6.51e-06'))
        self.assertEqual(
            risk_event_tree.Event_tree().mchs_liquid(flash_temperature=10, flow_rate=0.3, probability=0.000007),
            ('3.50e-08', '2.79e-09', '3.20e-08', '6.93e-06'))
        self.assertEqual(
            risk_event_tree.Event_tree().mchs_liquid(flash_temperature=30, flow_rate=0, probability=0.000007),
            ('3.50e-07', '4.06e-08', '3.65e-07', '6.24e-06'))
        self.assertEqual(
            risk_event_tree.Event_tree().mchs_liquid(flash_temperature=30, flow_rate=1, probability=0.000007),
            ('1.05e-07', '5.17e-09', '9.83e-08', '6.79e-06'))
        self.assertEqual(
            risk_event_tree.Event_tree().mchs_liquid(flash_temperature=30, flow_rate=0.3, probability=0.000007),
            ('3.50e-08', '1.74e-09', '3.31e-08', '6.93e-06'))

        # mchs_liquid_len
        for t in range(-20, 30, 1):
            for f in range(0, 100, 1):
                self.assertEqual(
                    len(risk_event_tree.Event_tree().mchs_liquid(flash_temperature=t, flow_rate=f / 10,
                                                                 probability=7e-5)), 4)
        # vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
        # mchs_gas
        self.assertEqual(
            risk_event_tree.Event_tree().mchs_gas(flow_rate=0, probability=0.000007),
            ('1.40e-06', '8.06e-07', '5.38e-07', '4.26e-06'))
        self.assertEqual(
            risk_event_tree.Event_tree().mchs_gas(flow_rate=0.3, probability=0.000007),
            ('3.50e-08', '2.79e-09', '3.20e-08', '6.93e-06'))
        self.assertEqual(
            risk_event_tree.Event_tree().mchs_gas(flow_rate=6, probability=0.000007),
            ('2.45e-07', '5.84e-08', '1.85e-07', '6.51e-06'))
        self.assertEqual(
            risk_event_tree.Event_tree().mchs_gas(flow_rate=11, probability=0.000007),
            ('1.05e-06', '6.28e-07', '4.19e-07', '4.90e-06'))

        # mchs_gas_len
        for f in range(0, 100, 1):
            self.assertEqual(
                len(risk_event_tree.Event_tree().mchs_gas(flow_rate=f / 10, probability=7e-5)), 4)

    def test_risk_event_tree_rostech(self):
        # vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
        # mchs_liquid
        self.assertEqual(
            risk_event_tree.Event_tree().rostech_liquid(type_obj=0, flow_rate=0, probability=0.000007),
            ('3.50e-07', '8.11e-08', '3.25e-07', '6.24e-06'))
        self.assertEqual(
            risk_event_tree.Event_tree().rostech_liquid(type_obj=0, flow_rate=2, probability=0.000007),
            ('2.80e-07', '5.64e-08', '2.26e-07', '6.44e-06'))
        self.assertEqual(
            risk_event_tree.Event_tree().rostech_liquid(type_obj=0, flow_rate=52, probability=0.000007),
            ('1.05e-06', '6.28e-07', '4.19e-07', '4.90e-06'))
        self.assertEqual(
            risk_event_tree.Event_tree().rostech_liquid(type_obj=1, flow_rate=0, probability=0.000007),
            ('3.50e-07', '6.65e-08', '2.66e-07', '6.32e-06'))

        # mchs_liquid_len
        for f in range(0, 1000, 5):
            self.assertEqual(
                len(risk_event_tree.Event_tree().rostech_liquid(type_obj=random.choice((1, 2)), flow_rate=f / 10,
                                                                probability=7e-5)), 4)

    def test_risk_probability(self):
        # vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
        # rosteh_device_tube
        self.assertEqual(
            risk_probability.Probability.probability_rosteh_device(1),
            ('1.00e-05', '5.00e-05'))
        self.assertEqual(
            risk_probability.Probability.probability_rosteh_tube(1,114),
            ('3.00e-07', '2.00e-07'))
        # rosteh_device_tube
        for j in range(0, 6, 1):
            self.assertEqual(
                len(risk_probability.Probability.probability_rosteh_device(type_obj=j)), 2)
        for j in range(10, 600, 10):
            self.assertEqual(
                len(risk_probability.Probability.probability_rosteh_tube(j,j)), 2)

        # vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
        # mchs_device
        self.assertEqual(
            risk_probability.Probability.probability_mchs_device(0),
            ('3.00e-07', '1.70e-06', '3.80e-06', '6.20e-06', '1.00e-05', '4.00e-05'))
        self.assertEqual(
            risk_probability.Probability.probability_mchs_device(1),
            ('5.00e-06', '1.20e-05', '8.80e-05'))
        # mchs_device_len
        for _ in range(10):
            self.assertEqual(
                len(risk_probability.Probability.probability_mchs_device(0)), 6)
        for _ in range(10):
            self.assertEqual(
                len(risk_probability.Probability.probability_mchs_device(1)), 3)

        # vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
        # mchs_tube
        self.assertEqual(
            risk_probability.Probability.probability_mchs_tube(1,100),
            ('2.80e-06', '1.20e-06', '4.70e-07', '0.00e+00', '2.40e-07'))
        self.assertEqual(
            risk_probability.Probability.probability_mchs_tube(1, 600),
            ('4.70e-07', '2.00e-07', '7.90e-08', '3.40e-08', '6.40e-09'))
        # mchs_tube_len
        for j in range(25):
            self.assertEqual(
                len(risk_probability.Probability.probability_mchs_tube(j,100)), 5)

if __name__ == '__main__':
    main()
