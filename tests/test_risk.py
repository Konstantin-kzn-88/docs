import random
from unittest import TestCase, main
from risk import risk_event_tree


class ServerTest(TestCase):

    def test_risk_event_tree_mchs(self):
        self.assertEqual(risk_event_tree.Event_tree().mchs(flash_temperature=10, flow_rate=0, probability=0.000007),
                         ('1.40e-06', '8.06e-07', '5.38e-07', '4.26e-06'))
        self.assertEqual(risk_event_tree.Event_tree().mchs(flash_temperature=10, flow_rate=1, probability=0.000007),
                         ('2.45e-07', '5.84e-08', '1.85e-07', '6.51e-06'))
        self.assertEqual(risk_event_tree.Event_tree().mchs(flash_temperature=10, flow_rate=0.3, probability=0.000007),
                         ('3.50e-08', '2.79e-09', '3.20e-08', '6.93e-06'))
        self.assertEqual(risk_event_tree.Event_tree().mchs(flash_temperature=30, flow_rate=0, probability=0.000007),
                         ('3.50e-07', '4.06e-08', '3.65e-07', '6.24e-06'))
        self.assertEqual(risk_event_tree.Event_tree().mchs(flash_temperature=30, flow_rate=1, probability=0.000007),
                         ('1.05e-07', '5.17e-09', '9.83e-08', '6.79e-06'))
        self.assertEqual(risk_event_tree.Event_tree().mchs(flash_temperature=30, flow_rate=0.3, probability=0.000007),
                         ('3.50e-08', '1.74e-09', '3.31e-08', '6.93e-06'))

    def test_len_risk_event_tree_mchs(self):
        for t in range(-20, 30, 1):
            for f in range(0, 100, 1):
                self.assertEqual(
                    len(risk_event_tree.Event_tree().mchs(flash_temperature=t, flow_rate=f / 10, probability=7e-5)), 4)


if __name__ == '__main__':
    main()
