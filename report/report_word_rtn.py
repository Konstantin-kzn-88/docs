from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm
from pathlib import Path
import time
import os
import math
import copy
from calc import calc_liguid_evaporation as ev
from calc import calc_tvs_explosion as expl
from calc import calc_strait_fire as fire
from calc import calc_lower_concentration as nkpr
from calc import calc_damage as damage
from calc import calc_fn_fg_chart
from risk import risk_statistics_weather as weather
from risk import risk_probability as pr
from risk import risk_event_tree as tree

DESKTOP_PATH = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
LAYER_THICKNESS = 20  # м^-1
KG_TO_TONN = 1000  # 1000 кг = 1000/KG_TO_TONN = 1 тонна
TONN_TO_KG = 1000  # 1т = 1*TONN_TO_KG = 1000 кг
KM_TO_M = 1000  # 1км = 1*KM_TO_M = 1000 м
CUT_OFF_TIME = 12 * 3600  # секунд
TIME_EVAPORATION = 3600  # секунд
HOUR_TO_SECONDS = 3600  # 1ч = 1*HOUR_TO_SECONDS = 3600 с
DAY_TO_HOUR = 24  # 1сут = 1*DAY_TO_HOUR = 24 ч


class Report:
    def __init__(self, project_info: dict, object_info: dict, org_info: dict, doc_info: dict, dev_info: list,
                 pipe_info: list, sub_info: list, sender_call: int):
        """
        Класс отчета
        :param project_info: словарь данных проекта
        :param object_info: словарь данных объекта
        :param org_info: словарь данных организации
        :param doc_info: словарь данных томов
        :param dev_info: словарь данных оборудования
        :param pipe_info: словарь данных трубопроводов
        :param sub_info: словарь данных веществ
        :param sender_call: номер вызова, определяет то какой шаблон заполнять
        0 - общий шаблон с таблицами РТН
        1 - декларация промышленной безопасности
        """
        self.project_info = project_info
        self.object_info = object_info
        self.org_info = org_info
        self.doc_info = doc_info
        self.dev_info = dev_info
        self.pipe_info = pipe_info
        self.sub_info = sub_info
        self.sender_call = sender_call

    def all_table(self):
        self.path_template = Path(__file__).parents[1]

        context = {}
        context.update(self.org_info)
        context.update(self.object_info)
        context.update(self.project_info)
        context.update(self.doc_info)
        # Таблица с оборудованием
        context['dev_table'] = self.dev_info
        context['pipe_table'] = self.pipe_info
        # Таблица с распределением ОВ
        mass_in_dev_and_pipe = self.__calc_mass_in_device(self.dev_info, self.pipe_info, self.sub_info)
        context['mass_sub_table'] = mass_in_dev_and_pipe
        context['sum_sub'] = sum([float(i['Quantity']) for i in mass_in_dev_and_pipe])
        # Таблица с авариями
        if len(self.pipe_info) != 0:
            with open(f'{self.path_template}\\report\\templates\\oil_pipelines.txt', 'r', encoding="utf-8") as f:
                data_oil_pipe = f.read()
                context['oil_pipeline_accident_table'] = eval(data_oil_pipe)
        if len(self.dev_info) != 0:
            with open(f'{self.path_template}\\report\\templates\\oil_device.txt', 'r', encoding="utf-8") as f:
                data_oil_dev = f.read()
                context['oil_device_accident_table'] = eval(data_oil_dev)
        # vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
        # Таблица количества опасного вещества участвующего в аварии
        # vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
        all_table_data = []  # список всех таблиц
        # Т=30 С
        # Полная
        C1_1_max = self.__get_mass_accident(1, 30, mass_in_dev_and_pipe, type_hole=0)
        context['C1_1_max'] = C1_1_max
        context['C2_1_max'] = C1_1_max
        context['C3_1_max'] = C1_1_max
        context['C4_1_max'] = C1_1_max
        C1_2_max = self.__get_mass_accident(2, 30, mass_in_dev_and_pipe, type_hole=0)
        context['C1_2_max'] = C1_2_max
        context['C2_2_max'] = C1_2_max
        context['C3_2_max'] = C1_2_max
        context['C4_2_max'] = C1_2_max
        C1_3_max = self.__get_mass_accident(3, 30, mass_in_dev_and_pipe, type_hole=0)
        context['C1_3_max'] = C1_3_max
        context['C2_3_max'] = C1_3_max
        context['C3_3_max'] = C1_3_max
        context['C4_3_max'] = C1_3_max
        all_table_data.extend((C1_1_max, C1_2_max, C1_3_max))
        # 10 мм
        C1_1_max_10 = self.__get_mass_accident(1, 30, mass_in_dev_and_pipe, type_hole=1)
        context['C1_1_max_10'] = C1_1_max_10
        context['C2_1_max_10'] = C1_1_max_10
        context['C3_1_max_10'] = C1_1_max_10
        context['C4_1_max_10'] = C1_1_max_10
        C1_2_max_10 = self.__get_mass_accident(2, 30, mass_in_dev_and_pipe, type_hole=1)
        context['C1_2_max_10'] = C1_2_max_10
        context['C2_2_max_10'] = C1_2_max_10
        context['C3_2_max_10'] = C1_2_max_10
        context['C4_2_max_10'] = C1_2_max_10
        C1_3_max_10 = self.__get_mass_accident(3, 30, mass_in_dev_and_pipe, type_hole=1)
        context['C1_3_max_10'] = C1_3_max_10
        context['C2_3_max_10'] = C1_3_max_10
        context['C3_3_max_10'] = C1_3_max_10
        context['C4_3_max_10'] = C1_3_max_10
        all_table_data.extend((C1_1_max_10, C1_2_max_10, C1_3_max_10))
        # vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
        # Т=20 С
        # Полная
        C1_1_20 = self.__get_mass_accident(1, 20, mass_in_dev_and_pipe, type_hole=0)
        context['C1_1_20'] = C1_1_20
        context['C2_1_20'] = C1_1_20
        context['C3_1_20'] = C1_1_20
        context['C4_1_20'] = C1_1_20
        C1_2_20 = self.__get_mass_accident(2, 20, mass_in_dev_and_pipe, type_hole=0)
        context['C1_2_20'] = C1_2_20
        context['C2_2_20'] = C1_2_20
        context['C3_2_20'] = C1_2_20
        context['C4_2_20'] = C1_2_20
        C1_3_20 = self.__get_mass_accident(3, 20, mass_in_dev_and_pipe, type_hole=0)
        context['C1_3_20'] = C1_3_20
        context['C2_3_20'] = C1_3_20
        context['C3_3_20'] = C1_3_20
        context['C4_3_20'] = C1_3_20
        all_table_data.extend((C1_1_20, C1_2_20, C1_3_20))
        # 10мм
        C1_1_20_10 = self.__get_mass_accident(1, 20, mass_in_dev_and_pipe, type_hole=1)
        context['C1_1_20_10'] = C1_1_20_10
        context['C2_1_20_10'] = C1_1_20_10
        context['C3_1_20_10'] = C1_1_20_10
        context['C4_1_20_10'] = C1_1_20_10
        C1_2_20_10 = self.__get_mass_accident(2, 20, mass_in_dev_and_pipe, type_hole=1)
        context['C1_2_20_10'] = C1_2_20_10
        context['C2_2_20_10'] = C1_2_20_10
        context['C3_2_20_10'] = C1_2_20_10
        context['C4_2_20_10'] = C1_2_20_10
        C1_3_20_10 = self.__get_mass_accident(3, 20, mass_in_dev_and_pipe, type_hole=1)
        context['C1_3_20_10'] = C1_3_20_10
        context['C2_3_20_10'] = C1_3_20_10
        context['C3_3_20_10'] = C1_3_20_10
        context['C4_3_20_10'] = C1_3_20_10
        all_table_data.extend((C1_1_20_10, C1_2_20_10, C1_3_20_10))
        # vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
        # Т=10 С
        # Полная
        C1_1_10 = self.__get_mass_accident(1, 10, mass_in_dev_and_pipe, type_hole=0)
        context['C1_1_10'] = C1_1_10
        context['C2_1_10'] = C1_1_10
        context['C3_1_10'] = C1_1_10
        context['C4_1_10'] = C1_1_10
        C1_2_10 = self.__get_mass_accident(2, 10, mass_in_dev_and_pipe, type_hole=0)
        context['C1_2_10'] = C1_2_10
        context['C2_2_10'] = C1_2_10
        context['C3_2_10'] = C1_2_10
        context['C4_2_10'] = C1_2_10
        C1_3_10 = self.__get_mass_accident(3, 10, mass_in_dev_and_pipe, type_hole=0)
        context['C1_3_10'] = C1_3_10
        context['C2_3_10'] = C1_3_10
        context['C3_3_10'] = C1_3_10
        context['C4_3_10'] = C1_3_10
        all_table_data.extend((C1_1_10, C1_2_10, C1_3_10))
        # 10 мм
        C1_1_10_10 = self.__get_mass_accident(1, 10, mass_in_dev_and_pipe, type_hole=1)
        context['C1_1_10_10'] = C1_1_10_10
        context['C2_1_10_10'] = C1_1_10_10
        context['C3_1_10_10'] = C1_1_10_10
        context['C4_1_10_10'] = C1_1_10_10
        C1_2_10_10 = self.__get_mass_accident(2, 10, mass_in_dev_and_pipe, type_hole=1)
        context['C1_2_10_10'] = C1_2_10_10
        context['C2_2_10_10'] = C1_2_10_10
        context['C3_2_10_10'] = C1_2_10_10
        context['C4_2_10_10'] = C1_2_10_10
        C1_3_10_10 = self.__get_mass_accident(3, 10, mass_in_dev_and_pipe, type_hole=1)
        context['C1_3_10_10'] = C1_3_10_10
        context['C2_3_10_10'] = C1_3_10_10
        context['C3_3_10_10'] = C1_3_10_10
        context['C4_3_10_10'] = C1_3_10_10
        all_table_data.extend((C1_1_10_10, C1_2_10_10, C1_3_10_10))

        self.__save_fn_fg_chart(all_table_data)

        # Таблица взрывов
        # vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
        # Т=30 С
        # Полная
        context['C2_1_max_dP'] = C1_1_max
        context['C2_2_max_dP'] = C1_2_max
        context['C2_3_max_dP'] = C1_3_max
        # 10мм
        context['C2_1_max_10_dP'] = C1_1_max_10
        context['C2_2_max_10_dP'] = C1_2_max_10
        context['C2_3_max_10_dP'] = C1_3_max_10
        # vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
        # Т=20 С
        # Полная
        context['C2_1_20_dP'] = C1_1_20
        context['C2_2_20_dP'] = C1_2_20
        context['C2_3_20_dP'] = C1_3_20
        # 10мм
        context['C2_1_20_10_dP'] = C1_1_20_10
        context['C2_2_20_10_dP'] = C1_2_20_10
        context['C2_3_20_10_dP'] = C1_3_20_10
        # vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
        # Т=10 С
        # Полная
        context['C2_1_10_dP'] = C1_1_10
        context['C2_2_10_dP'] = C1_2_10
        context['C2_3_10_dP'] = C1_3_10
        # 10мм
        context['C2_1_10_10_dP'] = C1_1_10_10
        context['C2_2_10_10_dP'] = C1_2_10_10
        context['C2_3_10_10_dP'] = C1_3_10_10

        # Таблица пожаров
        # vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
        # Т=30 С
        # Полная
        context['C1_1_max_Q'] = C1_1_max
        context['C1_2_max_Q'] = C1_2_max
        context['C1_3_max_Q'] = C1_3_max
        # 10 мм
        context['C1_1_max_10_Q'] = C1_1_max_10
        context['C1_2_max_10_Q'] = C1_2_max_10
        context['C1_3_max_10_Q'] = C1_3_max_10
        # vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
        # Т=20 С
        # Полная
        context['C1_1_20_Q'] = C1_1_20
        context['C1_2_20_Q'] = C1_2_20
        context['C1_3_20_Q'] = C1_3_20
        # 10 мм
        context['C1_1_20_10_Q'] = C1_1_20_10
        context['C1_2_20_10_Q'] = C1_2_20_10
        context['C1_3_20_10_Q'] = C1_3_20_10
        # vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
        # Т=10 С
        # Полная
        context['C1_1_10_Q'] = C1_1_10
        context['C1_2_10_Q'] = C1_2_10
        context['C1_3_10_Q'] = C1_3_10
        # 10 мм
        context['C1_1_10_10_Q'] = C1_1_10_10
        context['C1_2_10_10_Q'] = C1_2_10_10
        context['C1_3_10_10_Q'] = C1_3_10_10

        # Таблица вспышек
        # vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
        # Т=30 С
        # Полная
        context['C3_1_max_NKPR'] = C1_1_max
        context['C3_2_max_NKPR'] = C1_2_max
        context['C3_3_max_NKPR'] = C1_3_max
        # 10 мм
        context['C3_1_max_10_NKPR'] = C1_1_max_10
        context['C3_2_max_10_NKPR'] = C1_2_max_10
        context['C3_3_max_10_NKPR'] = C1_3_max_10
        # Т=20 С
        # Полная
        context['C3_1_20_NKPR'] = C1_1_20
        context['C3_2_20_NKPR'] = C1_2_20
        context['C3_3_20_NKPR'] = C1_3_20
        # 10 мм
        context['C3_1_20_10_NKPR'] = C1_1_20_10
        context['C3_2_20_10_NKPR'] = C1_2_20_10
        context['C3_3_20_10_NKPR'] = C1_3_20_10
        # Т=20 С
        # Полная
        context['C3_1_10_NKPR'] = C1_1_10
        context['C3_2_10_NKPR'] = C1_2_10
        context['C3_3_10_NKPR'] = C1_3_10
        # 10 мм
        context['C3_1_10_10_NKPR'] = C1_1_10_10
        context['C3_2_10_10_NKPR'] = C1_2_10_10
        context['C3_3_10_10_NKPR'] = C1_3_10_10

        # Таблица ущерба
        # vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
        # Т=30 С
        # Полная
        context['C1_1_max_damage'] = C1_1_max
        context['C1_2_max_damage'] = C1_2_max
        context['C1_3_max_damage'] = C1_3_max
        # 100мм
        context['C1_1_max_10_damage'] = C1_1_max_10
        context['C1_2_max_10_damage'] = C1_2_max_10
        context['C1_3_max_10_damage'] = C1_3_max_10
        # Т=20 С
        # Полная
        context['C1_1_20_damage'] = C1_1_20
        context['C1_2_20_damage'] = C1_2_20
        context['C1_3_20_damage'] = C1_3_20
        # 100мм
        context['C1_1_20_10_damage'] = C1_1_20_10
        context['C1_2_20_10_damage'] = C1_2_20_10
        context['C1_3_20_10_damage'] = C1_3_20_10
        # Т=10 С
        # Полная
        context['C1_1_10_damage'] = C1_1_10
        context['C1_2_10_damage'] = C1_2_10
        context['C1_3_10_damage'] = C1_3_10
        # 100мм
        context['C1_1_10_10_damage'] = C1_1_10_10
        context['C1_2_10_10_damage'] = C1_2_10_10
        context['C1_3_10_10_damage'] = C1_3_10_10

        # Таблица риска
        # vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
        # Т=30 С
        # Полная 1 м/с
        context['C1_1_max_risk'] = C1_1_max
        context['C2_1_max_risk'] = C1_1_max
        context['C3_1_max_risk'] = C1_1_max
        context['C4_1_max_risk'] = C1_1_max
        # Полная 2 м/с
        context['C1_2_max_risk'] = C1_2_max
        context['C2_2_max_risk'] = C1_2_max
        context['C3_2_max_risk'] = C1_2_max
        context['C4_2_max_risk'] = C1_2_max
        # Полная 3 м/с
        context['C1_3_max_risk'] = C1_3_max
        context['C2_3_max_risk'] = C1_3_max
        context['C3_3_max_risk'] = C1_3_max
        context['C4_3_max_risk'] = C1_3_max
        # Т=20 С
        # Полная 1 м/с
        context['C1_1_20_risk'] = C1_1_20
        context['C2_1_20_risk'] = C1_1_20
        context['C3_1_20_risk'] = C1_1_20
        context['C4_1_20_risk'] = C1_1_20
        # Полная 2 м/с
        context['C1_2_20_risk'] = C1_2_20
        context['C2_2_20_risk'] = C1_2_20
        context['C3_2_20_risk'] = C1_2_20
        context['C4_2_20_risk'] = C1_2_20
        # Полная 3 м/с
        context['C1_3_20_risk'] = C1_3_20
        context['C2_3_20_risk'] = C1_3_20
        context['C3_3_20_risk'] = C1_3_20
        context['C4_3_20_risk'] = C1_3_20
        # Т=10 С
        # Полная 1 м/с
        context['C1_1_10_risk'] = C1_1_10
        context['C2_1_10_risk'] = C1_1_10
        context['C3_1_10_risk'] = C1_1_10
        context['C4_1_10_risk'] = C1_1_10
        # Полная 2 м/с
        context['C1_2_10_risk'] = C1_2_10
        context['C2_2_10_risk'] = C1_2_10
        context['C3_2_10_risk'] = C1_2_10
        context['C4_2_10_risk'] = C1_2_10
        # Полная 3 м/с
        context['C1_3_10_risk'] = C1_3_10
        context['C2_3_10_risk'] = C1_3_10
        context['C3_3_10_risk'] = C1_3_10
        context['C4_3_10_risk'] = C1_3_10
        # Т=30 С
        # 10мм 1 м/с
        context['C1_1_max_10_risk'] = C1_1_max_10
        context['C2_1_max_10_risk'] = C1_1_max_10
        context['C3_1_max_10_risk'] = C1_1_max_10
        context['C4_1_max_10_risk'] = C1_1_max_10
        # 10мм 2 м/с
        context['C1_2_max_10_risk'] = C1_2_max_10
        context['C2_2_max_10_risk'] = C1_2_max_10
        context['C3_2_max_10_risk'] = C1_2_max_10
        context['C4_2_max_10_risk'] = C1_2_max_10
        # 10мм 3 м/с
        context['C1_3_max_10_risk'] = C1_3_max_10
        context['C2_3_max_10_risk'] = C1_3_max_10
        context['C3_3_max_10_risk'] = C1_3_max_10
        context['C4_3_max_10_risk'] = C1_3_max_10
        # Т=20 С
        # 10мм 1 м/с
        context['C1_1_20_10_risk'] = C1_1_20_10
        context['C2_1_20_10_risk'] = C1_1_20_10
        context['C3_1_20_10_risk'] = C1_1_20_10
        context['C4_1_20_10_risk'] = C1_1_20_10
        # 10мм 2 м/с
        context['C1_2_20_10_risk'] = C1_2_20_10
        context['C2_2_20_10_risk'] = C1_2_20_10
        context['C3_2_20_10_risk'] = C1_2_20_10
        context['C4_2_20_10_risk'] = C1_2_20_10
        # 10мм 3 м/с
        context['C1_3_20_10_risk'] = C1_3_20_10
        context['C2_3_20_10_risk'] = C1_3_20_10
        context['C3_3_20_10_risk'] = C1_3_20_10
        context['C4_3_20_10_risk'] = C1_3_20_10
        # Т=10 С
        # 10мм 1 м/с
        context['C1_1_10_10_risk'] = C1_1_10_10
        context['C2_1_10_10_risk'] = C1_1_10_10
        context['C3_1_10_10_risk'] = C1_1_10_10
        context['C4_1_10_10_risk'] = C1_1_10_10
        # 10мм 2 м/с
        context['C1_2_10_10_risk'] = C1_2_10_10
        context['C2_2_10_10_risk'] = C1_2_10_10
        context['C3_2_10_10_risk'] = C1_2_10_10
        context['C4_2_10_10_risk'] = C1_2_10_10
        # 10мм 3 м/с
        context['C1_3_10_10_risk'] = C1_3_10_10
        context['C2_3_10_10_risk'] = C1_3_10_10
        context['C3_3_10_10_risk'] = C1_3_10_10
        context['C4_3_10_10_risk'] = C1_3_10_10

        # Индивидуальный и коллективный риск
        risk = self.__calc_ind_risk(all_table_data)
        context['Ind_risk'] = "{:.2e}".format(risk[0])
        context['Group_risk'] = "{:.2e}".format(risk[1])
        # Наиболее опасные и вероятные
        context['most_dangerous'] = self.__most_dangerous(C1_1_max)
        context['most_possible'] = self.__most_possible(C1_3_10_10)


        if self.sender_call == 0:
            doc = DocxTemplate(f'{self.path_template}\\report\\templates\\all_table_rtn.docx')
            # FN FG диаграммы
            context['fn'] = InlineImage(doc, f'{self.path_template}\\report\\templates\\fn.jpg', width=Mm(160))
            context['fg'] = InlineImage(doc, f'{self.path_template}\\report\\templates\\fg.jpg', width=Mm(160))
            # Заполним из словаря
            doc.render(context)
            text = str(int(time.time()))
            # Сохраним
            doc.save(f'{DESKTOP_PATH}\\{text}_{self.project_info["Project_code"]}_all_table_rtn.docx')
        elif self.sender_call == 1:
            print('ddsf')
            rpz = DocxTemplate(f'{self.path_template}\\report\\templates\\temp_rpz.docx')
            # FN FG диаграммы
            context['fn'] = InlineImage(rpz, f'{self.path_template}\\report\\templates\\fn.jpg', width=Mm(160))
            context['fg'] = InlineImage(rpz, f'{self.path_template}\\report\\templates\\fg.jpg', width=Mm(160))
            # Заполним из словаря
            rpz.render(context)
            text = str(int(time.time()))
            # Сохраним
            rpz.save(f'{DESKTOP_PATH}\\{text}_{self.project_info["Project_code"]}_rpz.docx')
        else:
            doc = DocxTemplate(f'{self.path_template}\\report\\templates\\all_table_rtn.docx')
            # FN FG диаграммы
            context['fn'] = InlineImage(doc, f'{self.path_template}\\report\\templates\\fn.jpg', width=Mm(160))
            context['fg'] = InlineImage(doc, f'{self.path_template}\\report\\templates\\fg.jpg', width=Mm(160))
            # Заполним из словаря
            doc.render(context)
            text = str(int(time.time()))
            # Сохраним
            doc.save(f'{DESKTOP_PATH}\\{text}_{self.project_info["Project_code"]}_all_table_rtn.docx')






    def __save_fn_fg_chart(self, data: list):
        pr = []  # вероятности
        ppl = []  # люди
        dmg = []  # ущерб
        for item in data:
            for dict_ in item:
                pr.extend((float(dict_['Frequency_C1']), float(dict_['Frequency_C2']),
                           float(dict_['Frequency_C3']), float(dict_['Frequency_C4'])))
                ppl.extend((float(dict_['Death_person_C1']), float(dict_['Death_person_C2']),
                            float(dict_['Death_person_C3']), float(dict_['Death_person_C4'])))
                dmg.extend((float(dict_['Dsum_C1']), float(dict_['Dsum_C2']),
                            float(dict_['Dsum_C3']), float(dict_['Dsum_C4'])))
        calc_fn_fg_chart.FN_FG_chart(f'{self.path_template}\\report\\templates').fn_chart([pr, ppl])
        calc_fn_fg_chart.FN_FG_chart(f'{self.path_template}\\report\\templates').fg_chart([pr, dmg])

    def __calc_ind_risk(self, data: list):
        group_risk = 0  # коллективный риск
        ppl_sum = 0  # люди
        for item in data:
            for dict_ in item:
                ppl_sum += float(dict_['Death_person_C1']) + float(dict_['Death_person_C2'])
                ppl_sum += float(dict_['Death_person_C3']) + float(dict_['Death_person_C4'])

                group_risk += float(dict_['Frequency_C1']) * float(dict_['Death_person_C1'])
                group_risk += float(dict_['Frequency_C2']) * float(dict_['Death_person_C2'])
                group_risk += float(dict_['Frequency_C3']) * float(dict_['Death_person_C3'])
                group_risk += float(dict_['Frequency_C4']) * float(dict_['Death_person_C4'])

        individual_risk = group_risk / ppl_sum
        return (individual_risk, group_risk)

    def __most_possible(self, data: list):
        dev = data[0]['Poz_sub']
        frequency = data[0]['Frequency_C4']
        dmg = data[0]['Dsum_C4']

        for item in data:
            if float(frequency) < float(item['Frequency_C4']):
                dev = item['Poz_sub']
                frequency = item['Frequency_C4']
                dmg = item['Dsum_C4']

        str_ = f'''наиболее вероятным сценарием является сценарий частичной разгерметизации С4_3_10_10 для обрудования (диаметр деффектного отверстия 10 мм, при длительном истечении): {dev.split()[0].replace(',', '')} с вероятностью возникновения {frequency} 1/год при метеоусловиях:  скорость ветра 3 м/с, температура воздуха воздуха 10 град.С. Ущерб при реализации данного сценария составляет: {dmg} млн.руб'''
        return str_

    def __most_dangerous(self, data: list):
        dev = data[0]['Poz_sub']
        frequency = data[0]['Frequency_C1']
        dmg = data[0]['Dsum_C1']

        for item in data:
            if float(dmg) < float(item['Dsum_C1']):
                dev = item['Poz_sub']
                frequency = item['Frequency_C1']
                dmg = item['Dsum_C1']

        str_ = f'''наиболее опасным сценарием является сценарий полного разрушения С1_1_30_0 для обрудования: {dev.split()[0].replace(',', '')} с вероятностью возникновения {frequency} 1/год при метеоусловиях:  скорость ветра 1 м/с, температура воздуха воздуха более 30 град.С. Ущерб при реализации данного сценария составляет: {dmg} млн.руб'''
        return str_

    def __calc_mass_in_device(self, dev_info: list, pipe_info: list, sub_info: list):
        """
        Расчет количества опасного вещества в оборудовании
        :param dev_info: список словарей оборудования
        :param pipe_info: спиок словарей трубопроводов
        :param sub_info: список словарей веществ
        :return: mass_list список словарей оборудования с распределением веществ
        """
        mass_list = []
        for item in dev_info:
            dev_dict = {}
            dev_dict['Locations'] = item['Locations']
            dev_dict['Spill_square'] = float(item['Spill_square'])
            dev_dict['Flow'] = 0  # допущение что для емкостного оборудования притока нет
            sub = self.__get_sub(sub_info, item['SubId'])
            dev_dict['Poz_sub'] = f"{item['Pozition']}, {sub['Name_sub']}"
            dev_dict['Volume'] = float(item['Volume'])
            dev_dict['Quantity'] = round((float(item['Volume']) * float(item['Completion'].replace(",", ".")) * float(
                sub['Density'].replace(",", "."))) / KG_TO_TONN, 2)
            dev_dict['State'] = 'г.ф.+ж.ф.' if item['Completion'] != 1 else 'ж.ф.'
            dev_dict['Pressure'] = item['Pressure']
            dev_dict['Temperature'] = item['Temperature']
            # получим свойства вещества
            dev_dict['Class_substance'] = float(sub['Class_substance'].replace(",", "."))
            dev_dict['Cost'] = float(sub['Cost'].replace(",", "."))
            dev_dict['Density'] = float(sub['Density'].replace(",", "."))
            dev_dict['Density_gas'] = float(sub['Density_gas'].replace(",", "."))
            dev_dict['Energy_level'] = float(sub['Energy_level'].replace(",", "."))
            dev_dict['Flash_temperature'] = float(sub['Flash_temperature'].replace(",", "."))
            dev_dict['Heat_of_combustion'] = int(sub['Heat_of_combustion'].replace(",", "."))
            dev_dict['Lower_concentration'] = float(sub['Lower_concentration'].replace(",", "."))
            dev_dict['Molecular_weight'] = float(sub['Molecular_weight'].replace(",", "."))
            dev_dict['Sigma'] = float(sub['Sigma'].replace(",", "."))
            dev_dict['Steam_pressure'] = float(sub['Steam_pressure'].replace(",", "."))
            dev_dict['Boiling_temperature'] = float(sub['Boiling_temperature'].replace(",", "."))
            dev_dict['Type_device'] = item['Type_device']
            dev_dict['Death_person'] = int(item['Death_person'])
            dev_dict['Injured_person'] = int(item['Injured_person'])
            dev_dict['View_space'] = int(item['View_space'])

            mass_list.append(dev_dict)

        for item in pipe_info:
            pipe_dict = {}
            pipe_dict['Locations'] = item['Locations']
            sub = self.__get_sub(sub_info, item['SubId'])
            pipe_dict['Poz_sub'] = f"{item['Pozition']}, {sub['Name_sub']}"

            diametr = float(item['Diameter'].replace(",", "."))
            lenght = float(item['Length'].replace(",", "."))
            density = float(sub['Density'].replace(",", "."))
            volume = self.__get_volume_pipe(diametr, lenght)

            pipe_dict['Flow'] = float(item['Flow'].replace(",", "."))
            part = (((pipe_dict['Flow'] * CUT_OFF_TIME) * TONN_TO_KG / (DAY_TO_HOUR * HOUR_TO_SECONDS)) / float(
                sub['Density'].replace(",", "."))) * LAYER_THICKNESS
            pipe_dict['Spill_square'] = volume * LAYER_THICKNESS + part
            pipe_dict['Quantity'] = round((volume * density) / KG_TO_TONN, 2)  # M, т
            pipe_dict['State'] = 'ж.ф.'
            pipe_dict['Pressure'] = item['Pressure']
            pipe_dict['Temperature'] = item['Temperature']
            # получим свойства вещества
            pipe_dict['Class_substance'] = float(sub['Class_substance'].replace(",", "."))
            pipe_dict['Cost'] = float(sub['Cost'].replace(",", "."))
            pipe_dict['Density'] = float(sub['Density'].replace(",", "."))
            pipe_dict['Density_gas'] = float(sub['Density_gas'].replace(",", "."))
            pipe_dict['Energy_level'] = float(sub['Energy_level'].replace(",", "."))
            pipe_dict['Flash_temperature'] = float(sub['Flash_temperature'].replace(",", "."))
            pipe_dict['Heat_of_combustion'] = int(sub['Heat_of_combustion'].replace(",", "."))
            pipe_dict['Lower_concentration'] = float(sub['Lower_concentration'].replace(",", "."))
            pipe_dict['Molecular_weight'] = float(sub['Molecular_weight'].replace(",", "."))
            pipe_dict['Sigma'] = float(sub['Sigma'].replace(",", "."))
            pipe_dict['Steam_pressure'] = float(sub['Steam_pressure'].replace(",", "."))
            pipe_dict['Boiling_temperature'] = float(sub['Boiling_temperature'].replace(",", "."))
            pipe_dict['Type_device'] = -1
            pipe_dict['Length'] = item['Length']
            pipe_dict['Diameter'] = item['Diameter']
            pipe_dict['Death_person'] = int(item['Death_person'])
            pipe_dict['Injured_person'] = int(item['Injured_person'])
            pipe_dict['View_space'] = int(item['View_space'])

            mass_list.append(pipe_dict)

        return mass_list

    def __get_sub(self, sub_info: list, id: int) -> dict:
        """
        Функция возрвщает словарь сос свойствами вещества
        :param sub_info: список словарей свойств веществ
        :param id: id вещества которое нужно вытащить из sub_info
        :return: item словарь со свойствами вещества
        """
        # Посмотрим каждое вещество, если id совпадает, то вернем его свойства
        for item in sub_info:
            if item['Id'] == id:
                return item
        # Если ничего не нашли, то вернем типовые свойства
        item = {'Boiling_temperature': '330',
                'Class_substance': '1',
                'Cost': '60000',
                'Density': '800',
                'Density_gas': '4',
                'Energy_level': '1',
                'Flash_temperature': '10',
                'Heat_of_combustion': '45309',
                'Id': 0,
                'Lower_concentration': '4',
                'Molecular_weight': '160',
                'Name_sub': 'Нефть_типовая',
                'Sigma': '4',
                'Steam_pressure': '50'}
        return item

    def __get_volume_pipe(self, diametr: float, lenght: float):
        """
        Получение объема трубопровода, м3
        :param diametr: диаметр, мм
        :param lenght: длина, км
        :return: объем, м3
        """
        return math.pi * math.pow(diametr / 2000, 2) * (lenght * 1000)

    def __get_mass_accident(self, wind_velocity: int, air_temperature: int, characteristics: list,
                            type_hole: int) -> list:
        """
        :param wind_velocity: скорость ветра, м/с
        :param air_temperature: температура воздуха, град.С
        :param characteristics: характеристики оборудования и вещества в нем
        :param type_hole: тип разгерметизации
                            0 - полная
                            1 - 10мм продолжительный выброс

        :return: список словарей с характеристиками оборудования и испарившейся массы
        """
        characteristics = copy.deepcopy(characteristics)
        result = []
        wind_index = (1, 2, 3).index(wind_velocity) if wind_velocity in (1, 2, 3) else 0
        temperature_index = (10, 20, 30).index(air_temperature) if air_temperature in (10, 20, 30) else 0
        z = self.__get_array_z()[wind_index][temperature_index]

        for item in characteristics:
            # 1. Определим количество испарившегося
            steam_arr = self.__get_array_steam_pressure(item['Steam_pressure'])
            steam_pressure = steam_arr[wind_index][temperature_index]
            item['Steam_pressure'] = steam_pressure  # заменим давление пара на расчетное
            # Определим коэф.участия в зависимости от типа разгерметизации
            k = (1, 0.45)
            item['Emergency_weight'] = round(
                (item['Quantity'] + (item['Flow'] * CUT_OFF_TIME) / (DAY_TO_HOUR * HOUR_TO_SECONDS)) * k[
                    type_hole] * TONN_TO_KG, 2)

            item['Spill_fire'] = int(item['Spill_square'] * k[type_hole])

            evaporation_mass = ev.Liquid_evaporation().evaporation_in_moment(TIME_EVAPORATION,
                                                                             item['Steam_pressure'],
                                                                             item['Molecular_weight'],
                                                                             item['Spill_fire'])[0]

            item['Evaporation'] = (
                round(evaporation_mass * z, 2) if evaporation_mass / KG_TO_TONN < item['Quantity'] else item[
                    'Quantity'])

            # 2. Определим сценарии аварии
            wind_speed, temperature, _, _ = weather.Weather.get_statistic_weather(
                self.object_info['Address_opo'].split()[0])



            if item['Type_device'] == -1:
                probability = pr.Probability().probability_rosteh_tube(
                    int(float(item['Length'].replace(",", ".")) * KM_TO_M),
                    int(item['Diameter'].replace(",", ".")))
            else:
                probability = pr.Probability().probability_rosteh_device(int(item['Type_device']))

            chance = float(probability[type_hole]) * wind_speed[wind_index] * temperature[temperature_index]
            tree_arr = tree.Event_tree.mchs_liquid(float(item['Flash_temperature']), item['Flow'], chance)

            item['Frequency_C1'] = tree_arr[0]
            item['Frequency_C2'] = tree_arr[1]
            item['Frequency_C3'] = tree_arr[2]
            item['Frequency_C4'] = tree_arr[3]

            # 3. Расчитаем взрыв
            item['dP100'], item['dP53'], item['dP28'], item['dP12'], item['dP5'], item[
                'dP3'] = expl.Explosion().explosion_class_zone(class_substance=int(item['Class_substance']),
                                                               view_space=item['View_space'],
                                                               mass=round(evaporation_mass * z, 2),
                                                               heat_of_combustion=item['Heat_of_combustion'],
                                                               sigma=item['Sigma'],
                                                               energy_level=item['Energy_level'])

            # 4. Расчитаем пожар пролива
            item['q10'], item['q7'], item['q4'], item['q1'] = fire.Strait_fire().termal_class_zone(
                S_spill=item['Spill_fire'],
                m_sg=0.06,
                mol_mass=item['Molecular_weight'],
                t_boiling=item['Boiling_temperature'], wind_velocity=wind_velocity)

            # 5. Расчитаем вспышку
            item['Nkpr'], item['Flash'] = nkpr.LCLP().lower_concentration_limit(mass=round(evaporation_mass * z, 2),
                                                                                mol_mass=item['Molecular_weight'],
                                                                                t_boiling=item['Boiling_temperature'],
                                                                                lower_concentration=item[
                                                                                    'Lower_concentration'])

            # 6. Расчитаем погибших и пострадавших

            tuple_dead_people = (
                (item['Death_person'], 0),
                (0, 0)
            )[type_hole]

            tuple_injured_people = (
                (item['Injured_person'], 1),
                (1, 1)
            )[type_hole]

            item['Death_person_C1'] = tuple_dead_people[type_hole]
            item['Death_person_C2'] = round(tuple_dead_people[type_hole] / 2)
            item['Death_person_C3'] = item['Death_person_C2']
            item['Death_person_C4'] = 0

            item['Injured_person_C1'] = tuple_injured_people[type_hole]
            item['Injured_person_C2'] = round(tuple_injured_people[type_hole] / 2)
            item['Injured_person_C3'] = item['Injured_person_C2']
            item['Injured_person_C4'] = 0

            # 7. Ущерб.
            if item['Type_device'] == -1:
                volume = 0
                diametr = int(item['Diameter'].replace(",", "."))
                lenght = int(float(item['Length'].replace(",", ".")) * KM_TO_M)
            else:
                volume = item['Volume'] * k[type_hole]
                diametr = 0
                lenght = 0

            C1_damage = damage.Damage().damage_array(volume=volume, diametr=diametr, lenght=lenght,
                                                     cost_sub=item['Cost'] * pow(10, -6),
                                                     part_sub=1,
                                                     death_person=item['Death_person_C1'],
                                                     injured_person=item['Injured_person_C1'],
                                                     m_out_spill=evaporation_mass / KG_TO_TONN,
                                                     m_in_spill=item['Emergency_weight'] / KG_TO_TONN,
                                                     S_spill=item['Spill_fire'])

            item['D1_C1'], item['D2_C1'], item['D3_C1'], item['D4_C1'], item['D5_C1'], item['D6_C1'], item[
                'Dsum_C1'] = (
                C1_damage[0], C1_damage[1], C1_damage[2], C1_damage[3], C1_damage[8], C1_damage[7], C1_damage[9])

            C2_damage = damage.Damage().damage_array(volume=volume, diametr=diametr, lenght=lenght,
                                                     cost_sub=item['Cost'] * pow(10, -6),
                                                     part_sub=0.4,
                                                     death_person=item['Death_person_C2'],
                                                     injured_person=item['Injured_person_C2'],
                                                     m_out_spill=evaporation_mass / KG_TO_TONN,
                                                     m_in_spill=item[
                                                                    'Emergency_weight'] / KG_TO_TONN,
                                                     S_spill=item['Spill_fire'])

            item['D1_C2'], item['D2_C2'], item['D3_C2'], item['D4_C2'], item['D5_C2'], item['D6_C2'], item[
                'Dsum_C2'] = (
                C2_damage[0], C2_damage[1], C2_damage[2], C2_damage[3], C2_damage[8], C2_damage[7], C2_damage[9])

            C3_damage = damage.Damage().damage_array(volume=volume, diametr=diametr, lenght=lenght,
                                                     cost_sub=item['Cost'] * pow(10, -6),
                                                     part_sub=0.3,
                                                     death_person=item['Death_person_C3'],
                                                     injured_person=item['Injured_person_C3'],
                                                     m_out_spill=evaporation_mass / KG_TO_TONN,
                                                     m_in_spill=item[
                                                                    'Emergency_weight'] / KG_TO_TONN,
                                                     S_spill=item['Spill_fire'])

            item['D3_C3'], item['D2_C3'], item['D3_C3'], item['D4_C3'], item['D5_C3'], item['D6_C3'], item[
                'Dsum_C3'] = (
                C3_damage[0], C3_damage[1], C3_damage[2], C3_damage[3], C3_damage[8], C3_damage[7], C3_damage[9])

            C4_damage = damage.Damage().damage_array(volume=volume, diametr=diametr, lenght=lenght,
                                                     cost_sub=item['Cost'] * pow(10, -6),
                                                     part_sub=0.1,
                                                     death_person=item['Death_person_C4'],
                                                     injured_person=item['Injured_person_C4'],
                                                     m_out_spill=evaporation_mass / KG_TO_TONN,
                                                     m_in_spill=item[
                                                                    'Emergency_weight'] / KG_TO_TONN,
                                                     S_spill=item['Spill_fire'])

            item['D3_C4'], item['D2_C4'], item['D3_C4'], item['D4_C4'], item['D5_C4'], item[
                'D6_C4'], item['Dsum_C4'] = (
                C4_damage[0], C4_damage[1], C4_damage[2], C4_damage[3], C4_damage[8], C4_damage[7], C4_damage[9])

            # Риск мат ожидание
            item['Risk_C1'] = "{:.2e}".format(float(item['Frequency_C1']) * float(item['Dsum_C1']))
            item['Risk_C2'] = "{:.2e}".format(float(item['Frequency_C2']) * float(item['Dsum_C2']))
            item['Risk_C3'] = "{:.2e}".format(float(item['Frequency_C3']) * float(item['Dsum_C3']))
            item['Risk_C4'] = "{:.2e}".format(float(item['Frequency_C4']) * float(item['Dsum_C4']))

            # Добавление item  врезультирующий список
            result.append(item)
            # Удаление из словаря 0 значений
            for i in result:
                if 0 == float(i['Frequency_C1']): result.pop(result.index(i))

        return result

    def __get_array_steam_pressure(self, steam_pressure) -> tuple:
        """
        Получить массив значений давлений насыщенного пара, для различных скоростей ветра и температур
        t/v    10      20    30
        1     0,75x    x     1.25x
        2     0,75y    y     1.25y
        3     0,75z    z     1.25z
        """
        x = steam_pressure
        y = steam_pressure * 1.1
        z = steam_pressure * 1.2
        return ((0.75 * x, x, 1.25 * x),
                (0.75 * y, y, 1.25 * y),
                (0.75 * z, z, 1.25 * z))

    def __get_array_z(self, z: float = 0.1) -> tuple:
        """
        Получить массив значений давлений насыщенного пара, для различных скоростей ветра и температур
        t/v    10      20         30
        1      z       z          z
        2     0,07    0,07       0,07
        3     0,04    0,04       0,04
        """

        return ((z, z, z),
                (0.07, 0.07, 0.07),
                (0.04, 0.04, 0.04))


if __name__ == '__main__':
    pipe_info = [{'Death_person': '1',
                  'Diameter': '89',
                  'Flow': '10',
                  'Ground': 'Подземное',
                  'Id': 53,
                  'Injured_person': '2',
                  'Length': '0,852',
                  'Locations': 'Онбийское м.н.',
                  'Material': 'Сталь',
                  'Name': 'Нефтепровод',
                  'Pozition': 'Трубопровод от К-19 до БГ',
                  'Pressure': '0,55',
                  'ProjectsId': 28,
                  'SubId': 3,
                  'Target': 'Транспорт нефти',
                  'Temperature': '10',
                  'View_space': '4'},
                 {'Death_person': '2',
                  'Diameter': '159',
                  'Flow': '12',
                  'Ground': 'Подземное',
                  'Id': 54,
                  'Injured_person': '2',
                  'Length': '0,88',
                  'Locations': 'Онбйское м.н.',
                  'Material': 'Сталь В20',
                  'Name': 'Трубопровд',
                  'Pozition': 'К-99',
                  'Pressure': '2',
                  'ProjectsId': 28,
                  'SubId': 2,
                  'Target': 'Транспорт нефти',
                  'Temperature': '10',
                  'View_space': '4'}]

    dev_info = [{'Completion': '0,8',
                 'Death_person': '2',
                 'Ground': 'Наземное',
                 'Id': 55,
                 'Injured_person': '2',
                 'Locations': 'Онбийское м.н.',
                 'Material': 'Сталь',
                 'Name': 'Емкость',
                 'Pozition': 'Е-12',
                 'Pressure': '1,2',
                 'ProjectsId': 28,
                 'Spill_square': '200',
                 'SubId': 1,
                 'Target': 'Хранение нефти',
                 'Temperature': '30',
                 'Type_device': '0',
                 'View_space': '3',
                 'Volume': '100'}]

    doc_info = {'Book_dpb': 'Книга 1. Декларация промышленной безопасности',
                'Book_gochs': '-',
                'Book_ifl': 'Книга 3. ИФЛ',
                'Book_rpz': 'Книга 2. Расчетно-пояснительная записка',
                'Code_dpb': '48-19-ДПБ-',
                'Code_fire_safety': '48-19-ПБ',
                'Code_gochs': '48-19-ИТМ',
                'Code_ifl': '48-19-ДПБ3',
                'Code_rpz': '48-19-ДПБ2',
                'Id': 27,
                'Part_other_documentation_dpb': 'Часть 1. Декларация промышленной '
                                                'безопасности.',
                'Part_other_documentation_gochs': 'Часть 2. ГОЧС.',
                'ProjectsId': 28,
                'Section_fire_safety': 'Раздел 9. ПБ',
                'Section_other_documentation': 'Раздел 12. Иная документация в случаях, '
                                               'предусмотр',
                'Tom_dpb': '12.1.1',
                'Tom_fire_safety': '9',
                'Tom_gochs': '12.2',
                'Tom_ifl': '12.1.3',
                'Tom_rpz': '12.1.2'}

    org_info = {'Date_get_license': '14.04.2016',
                'Director': 'Генеральный директор',
                'Email': '-',
                'Fax': '(8553) 39-70-70',
                'Id': 1,
                'Jur_adress': 'Республика Татарстан, г. Альметьевск, ул. Маяковского, д. 116',
                'License': 'ВП-00-010185',
                'Name_director': 'Хайруллин Ирек Акрамович',
                'Name_org': 'ООО "Татех"',
                'Name_org_full': 'Общество с ограниченной ответственностью',
                'Name_tech_director': 'Верия Евгений Иванович',
                'Tech_director': 'Главный инженер',
                'Telephone': '(8553) 39-70-01'}

    object_info = {'Address_opo': 'Заинский муниципальный район',
                   'Class_opo': '1',
                   'Id': 6,
                   'Name_opo': 'Система промысловых трубопроводов Онбийского нефтяного '
                               'месторождения',
                   'OrganizationId': 1,
                   'Reg_number_opo': 'А43-09862-003'}

    project_info = {'Id': 28,
                    'Name_project': '«Обустройство дополнительных скважин Онбийского нефтяного '
                                    'месторождения АО «Татех»',
                    'ObjectsId': 6,
                    'Project_automat': 'Для обеспечения сбора информации и управления '
                                       'проектируемыми объектами данным подразделом проектной '
                                       'документации предусматривается организация каналов '
                                       'передачи технологической информации с объектов добычи '
                                       'Онбийского нефтяного месторождения АО «Татех».\n'
                                       'Согласно проектной документации передача данных с '
                                       'контролируемых объектов (куст скважин К-583Б) '
                                       'предусматривается по радиоканалу в диапазоне '
                                       'ультракоротких волн на частоте 433...447 МГц посредством '
                                       'радиомодема «Спектр 9600GM» и направленной антен-ны '
                                       'Y6UHF.\n'
                                       'Проектируемые объекты подключаются к существующей системе '
                                       'сбора и управления с передачей данных в существующий '
                                       'диспетчерский пункт (ДП) при ДНС-30 АО «Татех».\n'
                                       'Для передачи технологической информации с проектированных '
                                       'скважин, оборудо-ванных приводом ПНШТ-60 (5 шт.), '
                                       'устанавливаются станции управления «СУЭН-1-ПЧ-15-Ш», '
                                       'сигналы о работе которых по кабелю «витая пара» и '
                                       'интерфейсу RS-485 в поступают программируемый контроллер '
                                       'DirectLOGICD0-06DR. Далее информация при помощи '
                                       'ра-диомодема «Спектр 9600GM» ООО «Ратеос» с направленной '
                                       'антенной Y6UHF поступает в сеть обмена данными и далее '
                                       'передается в диспетчерский пункт (ДП) при ДНС-30.\n',
                    'Project_code': '119-20',
                    'Project_description': 'К моменту разработки данного проекта Онбийское '
                                           'нефтяное месторождение достаточ-но обустроено. '
                                           'Промысловая система сбора продукции скважин '
                                           'представляет собой ком-плекс инженерных сооружений и '
                                           'коммуникаций, обеспечивающий замер и транспорт '
                                           'про-дукции.\n'
                                           'На проектируемом объекте проектной документацией '
                                           'предусматривается герметизи-рованная однотрубная '
                                           'система сбора и транспорта продукции скважин по '
                                           'следующим тех-нологическим схемам:\n'
                                           'Продукция проектируемых добывающих скважин под '
                                           'устьевым давлением не более 2МПа после замера дебитов '
                                           'на БГЗЖ по выкидным трубопроводам транспортируется до '
                                           'точки врезки в существующий промысловый трубопровод и '
                                           'далее поступает на ДНС-30 Онбийского нефтяного '
                                           'месторождения.\n'
                                           'В соответствии с принятой технологической схемой в '
                                           'составе системы сбора и транс-порта продукции скважин '
                                           'предусматриваются:\n'
                                           '- обустройства устьев скважин;\n'
                                           '- блок гребенок замера жидкости;\n'
                                           '- блок подачи реагента БДПР-1,6/1/0,4;\n'
                                           '- нефтегазопроводы - по ТУ 1390-007-67740692-2010, ТУ '
                                           '1390-001-67740692-2010.\n'
                                           'Трассирование нефтесборных сетей, выбрано исходя из '
                                           'соблюдения интересов земле-пользователей на границах '
                                           'угодий, с занятием минимальной площади менее ценных '
                                           'земель.\n'}

    sub_info = [{'Boiling_temperature': '359',
                 'Class_substance': '1',
                 'Cost': '60000',
                 'Density': '900',
                 'Density_gas': '3',
                 'Energy_level': '1',
                 'Flash_temperature': '16',
                 'Heat_of_combustion': '45367',
                 'Id': 1,
                 'Lower_concentration': '3',
                 'Molecular_weight': '152',
                 'Name_sub': 'Нефть_900',
                 'Sigma': '4',
                 'Steam_pressure': '49'},
                {'Boiling_temperature': '330',
                 'Class_substance': '1',
                 'Cost': '60000',
                 'Density': '800',
                 'Density_gas': '4',
                 'Energy_level': '1',
                 'Flash_temperature': '10',
                 'Heat_of_combustion': '45309',
                 'Id': 2,
                 'Lower_concentration': '4',
                 'Molecular_weight': '160',
                 'Name_sub': 'Нефть_800',
                 'Sigma': '4',
                 'Steam_pressure': '50'},
                {'Boiling_temperature': '367',
                 'Class_substance': '3',
                 'Cost': '60000',
                 'Density': '850',
                 'Density_gas': '5',
                 'Energy_level': '1',
                 'Flash_temperature': '12',
                 'Heat_of_combustion': '45136',
                 'Id': 3,
                 'Lower_concentration': '4',
                 'Molecular_weight': '174',
                 'Name_sub': 'Нефть_850',
                 'Sigma': '4',
                 'Steam_pressure': '51'}]
    r = Report(project_info, object_info, org_info, doc_info, dev_info, pipe_info, sub_info)
    r.all_table()


