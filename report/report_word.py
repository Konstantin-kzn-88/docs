from pprint import pprint

pipe_info = [{'Death_person': '1',
              'Diameter': '114',
              'Flow': '5',
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
              'SubId': 1,
              'Target': 'Транспорт нефти',
              'Temperature': '10',
              'View_space': '4'},
             {'Death_person': '1',
              'Diameter': '159',
              'Flow': '6',
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
              'SubId': 1,
              'Target': 'Транспорт нефти',
              'Temperature': '10',
              'View_space': '4'}]

dev_info = [{'Completion': '0,8',
             'Death_person': '1',
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

from docxtpl import DocxTemplate, InlineImage
from pathlib import Path
import time
import os
import math
from calc import calc_liguid_evaporation as ev
from risk import risk_statistics_weather as weather
from risk import risk_probability as pr
from risk import risk_event_tree as tree

DESKTOP_PATH = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
LAYER_THICKNESS = 20  # м^-1
KG_TO_TONN = 1000  # 1000 кг = 1000/KG_TO_TONN = 1 тонна
TONN_TO_KG = 1000  # 1т = 1*TONN_TO_KG = 1000 кг
KM_TO_M = 1000  # 1км = 1*KM_TO_M = 1000 м
CUT_OFF_TIME = 12  # секунд
TIME_EVAPORATION = 3600  # секунд


class Report:
    def __init__(self, project_info: dict, object_info: dict, org_info: dict, doc_info: dict, dev_info: list,
                 pipe_info: list, sub_info: list):
        self.project_info = project_info
        self.object_info = object_info
        self.org_info = org_info
        self.doc_info = doc_info
        self.dev_info = dev_info
        self.pipe_info = pipe_info
        self.sub_info = sub_info

    def all_table(self):
        path_template = Path(__file__).parents[1]
        doc = DocxTemplate(f'{path_template}\\report\\templates\\all_table.docx')
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
            with open(f'{path_template}\\report\\templates\\oil_pipelines.txt', 'r', encoding="utf-8") as f:
                data_oil_pipe = f.read()
                context['oil_pipeline_accident_table'] = eval(data_oil_pipe)
        if len(self.dev_info) != 0:
            with open(f'{path_template}\\report\\templates\\oil_device.txt', 'r', encoding="utf-8") as f:
                data_oil_dev = f.read()
                context['oil_device_accident_table'] = eval(data_oil_dev)
        # Таблица количества опасного вещества участвующего в аварии
        context['mass_С1_1_tmax_table'] = self.__get_mass_accident(1, 30, mass_in_dev_and_pipe, type_hole=0)
        context['mass_С2_1_tmax_table'] = self.__get_mass_accident(1, 30, mass_in_dev_and_pipe, type_hole=0)

        doc.render(context)
        text = str(int(time.time()))
        doc.save(f'{DESKTOP_PATH}\\{text}_{project_info["Project_code"]}_all_table.docx')

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
            dev_dict['Heat_of_combustion'] = float(sub['Heat_of_combustion'].replace(",", "."))
            dev_dict['Lower_concentration'] = float(sub['Lower_concentration'].replace(",", "."))
            dev_dict['Molecular_weight'] = float(sub['Molecular_weight'].replace(",", "."))
            dev_dict['Sigma'] = float(sub['Sigma'].replace(",", "."))
            dev_dict['Steam_pressure'] = float(sub['Steam_pressure'].replace(",", "."))
            dev_dict['Type_device'] = item['Type_device']

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
            pipe_dict['Spill_square'] = volume * LAYER_THICKNESS
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
            pipe_dict['Heat_of_combustion'] = float(sub['Heat_of_combustion'].replace(",", "."))
            pipe_dict['Lower_concentration'] = float(sub['Lower_concentration'].replace(",", "."))
            pipe_dict['Molecular_weight'] = float(sub['Molecular_weight'].replace(",", "."))
            pipe_dict['Sigma'] = float(sub['Sigma'].replace(",", "."))
            pipe_dict['Steam_pressure'] = float(sub['Steam_pressure'].replace(",", "."))
            pipe_dict['Type_device'] = -1
            pipe_dict['Length'] = item['Length']
            pipe_dict['Diameter'] = item['Diameter']

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
                            1 - 100 мм
                            2 - 50 мм
                            3 - 25 мм
                            4 - 12 мм
        :return: список словарей с характеристиками оборудования и испарившейся массы
        """
        result = []
        wind_index = (1, 2, 3).index(wind_velocity) if wind_velocity in (1, 2, 3) else 0
        temperature_index = (10, 20, 30).index(air_temperature) if air_temperature in (1, 2, 3) else 0

        for item in characteristics:
            # 1. Определим количество испарившегося
            steam_arr = self.__get_array_steam_pressure(item['Steam_pressure'])
            steam_pressure = steam_arr[wind_index][temperature_index]
            item['Steam_pressure'] = steam_pressure  # заменим даление пара на расчетное
            evaporation_mass = ev.Liquid_evaporation().evaporation_in_moment(TIME_EVAPORATION,
                                                                             item['Steam_pressure'],
                                                                             item['Molecular_weight'],
                                                                             item['Spill_square'])[0]

            item['Evaporation'] = (
                round(evaporation_mass / KG_TO_TONN, 2) if evaporation_mass / KG_TO_TONN < item['Quantity'] else item[
                    'Quantity'])

            result.append(item)
            # 2. Определим сценарии аварии
            wind_speed, temperature, _, _ = weather.Weather.get_statistic_weather(
                self.object_info['Address_opo'].split()[0])
            if item['Type_device'] == -1:
                probability = pr.Probability().probability_mchs_tube(
                    int(float(item['Length'].replace(",", ".")) * KM_TO_M),
                    int(item['Diameter'].replace(",", ".")))
            else:
                probability = pr.Probability().probability_mchs_device(
                    0 if float(item['Pressure'].replace(",", ".")) else 1)

            poz_ = 4 - type_hole
            temp = float(probability[poz_]) * wind_speed[wind_index] * temperature[temperature_index]
            tree_arr = tree.Event_tree.mchs_liquid(float(item['Flash_temperature']), item['Flow'], temp)

            item['Frequency_C1'] = tree_arr[0]
            item['Frequency_C2'] = tree_arr[1]

        return result

    def __get_array_steam_pressure(self, steam_pressure):
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


if __name__ == '__main__':
    r = Report(project_info, object_info, org_info, doc_info, dev_info, pipe_info, sub_info)
    r.all_table()
