import sys
import os

from pathlib import Path
from PySide2.QtSql import QSqlDatabase, QSqlQuery, QSqlRelationalTableModel, QSqlRelation
from PySide2.QtWidgets import QApplication, QMainWindow, QComboBox, QMessageBox, QWidget, QGridLayout, \
    QFormLayout, QGroupBox, QTableView, QStyleFactory, QStyledItemDelegate, QHeaderView, QMenu, QAction, QDialog, \
    QDialogButtonBox, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel, \
    QSpinBox
from PySide2.QtGui import QIcon
from PySide2.QtCore import Qt
from itertools import count
from pprint import pprint
from report import report_word_rtn
from report import report_word

db = QSqlDatabase.addDatabase("QMYSQL")
db.setHostName("server167.hosting.reg.ru")
db.setDatabaseName("u1082920_docs_db")
db.setUserName("u1082920_qt_cl")
db.setPassword("1201kZn1201!")
db.open()

if db.open():
    print("Database Open!")
else:
    print(f"Database NOT Open cause {db.lastError().text()}")


class ReadOnlyDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, insex):
        # print(f'parent=`{parent}`, \noption=`{option}`, \ninsex=`{insex}`\n')
        return


class MainWindow(QMainWindow):
    def __init__(self, parent=None) -> None:
        super().__init__()
        self.table_list = ["Организации", "Объекты", "Проекты", "Документы", "Вещества", "Оборудование", "Трубопроводы"]
        self.sender_list = ["Организация", "Объект", "Проект", "Документ", "Вещество", "Оборудование", "Трубопровод"]
        self.table_list_eng = ["Organizations", "Objects", "Projects", "Documents", "Substances", "Devices",
                               "Pipelines"]

        self.field_dict_in_db = {
            "Organizations": (
                'Name_org', 'Name_org_full', 'Director', 'Name_director', 'Tech_director', 'Name_tech_director',
                'Jur_adress',
                'Telephone', 'Fax', 'Email', 'License', 'Date_get_license'),
            "Objects":
                ('OrganizationId', 'Name_opo', 'Address_opo', 'Reg_number_opo', 'Class_opo'),
            "Projects":
                ('ObjectsId', 'Name_project', 'Project_code', 'Project_description', 'Project_automat'),
            "Documents":
                ('ProjectsId', 'Section_other_documentation', 'Part_other_documentation_dpb',
                 'Part_other_documentation_gochs',
                 'Book_dpb', 'Code_dpb', 'Tom_dpb', 'Book_rpz', 'Code_rpz', 'Tom_rpz', 'Book_ifl', 'Code_ifl',
                 'Tom_ifl',
                 'Book_gochs', 'Code_gochs', 'Tom_gochs', 'Section_fire_safety', 'Code_fire_safety', 'Tom_fire_safety'),
            "Substances":
                ('Name_sub', 'Density', 'Density_gas', 'Molecular_weight', 'Steam_pressure', 'Flash_temperature',
                 'Boiling_temperature', 'Class_substance', 'Heat_of_combustion', 'Sigma', 'Energy_level',
                 'Lower_concentration', 'Cost'),
            "Devices":
                ('ProjectsId', 'SubId', 'Type_device', 'Pozition', 'Name', 'Locations', 'Material', 'Ground', 'Target',
                 'Volume', 'Completion', 'Pressure', 'Temperature', 'Spill_square', 'View_space', 'Death_person',
                 'Injured_person', 'Time_person'),
            "Pipelines":
                ('ProjectsId', 'SubId', 'Pozition', 'Name', 'Locations', 'Material', 'Ground', 'Target',
                 'Length', 'Diameter', 'Pressure', 'Temperature', 'Flow', 'View_space', 'Death_person',
                 'Injured_person', 'Time_person')
        }

        self.field_dict = {
            "Organizations": (
                'Организация', 'Форма', 'Руководитель', 'Ф.И.О.', 'Тех.руководитель', 'Ф.И.О.',
                'Юр. адрес',
                'Телефон', 'Факс', 'Email', 'Лицензия', 'Дата лицензии'),
            "Objects":
                ('Организация', 'Объект', 'Адрес объекта', 'Рег. №', 'Класс'),
            "Projects":
                ('Объект', 'Проект', 'Шифр', 'Описание', 'Автоматизация'),
            "Documents":
                ('Проект', 'Раздел', 'Подраздел ДПБ',
                 'Подраздел ГОЧС',
                 'Книга ДПБ', 'Шифр ДПБ', 'Том ДПБ', 'Книга РПЗ', 'Код РПЗ', 'Том РПЗ', 'Книга ИФЛ', 'Код ИФЛ',
                 'Том ИФЛ',
                 'Книга ГОЧС', 'Код ГОЧС', 'Том ГОЧС', 'Подраздел ПБ', 'Код ПБ', 'Том ПБ'),
            "Substances":
                ('Наименование', 'po, кг /м3', 'po г.ф., кг/м3', 'M, кг/кмоль', 'Pn, кПа', 'Т.всп, гр.С',
                 'Т.кип, гр.С', 'Класс', 'Qсг, кДж/кг', 'sigma, -', 'Энергозапас, -',
                 'НКПР, % об.', 'Цена, т.р./т'),
            "Devices":
                ('Шифр', 'Вещество', 'Тип', 'Поз.', 'Наименование', 'Составляющая', 'Материал', 'Расположение',
                 'Назначение',
                 'V, м3', 'а, -', 'P, МПа', 'Т, С', 'S, м2', 'Класс, -', 'G1, чел',
                 'G2, чел', 't, ч'),
            "Pipelines":
                ('Шифр', 'Вещество', 'Поз.', 'Наименование', 'Составляющая', 'Материал', 'Расположение', 'Назначение',
                 'L, км', 'D, мм', 'P, МПа', 'Т, С', 'Q, т/сут', 'Класс, -', 'G1, чел',
                 'G2, чел', 't, ч')
        }

        self.set_ico()
        self.init_UI()

    def init_UI(self):

        self.setGeometry(500, 500, 1000, 750)
        self.setWindowTitle('Painter')
        # Центральный виджет
        central_widget = QWidget()
        # Основная сетка компановки
        central_grid = QGridLayout(self)
        central_grid.setColumnStretch(0, 7)
        central_grid.setColumnStretch(1, 1)
        # vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
        # Рамка
        layout_select = QFormLayout(self)
        GB_select = QGroupBox('Настройки')
        GB_select.setStyleSheet("QGroupBox { font-weight : bold; }")

        self.select_table = QComboBox()
        self.select_table.addItems(self.table_list)
        for count, value in enumerate(self.list_ico):
            self.select_table.setItemIcon(count, value)
        self.select_table.currentIndexChanged.connect(self.show_table)

        self.search_line_edit = QLineEdit()
        self.search_line_edit.setPlaceholderText("Поиск...")
        self.search_line_edit.setToolTip("Подсказка для поиска")
        self.search_line_edit.textChanged.connect(self.__update_filter)

        self.layer_thickness = QSpinBox()
        self.layer_thickness.setRange(5, 150)
        self.layer_thickness.setSingleStep(5)
        self.layer_thickness.setSuffix(" (1/м)")
        self.layer_thickness.setToolTip("Толщина свободного пролива")

        self.time_evaporation = QSpinBox()
        self.time_evaporation.setRange(900, 3600)
        self.time_evaporation.setSingleStep(100)
        self.time_evaporation.setSuffix(" (сек)")
        self.time_evaporation.setToolTip("Время испарения опасного вещества")

        layout_select.addRow("", self.select_table)
        layout_select.addRow("", self.search_line_edit)
        layout_select.addRow("", self.layer_thickness)
        layout_select.addRow("", self.time_evaporation)
        GB_select.setLayout(layout_select)

        # vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
        # Рамка
        layout_table = QFormLayout(self)
        GB_table = QGroupBox('Данные')
        GB_table.setStyleSheet("QGroupBox { font-weight : bold; }")
        self.table = QTableView()
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)  # адаптивный текст в таблице
        self.delegate = ReadOnlyDelegate(self.table)
        self.model = QSqlRelationalTableModel(db=db)
        self.show_table(index=0)
        layout_table.addRow("", self.table)
        GB_table.setLayout(layout_table)
        self.resize(800, 600)
        self.setWindowTitle('Safety_docs')
        self.set_ico()

        # 4. Размещение основных элементов на центральной сетке
        central_grid.addWidget(GB_table, 0, 0, 1, 1)
        central_grid.addWidget(GB_select, 0, 1, 1, 1)
        central_widget.setLayout(central_grid)
        self.setCentralWidget(central_widget)

        # vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
        # Меню (тулбар)
        # 1. Данные
        # 1.1. Добавить
        add_menu = QMenu('Добавить', self)
        add_menu.setIcon(self.add_ico)
        add_org = QAction(self.org_ico, 'Организация', self)
        add_org.triggered.connect(self.add_data_in_db)
        add_menu.addAction(add_org)
        add_object = QAction(self.object_ico, 'Объект', self)
        add_object.triggered.connect(self.add_data_in_db)
        add_menu.addAction(add_object)
        add_project = QAction(self.project_ico, 'Проект', self)
        add_project.triggered.connect(self.add_data_in_db)
        add_menu.addAction(add_project)
        add_doc = QAction(self.document_ico, 'Документ', self)
        add_doc.triggered.connect(self.add_data_in_db)
        add_menu.addAction(add_doc)
        add_sub = QAction(self.sub_ico, 'Вещество', self)
        add_sub.triggered.connect(self.add_data_in_db)
        add_menu.addAction(add_sub)
        add_device = QAction(self.device_ico, 'Оборудование', self)
        add_device.triggered.connect(self.add_data_in_db)
        add_menu.addAction(add_device)
        add_pipeline = QAction(self.pipeline_ico, 'Трубопровод', self)
        add_pipeline.triggered.connect(self.add_data_in_db)
        add_menu.addAction(add_pipeline)
        # 1.1. Удалить
        del_object = QAction(self.del_ico, 'Удалить', self)
        del_object.triggered.connect(self.del_data_in_db)
        # 2. Отчет
        # 2.1 Сводная таблица
        report_table = QAction(self.table_ico, 'Сводный отчет', self)
        report_table.triggered.connect(self.get_report_table)
        # 2.2. Документы
        doc_menu = QMenu('Разделы', self)
        doc_menu.setIcon(self.word_ico)
        doc_prom_bez = QAction(self.book_ico, 'Декларация ПБ', self)
        doc_prom_bez.triggered.connect(self.get_report_table)
        doc_menu.addAction(doc_prom_bez)
        doc_gochs = QAction(self.book_ico, 'ПМ ГОЧС', self)
        # doc_gochs.triggered.connect(self.add_data_in_db)
        doc_menu.addAction(doc_gochs)
        doc_pb = QAction(self.book_ico, 'Пожарная безопасность', self)
        # doc_pb.triggered.connect(self.add_data_in_db)
        doc_menu.addAction(doc_pb)
        # 2.3. Расчет
        calc_menu = QMenu('Расчет', self)
        calc_menu.setIcon(self.calc_ico)
        calc_fire = QAction(self.fire_ico, 'Пожар', self)
        # calc_fire.triggered.connect(self.add_data_in_db)
        calc_menu.addAction(calc_fire)
        calc_expl = QAction(self.expl_ico, 'Взрыв', self)
        # calc_expl.triggered.connect(self.add_data_in_db)
        calc_menu.addAction(calc_expl)
        calc_flash = QAction(self.flash_ico, 'Вспышка + НКПР', self)
        # calc_flash.triggered.connect(self.add_data_in_db)
        calc_menu.addAction(calc_flash)

        # Меню приложения (верхняя плашка)
        menubar = self.menuBar()
        data_menu = menubar.addMenu('Данные')
        data_menu.addMenu(add_menu)
        data_menu.addAction(del_object)
        report_menu = menubar.addMenu('Отчет')
        report_menu.addAction(report_table)
        report_menu.addMenu(doc_menu)
        report_menu.addMenu(calc_menu)
        # vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
        self.show()

    def show_table(self, index):
        # vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
        # Установка таблицы из модели
        # vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
        self.table.setModel(self.model)
        self.model.setTable(self.table_list_eng[index])
        # vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
        # Запрет редактирования столбцов
        # vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
        self.search_line_edit.setText('')
        if index in (0, 4):
            self.table.setItemDelegateForColumn(0, self.delegate)
            self.table.setItemDelegateForColumn(1, None)
            self.table.setItemDelegateForColumn(2, None)
            self.table.setItemDelegateForColumn(3, None)
        elif index in (1, 2, 3):
            self.table.setItemDelegateForColumn(0, self.delegate)
            self.table.setItemDelegateForColumn(1, self.delegate)
        elif index in (5, 6):
            self.table.setItemDelegateForColumn(0, self.delegate)
            self.table.setItemDelegateForColumn(1, self.delegate)
            self.table.setItemDelegateForColumn(2, self.delegate)
        # vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
        # Оформление заголовков таблицы
        # vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
        if index == 0:
            for i in count(1, 1):
                if i > len(self.field_dict["Organizations"]): break
                self.model.setHeaderData(i, Qt.Horizontal, self.field_dict["Organizations"][i - 1])
        if index == 1:
            self.model.setRelation(1, QSqlRelation("Organizations", "Id", "Name_org"))
            for i in count(1, 1):
                if i > len(self.field_dict["Objects"]): break
                self.model.setHeaderData(i, Qt.Horizontal, self.field_dict["Objects"][i - 1])
        if index == 2:
            self.model.setRelation(1, QSqlRelation("Objects", "Id", "Name_opo"))
            for i in count(1, 1):
                if i > len(self.field_dict["Projects"]): break
                self.model.setHeaderData(i, Qt.Horizontal, self.field_dict["Projects"][i - 1])
        if index == 3:
            self.model.setRelation(1, QSqlRelation("Projects", "Id", "Name_project"))
            for i in count(1, 1):
                if i > len(self.field_dict["Documents"]): break
                self.model.setHeaderData(i, Qt.Horizontal, self.field_dict["Documents"][i - 1])
        if index == 4:
            for i in count(1, 1):
                if i > len(self.field_dict["Substances"]): break
                self.model.setHeaderData(i, Qt.Horizontal, self.field_dict["Substances"][i - 1])
        if index == 5:
            self.model.setRelation(1, QSqlRelation("Projects", "Id", "Project_code"))
            self.model.setRelation(2, QSqlRelation("Substances", "Id", "Name_sub"))
            for i in count(1, 1):
                if i > len(self.field_dict["Devices"]): break
                self.model.setHeaderData(i, Qt.Horizontal, self.field_dict["Devices"][i - 1])
        if index == 6:
            self.model.setRelation(1, QSqlRelation("Projects", "Id", "Project_code"))
            self.model.setRelation(2, QSqlRelation("Substances", "Id", "Name_sub"))
            for i in count(1, 1):
                if i > len(self.field_dict["Pipelines"]): break
                self.model.setHeaderData(i, Qt.Horizontal, self.field_dict["Pipelines"][i - 1])

        self.model.select()

    # __________________________________________________________________________
    # vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
    # Добавление, удаление информации для базы данных и фильтрация
    # vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
    def add_data_in_db(self):
        """
        Функция предназначена для добавления данных в базу данных
        :return
        """
        # 1. Кто отправил сигнал
        sender = self.sender()
        # 2. Вызываем диалог добавления
        inputDialog = Add_Dialog(state=sender.text(), header_dict=self.field_dict)
        # 2.1. Получаем ответ от Диалога
        rez = inputDialog.exec()
        # 2.2. Если нажата кнопка Отмена
        if not rez:
            _ = QMessageBox.information(self, 'Внимание!', 'Добавление в базу данных отменено')
            return
        # 2.3. Если нажата кнопка Ок, проверим все ли данные введены
        data = self.__check_value_in_table(inputDialog.tableWidget)
        if data == []: return
        # 2.4. Смотрим в списке sender_list под каким индексом
        # стоит отправитель сигнала и сравниваем с:
        if self.sender_list.index(sender.text()) == 0:  # 0 - таблица организаций
            self.__add_record(data=data, table="Organizations", fields=self.field_dict_in_db["Organizations"])
            self.select_table.setCurrentIndex(0)
        elif self.sender_list.index(sender.text()) == 1:  # 1 - таблица объектов
            # Добавим в список id организации
            data.insert(0, int(inputDialog.id.currentText().split()[0]))
            self.select_table.setCurrentIndex(1)
            self.__add_record(data=data, table="Objects", fields=self.field_dict_in_db["Objects"])
        elif self.sender_list.index(sender.text()) == 2:  # 2 - таблица проектов
            # Добавим в список id объекта
            data.insert(0, int(inputDialog.id.currentText().split()[0]))
            self.__add_record(data=data, table="Projects", fields=self.field_dict_in_db["Projects"])
            self.select_table.setCurrentIndex(2)
        elif self.sender_list.index(sender.text()) == 3:  # 3 - таблица наименования томов
            # Добавим в список id проекта
            data.insert(0, int(inputDialog.id.currentText().split()[0]))
            self.__add_record(data=data, table="Documents", fields=self.field_dict_in_db["Documents"])
            self.select_table.setCurrentIndex(3)
        elif self.sender_list.index(sender.text()) == 4:  # 4 - вещества
            self.__add_record(data=data, table="Substances", fields=self.field_dict_in_db["Substances"])
            self.select_table.setCurrentIndex(4)
        elif self.sender_list.index(sender.text()) == 5:  # 5 - Оборудование
            # Добавим в список тип объекта
            data.insert(0, int(inputDialog.type_obj.currentText()[-1]))
            # Добавим в список id вещества
            data.insert(0, int(inputDialog.id_sub.currentText().split()[0]))
            # Добавим в список id проекта
            data.insert(0, int(inputDialog.id.currentText().split()[0]))
            self.__add_record(data=data, table="Devices", fields=self.field_dict_in_db["Devices"])
            self.select_table.setCurrentIndex(5)
        elif self.sender_list.index(sender.text()) == 6:  # 6 - Трубопроводы
            # Добавим в список id вещества
            data.insert(0, int(inputDialog.id_sub.currentText().split()[0]))
            # Добавим в список id проекта
            data.insert(0, int(inputDialog.id.currentText().split()[0]))
            self.__add_record(data=data, table="Pipelines", fields=self.field_dict_in_db["Pipelines"])
            self.select_table.setCurrentIndex(6)
        # 3. Обновляем таблицу в соответствии с индексом отправителя
        self.show_table(self.sender_list.index(sender.text()))

    def del_data_in_db(self):
        """
        Удаление данных из таблицы по наименованию таблицы и id строки
        """
        index = self.table.currentIndex()
        id = self.table.model().index(index.row(), 0).data()
        table_name = self.table_list_eng[self.select_table.currentIndex()]
        db.transaction()
        query = QSqlQuery()
        sql_request = f'DELETE FROM {table_name} WHERE Id={id}'
        query.prepare(sql_request)
        query.exec_()
        db.commit()
        self.show_table(self.select_table.currentIndex())

    # vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
    # Подфункции для add_data_in_db
    def __add_record(self, data: list, table: str, fields: tuple) -> None:
        """
        :param data - список значений из QTableWidget для вставки в базу данных
        :param table - наименование таблицы из базы данных (например: 'Organizations')
        :param fields - кортеж полей базы данных (например:
        ('Name_org', 'Name_org_full',
        'Director', 'Name_director', 'Tech_director', 'Name_tech_director',
        'Jur_adress', 'Telephone', 'Fax', 'Email', 'License', 'Date_get_license')
        )
        """

        # Данные введены целиком открываем транзакцию
        db.transaction()
        query = QSqlQuery()
        placeholder, sql_request = self.__create_insert_sql_request(table=table, fields=fields)
        query.prepare(sql_request)
        for i in range(len(data)):
            query.bindValue(placeholder[i], data[i])
        query.exec_()
        db.commit()

    def __create_insert_sql_request(self, table: str, fields: tuple):
        """
        Функция предназначена для формирования запроса на вставку в базу данных
        и заполнителей для вставки значений через PyQt5

        :param table - наименование таблицы из базы данных (например: 'Organizations')
        :param fields - кортеж полей базы данных (например:
        ('Name_org', 'Name_org_full',
        'Director', 'Name_director', 'Tech_director', 'Name_tech_director',
        'Jur_adress', 'Telephone', 'Fax', 'Email', 'License', 'Date_get_license')
        )
        :return placeholder - список заполнителей для вставки значений по именованным параметрам
        :return sql_request - строковый запрос SQL
        """
        placeholder = [f":{i}" for i in fields]
        fields = str(fields).strip("()")
        fields = fields.replace("'", "")
        sql_request = f'INSERT INTO {table} ({fields}) VALUES ({placeholder})'.replace('[', '').replace(']',
                                                                                                        '').replace("'",
                                                                                                                    "")
        return placeholder, sql_request

    def __check_value_in_table(self, table_widget) -> list:
        """
        Функция предназначена для получения данных из QTableWidget, если данные заполнены не все,
        то вернуть пустой список.

        :param table_widget - таблица QTableWidget
        :return data - список значений из QTableWidget, либо пустой список если данные заполнены не все
        """
        data = []
        for row in range(table_widget.rowCount()):
            if table_widget.item(row, 1) is not None:
                data.append(table_widget.item(row, 1).text())
            else:
                _ = QMessageBox.information(self, 'Внимание!',
                                            'Данные не заполнены. Добавление в базу данных не возможно!')
                return []
        return data

    def __update_filter(self, s):
        """
        Функция фильтрации представления модели
        :param s - подстрока поиска
        """
        name_col_for_filter = (
            'Name_org', 'Name_opo', 'Project_code', 'Name_project', 'Name_sub', 'Project_code', 'Project_code')
        filter_str = f'{name_col_for_filter[self.select_table.currentIndex()]} LIKE "%{s}%"'
        self.model.setFilter(filter_str)

    # vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
    # __________________________________________________________________________
    # __________________________________________________________________________
    # vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
    # Отчеты
    # vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
    def get_report_table(self):
        # 1. Вызываем диалог добавления
        get_report_dialog = Get_report()
        # 1.1. Получаем ответ от Диалога
        rez = get_report_dialog.exec()
        # 1.2. Если нажата кнопка Отмена
        if not rez:
            _ = QMessageBox.information(self, 'Внимание!', 'Составление сводного отчета отменено')
            return
        # 1.3 Заведем словари для информации
        project_info = {}
        object_info = {}
        org_info = {}
        doc_info = {}
        dev_info = []
        pipe_info = []
        sub_info = []
        # 2. Получим по шифру из проекта инфу из таблицы Projects
        query = QSqlQuery(
            f'SELECT * FROM Projects WHERE Project_code = "{get_report_dialog.num_project.currentText()}"')
        query.next()
        for i in range(len(self.field_dict_in_db['Projects']) + 1):
            if i == 0:
                project_info['Id'] = query.value(i)
            else:
                project_info[self.field_dict_in_db['Projects'][i - 1]] = query.value(i)
        pprint(project_info)
        query.exec_()
        # 3. Получим по id  инфу из таблицы Objects
        query = QSqlQuery(f'SELECT * FROM Objects WHERE Id = {project_info["ObjectsId"]}')
        query.next()
        for i in range(len(self.field_dict_in_db['Objects']) + 1):
            if i == 0:
                object_info['Id'] = query.value(i)
            else:
                object_info[self.field_dict_in_db['Objects'][i - 1]] = query.value(i)
        pprint(object_info)
        query.exec_()
        # 3. Получим по id  инфу из таблицы Organizations
        query = QSqlQuery(f'SELECT * FROM Organizations WHERE Id = {object_info["OrganizationId"]}')
        query.next()
        for i in range(len(self.field_dict_in_db['Organizations']) + 1):
            if i == 0:
                org_info['Id'] = query.value(i)
            else:
                org_info[self.field_dict_in_db['Organizations'][i - 1]] = query.value(i)
        pprint(org_info)
        query.exec_()
        # 4. Получим по id  инфу из таблицы Documents
        query = QSqlQuery(f'SELECT * FROM Documents WHERE ProjectsId = {project_info["Id"]}')
        query.next()
        for i in range(len(self.field_dict_in_db['Documents']) + 1):
            if i == 0:
                doc_info['Id'] = query.value(i)
            else:
                doc_info[self.field_dict_in_db['Documents'][i - 1]] = query.value(i)
        pprint(doc_info)
        query.exec_()
        # 5. Получим по id  инфу из таблицы Devices
        query = QSqlQuery(f'SELECT * FROM Devices WHERE ProjectsId = {project_info["Id"]}')
        while query.next():
            dict_dev = {}
            for i in range(len(self.field_dict_in_db['Devices']) + 1):
                if i == 0:
                    dict_dev['Id'] = query.value(i)
                else:
                    dict_dev[self.field_dict_in_db['Devices'][i - 1]] = query.value(i)
            dev_info.append(dict_dev)
        pprint(dev_info)
        query.exec_()
        # 6. Получим по id  инфу из таблицы Pipelines
        query = QSqlQuery(f'SELECT * FROM Pipelines WHERE ProjectsId = {project_info["Id"]}')
        while query.next():
            dict_pipe = {}
            for i in range(len(self.field_dict_in_db['Pipelines']) + 1):
                if i == 0:
                    dict_pipe['Id'] = query.value(i)
                else:
                    dict_pipe[self.field_dict_in_db['Pipelines'][i - 1]] = query.value(i)
            pipe_info.append(dict_pipe)
        pprint(pipe_info)
        # 6. Получим все вещества
        query = QSqlQuery(f'SELECT * FROM Substances')
        while query.next():
            dict_sub = {}
            for i in range(len(self.field_dict_in_db['Substances']) + 1):
                if i == 0:
                    dict_sub['Id'] = query.value(i)
                else:
                    dict_sub[self.field_dict_in_db['Substances'][i - 1]] = query.value(i)
            sub_info.append(dict_sub)
        pprint(sub_info)
        query.exec_()
        #  Отчеты по таблицам
        sender = self.sender()
        if sender.text() == 'Сводный отчет':

            report_word_rtn.TIME_EVAPORATION = self.time_evaporation.value()
            report_word_rtn.LAYER_THICKNESS = self.layer_thickness.value()
            report_word_rtn.Report(project_info, object_info, org_info, doc_info, dev_info, pipe_info,
                                   sub_info, sender_call=0).all_table()

            report_word.TIME_EVAPORATION = self.time_evaporation.value()
            report_word.LAYER_THICKNESS = self.layer_thickness.value()
            report_word.Report(project_info, object_info, org_info, doc_info, dev_info, pipe_info, sub_info,
                               sender_call=0).all_table()
        elif sender.text() == 'Декларация ПБ':
            report_word_rtn.TIME_EVAPORATION = self.time_evaporation.value()
            report_word_rtn.LAYER_THICKNESS = self.layer_thickness.value()
            report_word_rtn.Report(project_info, object_info, org_info, doc_info, dev_info, pipe_info,
                                   sub_info, sender_call=1).all_table()

    def set_ico(self):
        path_ico = str(Path(os.getcwd()))
        self.main_ico = QIcon(path_ico + '/ico/main.png')
        self.add_ico = QIcon(path_ico + '/ico/plus.png')
        self.del_ico = QIcon(path_ico + '/ico/minus.png')
        self.ok_ico = QIcon(path_ico + '/ico/ok.png')
        self.org_ico = QIcon(path_ico + '/ico/org.png')
        self.object_ico = QIcon(path_ico + '/ico/object.png')
        self.project_ico = QIcon(path_ico + '/ico/project.png')
        self.document_ico = QIcon(path_ico + '/ico/document.png')
        self.sub_ico = QIcon(path_ico + '/ico/sub.png')
        self.device_ico = QIcon(path_ico + '/ico/device.png')
        self.pipeline_ico = QIcon(path_ico + '/ico/pipeline.png')
        self.table_ico = QIcon(path_ico + '/ico/table.png')
        self.fire_ico = QIcon(path_ico + '/ico/fire.png')
        self.calc_ico = QIcon(path_ico + '/ico/calc.png')
        self.expl_ico = QIcon(path_ico + '/ico/explosion.png')
        self.flash_ico = QIcon(path_ico + '/ico/flash.png')
        self.word_ico = QIcon(path_ico + '/ico/word.png')
        self.book_ico = QIcon(path_ico + '/ico/book.png')
        self.setWindowIcon(self.main_ico)
        self.list_ico = [self.org_ico, self.object_ico, self.project_ico, self.document_ico, self.sub_ico,
                         self.device_ico, self.pipeline_ico]

    def closeEvent(self, event):
        reply = QMessageBox.question \
            (self, 'Выход из программы',
             "Вы уверены, что хотите уйти?",
             QMessageBox.Yes,
             QMessageBox.No)
        if reply == QMessageBox.Yes:
            db.close()
            event.accept()
        else:
            event.ignore()


class Get_report(QDialog):
    def __init__(self, ):
        super().__init__()
        # 1. Какие проекты сейчас в БД (id + шифр)
        number_project = []
        query = QSqlQuery('SELECT * FROM Projects')
        while query.next():
            number_project.append(query.value(3))
        query.exec_()
        number_project = sorted(number_project)
        # 2. Иконки
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)  # убрать знак вопроса
        path_ico = str(Path(os.getcwd()))
        main_ico = QIcon(path_ico + '/ico/main.png')
        self.setWindowIcon(main_ico)
        self.setWindowTitle('Сводный отчет')
        # 3. Основной слой диалога
        main_layout = QVBoxLayout(self)
        label = QLabel()
        label.setText('Выберете шифр проекта:')
        self.num_project = QComboBox()
        self.num_project.addItems(number_project)
        main_layout.addWidget(label)
        main_layout.addWidget(self.num_project)
        # Группа кнопок Ок-Cancel
        button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        main_layout.addWidget(button_box)


class Add_Dialog(QDialog):
    def __init__(self, state: str, header_dict: dict):
        super().__init__()
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)  # убрать знак вопроса

        path_ico = str(Path(os.getcwd()))
        main_ico = QIcon(path_ico + '/ico/main.png')
        self.setWindowIcon(main_ico)

        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(2)
        main_layout = QVBoxLayout(self)

        if state in ('Организация', 'Вещество'):
            i = ('Организация', 'Вещество').index(state)
            name_table = ('Organizations', 'Substances')
            self.setWindowTitle('Добавление организации')
            row_count = len(header_dict[name_table[i]])
            self.tableWidget.setRowCount(row_count)
            for j in range(row_count):
                self.tableWidget.setItem(j, 0, QTableWidgetItem(header_dict[name_table[i]][j]))
            main_layout.addWidget(self.tableWidget)

        if state in ('Объект', 'Проект', 'Документ'):
            i = ('Объект', 'Проект', 'Документ').index(state)
            name_table = ('Objects', 'Projects', 'Documents')
            self.setWindowTitle(f'Добавление "{state}"')
            row_count = len(header_dict[name_table[i]]) - 1
            self.tableWidget.setRowCount(row_count)
            # заполним комбобокс
            list_ = self.fill_combobox(state)
            self.id = QComboBox()
            self.id.addItems(list_)
            # таблица с данными
            for j in range(row_count):
                self.tableWidget.setItem(j, 0, QTableWidgetItem(header_dict[name_table[i]][j + 1]))
            main_layout.addWidget(self.id)
            main_layout.addWidget(self.tableWidget)

        if state in ('Оборудование',):
            i = ('Оборудование',).index(state)
            name_table = ('Devices',)
            self.setWindowTitle(f'Добавление "{state}"')
            row_count = len(header_dict[name_table[i]]) - 3
            self.tableWidget.setRowCount(row_count)
            # заполним комбобокс с проектами
            list_ = self.fill_combobox(state)
            self.id = QComboBox()
            self.id.addItems(list_)
            # заполним комбобокс с веществами
            list_sub = self.fill_combobox('Вещество')
            self.id_sub = QComboBox()
            self.id_sub.addItems(list_sub)
            # заполним комбобокс с типами объектов
            self.type_obj = QComboBox()
            self.type_obj.addItems(["Тип 0", "Тип 1"])
            # таблица с данными
            for j in range(row_count):
                self.tableWidget.setItem(j, 0, QTableWidgetItem(header_dict[name_table[i]][j + 3]))
            main_layout.addWidget(self.id)
            main_layout.addWidget(self.id_sub)
            main_layout.addWidget(self.type_obj)
            main_layout.addWidget(self.tableWidget)

        if state in ('Трубопровод',):
            i = ('Трубопровод',).index(state)
            name_table = ('Pipelines',)
            self.setWindowTitle(f'Добавление "{state}"')
            row_count = len(header_dict[name_table[i]]) - 2
            self.tableWidget.setRowCount(row_count)
            # заполним комбобокс с проектами
            list_ = self.fill_combobox(state)
            self.id = QComboBox()
            self.id.addItems(list_)
            # заполним комбобокс с веществами
            list_sub = self.fill_combobox('Вещество')
            self.id_sub = QComboBox()
            self.id_sub.addItems(list_sub)
            # таблица с данными
            for j in range(row_count):
                self.tableWidget.setItem(j, 0, QTableWidgetItem(header_dict[name_table[i]][j + 2]))
            main_layout.addWidget(self.id)
            main_layout.addWidget(self.id_sub)
            main_layout.addWidget(self.tableWidget)

        # Группа кнопок Ок-Cancel
        button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        main_layout.addWidget(button_box)

    def fill_combobox(self, state):
        list_name = []
        if state == 'Объект':
            query = QSqlQuery('SELECT * FROM Organizations')
            while query.next():
                list_name.append(str(query.value(0)) + " " + query.value(1))
            query.exec_()
        if state == 'Проект':
            query = QSqlQuery('SELECT * FROM Objects')
            while query.next():
                list_name.append(str(query.value(0)) + " " + query.value(2) + " " + query.value(4))
            query.exec_()
        if state in ('Документ', 'Оборудование', 'Трубопровод'):
            query = QSqlQuery('SELECT * FROM Projects')
            while query.next():
                list_name.append(str(query.value(0)) + " " + query.value(3) + " " + query.value(2))
            query.exec_()
        if state == 'Вещество':
            query = QSqlQuery('SELECT * FROM Substances')
            while query.next():
                list_name.append(str(query.value(0)) + " " + query.value(1))
            query.exec_()
        return list_name


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('Fusion'))
    window = MainWindow()
    app.exec_()
