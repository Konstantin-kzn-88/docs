import random
from unittest import TestCase, main
from risk import risk_event_tree


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


if __name__ == '__main__':
    main()
