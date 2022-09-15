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

DESKTOP_PATH = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')


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
        context['dev_table'] = self.dev_info
        context['pipe_table'] = self.pipe_info
        doc.render(context)
        text = str(int(time.time()))
        doc.save(f'{DESKTOP_PATH}\\{text}_{project_info["Project_code"]}_all_table.docx')

    def _calc_mass_in_device(self, dev_info: dict):
        for item in dev_info:
            print(item['Volume'])
            print(item['Completion'])
            print(item['SubId'])
            mass_sub = item['Volume'] * item['Completion'] * item['Completion']  # аварийная масса выброса, кг


if __name__ == '__main__':
    r = Report(project_info, object_info, org_info, doc_info, dev_info, pipe_info, sub_info)
    r.all_table()
