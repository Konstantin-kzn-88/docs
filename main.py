from PySide2 import QtWidgets, QtGui, QtCore, QtSql
import mysql.connector as mysql
import os
import sys
from pathlib import Path

# db = QtSql.QSqlDatabase("QMYSQL/MARIADB")
db = mysql.connect(
    host='45.142.36.191',
    user='root',
    password='',
    database = 'docs_db'
)

class Painter(QtWidgets.QMainWindow):

    def __init__(self, parent=None) -> None:
        super().__init__()
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        # Иконки
        path_ico = str(Path(os.getcwd()))

        self.main_ico = QtGui.QIcon(path_ico + '/ico/main.png')

        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

        # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        # Главное окно
        self.setGeometry(500, 500, 950, 750)
        self.setWindowTitle('Safety_report')
        self.setWindowIcon(self.main_ico)
        # Центральный виджет
        central_widget = QtWidgets.QWidget()
        central_grid = QtWidgets.QGridLayout(self)
        central_grid.setRowStretch(0, 3)
        central_grid.setRowStretch(1, 1)
        central_grid.setRowStretch(2, 6)
        # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        # 1. Организации
        # Рамка
        layout_organization = QtWidgets.QFormLayout(self)
        GB_organization = QtWidgets.QGroupBox('Организации')
        GB_organization.setStyleSheet("QGroupBox { font-weight : bold; }")
        # создаем сцену  #создаем сцену и плосы прокрутки картинки
        self.table_organization = QtWidgets.QTableView()
        self.model = QtSql.QSqlRelationalTableModel(db=db)
        self.table.setModel(self.model)
        self.model.setTable("objects")
        self.model.select()
        layout_organization.addRow("", self.table_organization)
        GB_organization.setLayout(layout_organization)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        # 2. Панель набора действий
        # т.к. данных  много создадим вкладки табов
        tabs = QtWidgets.QTabWidget()  # создаем набор вкладок табов
        # 2.1 Главная вкладка (масштаб, измерения, выбор генплана, состояние подключения к БД)
        tab_main = QtWidgets.QWidget()
        # 2.2. Зоны поражения
        tab_draw = QtWidgets.QWidget()
        # 2.3. Ситуационные планы
        tab_report = QtWidgets.QWidget()
        # 2.4. Настройки
        tab_settings = QtWidgets.QWidget()
        # добавляем к п.2.1. на главную вкладку
        tabs.addTab(tab_main, "")
        # tabs.setTabIcon(0, project_ico)
        tabs.setTabToolTip(0, "Основные действия")
        tab_main.layout = QtWidgets.QFormLayout(self)
        # добавляем к п.2.2. на вкладку зон поражения
        tabs.addTab(tab_draw, "")  # 2. Зоны поражения
        # tabs.setTabIcon(1, paint_ico)
        tabs.setTabToolTip(1, "Зоны поражения")
        tab_draw.layout = QtWidgets.QFormLayout(self)
        # добавляем к п.2.3. на вкладку ситуационных планов
        tabs.addTab(tab_report, "")  # 3. Отчет
        # tabs.setTabIcon(2, word_ico)
        tabs.setTabToolTip(2, "Отчет")
        tab_report.layout = QtWidgets.QFormLayout(self)
        # добавляем к п.2.4. на вкладку ситуационных планов
        tabs.addTab(tab_settings, "")  # 3. Ситуационные планы
        # tabs.setTabIcon(3, settings_ico)
        tabs.setTabToolTip(3, "Настройки")
        tab_settings.layout = QtWidgets.QFormLayout(self)
        # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        # 2.1.1. Рамка №1. Главной вкладки. Маштаб  (то что будет в рамке 1)
        self.scale_plan = QtWidgets.QLineEdit()
        self.scale_plan.setPlaceholderText("Масштаб")
        self.scale_plan.setToolTip("В одном пикселе метров")
        self.scale_plan.setReadOnly(True)
        # Упаковываем все в QGroupBox
        # Рамка №1
        layout_scale = QtWidgets.QFormLayout(self)
        GB_scale = QtWidgets.QGroupBox('Масштаб')
        GB_scale.setStyleSheet("QGroupBox { font-weight : bold; }")
        layout_scale.addRow("", self.scale_plan)
        GB_scale.setLayout(layout_scale)

        # 2.1.2. Рамка №2. Главной вкладки. Действия (масштаб, расстояние, площадь)  (то что будет в рамке 2)
        self.type_act = QtWidgets.QComboBox()  # тип действия
        self.type_act.addItems(["Масштаб", "Расстояние", "Площадь"])

        # self.type_act.activated[str].connect(self.select_type_act)
        self.result_type_act = QtWidgets.QLabel()  # для вывода результата применения type_act + draw_type_act
        self.draw_type_act = QtWidgets.QPushButton("Применить")
        # self.draw_type_act.clicked.connect(self.change_draw_type_act)
        self.draw_type_act.setCheckable(True)
        self.draw_type_act.setChecked(False)

        # Упаковываем все в QGroupBox
        # Рамка №2
        layout_act = QtWidgets.QFormLayout(self)
        GB_act = QtWidgets.QGroupBox('Действие')
        GB_act.setStyleSheet("QGroupBox { font-weight : bold; }")
        layout_act.addRow("", self.type_act)
        layout_act.addRow("", self.draw_type_act)
        layout_act.addRow("", self.result_type_act)
        GB_act.setLayout(layout_act)

        # 2.1.3. Рамка №3. Главной вкладки. Ситуацилнные планы. (то что будет в рамке 3)
        self.plan_list = QtWidgets.QComboBox()  # ген.планы объекта
        self.plan_list.addItems(["--Нет ген.планов--"])
        self.plan_list.setToolTip("""Ген.планы объекта""")
        # self.plan_list.activated[str].connect(self.plan_list_select)
        self.data_base_info_connect = QtWidgets.QLabel()  # информация о подключении базы данных
        self.data_base_info_connect.setText('Нет подключения к базе данных...')
        self.data_base_info_connect.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))
        self.data_base_info_connect.setStyleSheet('color: red')

        # Упаковываем все в QGroupBox
        # Рамка №2
        layout_plan = QtWidgets.QFormLayout(self)
        GB_plan = QtWidgets.QGroupBox('Выбор ген.плана')
        GB_plan.setStyleSheet("QGroupBox { font-weight : bold; }")
        layout_plan.addRow("", self.plan_list)
        layout_plan.addRow("", self.data_base_info_connect)
        GB_plan.setLayout(layout_plan)

        # Собираем рамки №№ 1-3
        tab_main.layout.addWidget(GB_scale)
        tab_main.layout.addWidget(GB_act)
        tab_main.layout.addWidget(GB_plan)
        # Размещаем на табе рамки №№ 1-2
        tab_main.setLayout(tab_main.layout)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        # 2.2.1. Рамка №1. Владки зон поражения. (то что будет в рамке 1)
        # color_zone набор кнопок для зон 6 возможных зон поражения
        self.color_zone1_btn = QtWidgets.QPushButton("Зона 1")
        # self.color_zone1_btn.setIcon(color_ico)
        self.color_zone1_btn.setToolTip("Цвет зоны 1")
        self.color_zone1_btn.setStyleSheet("background-color: red")
        # self.color_zone1_btn.clicked.connect(self.select_color)
        self.color_zone2_btn = QtWidgets.QPushButton("Зона 2")
        # self.color_zone2_btn.setIcon(color_ico)
        self.color_zone2_btn.setToolTip("Цвет зоны 2")
        self.color_zone2_btn.setStyleSheet("background-color: blue")
        # self.color_zone2_btn.clicked.connect(self.select_color)
        self.color_zone3_btn = QtWidgets.QPushButton("Зона 3")
        # self.color_zone3_btn.setIcon(color_ico)
        self.color_zone3_btn.setToolTip("Цвет зоны 3")
        self.color_zone3_btn.setStyleSheet("background-color: orange")
        # self.color_zone3_btn.clicked.connect(self.select_color)
        self.color_zone4_btn = QtWidgets.QPushButton("Зона 4")
        # self.color_zone4_btn.setIcon(color_ico)
        self.color_zone4_btn.setToolTip("Цвет зоны 4")
        self.color_zone4_btn.setStyleSheet("background-color: green")
        # self.color_zone4_btn.clicked.connect(self.select_color)
        self.color_zone5_btn = QtWidgets.QPushButton("Зона 5")
        # self.color_zone5_btn.setIcon(color_ico)
        self.color_zone5_btn.setToolTip("Цвет зоны 5")
        self.color_zone5_btn.setStyleSheet("background-color: magenta")
        # self.color_zone5_btn.clicked.connect(self.select_color)
        self.color_zone6_btn = QtWidgets.QPushButton("Зона 6")
        # self.color_zone6_btn.setIcon(color_ico)
        self.color_zone6_btn.setToolTip("Цвет зоны 6")
        self.color_zone6_btn.setStyleSheet("background-color: yellow")
        # self.color_zone6_btn.clicked.connect(self.select_color)

        # 2.2.2. Рамка №2. Владки зон поражения. (то что будет в рамке 2)
        self.data_excel = QtWidgets.QLineEdit()
        self.data_excel.setPlaceholderText("Данные из Excel")
        self.data_excel.setToolTip("Данные из Excel")
        self.data_excel.setReadOnly(True)

        self.get_data_btn = QtWidgets.QPushButton("Загрузить")
        # self.get_data_btn.setIcon(excel_ico)
        self.get_data_btn.setToolTip("Загрузить выделенный диапазон")
        # self.get_data_btn.clicked.connect(self.get_data_excel)

        self.draw_from_excel = QtWidgets.QPushButton("Рисовать")
        # self.draw_from_excel.setIcon(paint_ico)
        self.draw_from_excel.setToolTip("Отрисовка зон из Excel")
        # self.draw_from_excel.clicked.connect(lambda: self.draw_from_data([] if self.data_excel.text() == ''
        #                                                                  else eval(self.data_excel.text()),
        #                                                                  fill_thickness=self.fill_thickness.value()))

        # 2.2.3. Рамка №3. Владки зон поражения. (то что будет в рамке 3)
        self.opacity = QtWidgets.QDoubleSpinBox()
        self.opacity.setDecimals(1)
        self.opacity.setRange(0, 1)
        self.opacity.setSingleStep(0.1)
        self.opacity.setValue(0.5)

        # Упаковываем все на вкладку таба "1" (делаем все в QGroupBox)
        # Рамка №1
        layout_zone = QtWidgets.QFormLayout(self)
        GB_zone = QtWidgets.QGroupBox('Выбор цвета')
        GB_zone.setStyleSheet("QGroupBox { font-weight : bold; }")
        hbox_zone_1_2 = QtWidgets.QHBoxLayout()
        hbox_zone_1_2.addWidget(self.color_zone1_btn)
        hbox_zone_1_2.addWidget(self.color_zone2_btn)
        layout_zone.addRow("", hbox_zone_1_2)
        hbox_zone_3_4 = QtWidgets.QHBoxLayout()
        hbox_zone_3_4.addWidget(self.color_zone3_btn)
        hbox_zone_3_4.addWidget(self.color_zone4_btn)
        layout_zone.addRow("", hbox_zone_3_4)
        hbox_zone_5_6 = QtWidgets.QHBoxLayout()
        hbox_zone_5_6.addWidget(self.color_zone5_btn)
        hbox_zone_5_6.addWidget(self.color_zone6_btn)
        layout_zone.addRow("", hbox_zone_5_6)
        GB_zone.setLayout(layout_zone)
        # Рамка №2
        layout_xl = QtWidgets.QFormLayout(self)
        GB_xl = QtWidgets.QGroupBox('Данные из Excel')
        GB_xl.setStyleSheet("QGroupBox { font-weight : bold; }")
        layout_xl.addRow("", self.data_excel)
        hbox_xl_draw = QtWidgets.QHBoxLayout()
        hbox_xl_draw.addWidget(self.get_data_btn)
        hbox_xl_draw.addWidget(self.draw_from_excel)
        layout_xl.addRow("", hbox_xl_draw)
        GB_xl.setLayout(layout_xl)
        # Рамка №3
        layout_opacity = QtWidgets.QFormLayout(self)
        GB_opacity = QtWidgets.QGroupBox('Прозрачность')
        GB_opacity.setStyleSheet("QGroupBox { font-weight : bold; }")
        layout_opacity.addRow("", self.opacity)
        GB_opacity.setLayout(layout_opacity)

        # Собираем рамки №№ 1-3
        tab_draw.layout.addWidget(GB_zone)
        tab_draw.layout.addWidget(GB_xl)
        tab_draw.layout.addWidget(GB_opacity)
        # Размещаем на табе
        tab_draw.setLayout(tab_draw.layout)
        # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


        # 2.3.2. Рамка №2. Вкладка отчетов. Тип документа  (то что будет в рамке 2)
        self.type_doc = QtWidgets.QComboBox()  # тип документа
        self.type_doc.addItems(["ДПБ", "ПМ ГОЧС"])

        self.doc_report = QtWidgets.QPushButton("Сохранить")
        # self.doc_report.setIcon(download_ico)
        # self.doc_report.clicked.connect(self.report_word)

        # Упаковываем все в QGroupBox
        # Рамка №2
        layout_doc = QtWidgets.QFormLayout(self)
        GB_doc = QtWidgets.QGroupBox('Выбор документа')
        GB_doc.setStyleSheet("QGroupBox { font-weight : bold; }")
        hbox_doc = QtWidgets.QHBoxLayout()
        hbox_doc.addWidget(self.type_doc)
        hbox_doc.addWidget(self.doc_report)
        layout_doc.addRow("", hbox_doc)
        GB_doc.setLayout(layout_doc)

        # 2.3.3. Рамка №3. Вкладка отчетов. Тип плана  (то что будет в рамке 3)
        self.plan_report_type = QtWidgets.QComboBox()  # тип плана
        self.plan_report_type.addItems(["Взрыв", "Пожар", "Вспышка", "НКПР", "Риск"])

        # # self.type_act.activated[str].connect(self.select_type_act)
        self.plan_report = QtWidgets.QPushButton("Нарисовать")
        # self.plan_report.setIcon(show_ico)
        # self.plan_report.clicked.connect(self.plan_report_draw)

        # Упаковываем все в QGroupBox
        # Рамка №2
        layout_get_plan = QtWidgets.QFormLayout(self)
        GB_get_plan = QtWidgets.QGroupBox('Ситуационный план')
        GB_get_plan.setStyleSheet("QGroupBox { font-weight : bold; }")
        hbox_get_plan = QtWidgets.QHBoxLayout()
        hbox_get_plan.addWidget(self.plan_report_type)
        hbox_get_plan.addWidget(self.plan_report)
        layout_get_plan.addRow("", hbox_get_plan)
        GB_get_plan.setLayout(layout_get_plan)

        # Собираем рамки №№ 1-3

        tab_report.layout.addWidget(GB_doc)
        tab_report.layout.addWidget(GB_get_plan)
        # Размещаем на табе рамки №№ 1-2
        tab_report.setLayout(tab_report.layout)
        # # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        # 2.4.1. Рамка №1. Толщина линий объектов   (то что будет в рамке 1)
        self.thickness_line = QtWidgets.QSpinBox()
        self.thickness_line.setRange(1, 10)
        self.thickness_line.setSingleStep(1)
        self.thickness_line.setValue(2)
        self.thickness_line.setToolTip("Толщина линий объектов")

        self.fill_thickness = QtWidgets.QSpinBox()
        self.fill_thickness.setRange(0, 30)
        self.fill_thickness.setSingleStep(1)
        self.fill_thickness.setValue(10)
        self.fill_thickness.setToolTip("Толщина изолиний зон поражающего фактора")

        # 2.4.2. Рамка №2. Подробность расчета риска   (то что будет в рамке 2)
        self.sharpness = QtWidgets.QSpinBox()
        self.sharpness.setRange(1, 10)
        self.sharpness.setSingleStep(1)
        self.sharpness.setValue(5)

        # 2.4.3. Рамка №3. Время истечения   (то что будет в рамке 3)
        self.shutdown_time = QtWidgets.QSpinBox()
        self.shutdown_time.setToolTip("Время отключения трубопроводов в секундах")
        self.shutdown_time.setRange(0, 600)
        self.shutdown_time.setSingleStep(1)
        self.shutdown_time.setValue(0)

        #
        # # Упаковываем все в QGroupBox
        # # Рамка №1
        layout_set = QtWidgets.QFormLayout(self)
        GB_set = QtWidgets.QGroupBox('Толщина линий')
        GB_set.setStyleSheet("QGroupBox { font-weight : bold; }")
        hbox_fill = QtWidgets.QHBoxLayout()
        hbox_fill.addWidget(self.thickness_line)
        hbox_fill.addWidget(self.fill_thickness)
        layout_set.addRow("", hbox_fill)
        layout_set.addRow("", hbox_fill)
        GB_set.setLayout(layout_set)

        # # Рамка №2
        layout_sharpness = QtWidgets.QFormLayout(self)
        GB_sharpness = QtWidgets.QGroupBox('Сетка расчета риска')
        GB_sharpness.setStyleSheet("QGroupBox { font-weight : bold; }")
        layout_sharpness.addRow("", self.sharpness)
        GB_sharpness.setLayout(layout_sharpness)

        # # Рамка №2
        layout_shutdown = QtWidgets.QFormLayout(self)
        GB_shutdown = QtWidgets.QGroupBox('Время отключения, сек.')
        GB_shutdown.setStyleSheet("QGroupBox { font-weight : bold; }")
        layout_shutdown.addRow("", self.shutdown_time)
        GB_shutdown.setLayout(layout_shutdown)

        # Собираем рамки №№ 1
        tab_settings.layout.addWidget(GB_set)
        tab_settings.layout.addWidget(GB_sharpness)
        tab_settings.layout.addWidget(GB_shutdown)

        # Размещаем на табе рамки №№ 1
        tab_settings.setLayout(tab_settings.layout)
        # # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        # 3. Таблица для ввода данных

        # Рамка
        layout_data = QtWidgets.QFormLayout(self)
        GB_data = QtWidgets.QGroupBox('Данные об объекте')
        GB_data.setStyleSheet("QGroupBox { font-weight : bold; }")

        # таблица
        data_grid = QtWidgets.QGridLayout(self)
        data_grid.setColumnStretch(0, 15)
        data_grid.setColumnStretch(1, 1)

        self.table_data = QtWidgets.QTableWidget(0, 33)
        # self.table_data_view()  # фукция отрисовки заголовков таблицы
        # self.table_data.clicked[QtCore.QModelIndex].connect(self.get_index_in_table)
        # кнопки управления
        layout_control = QtWidgets.QFormLayout(self)
        GB_control = QtWidgets.QGroupBox('Действия объекта')

        self.add_row = QtWidgets.QPushButton("Добавить объект")
        self.add_row.setStyleSheet("text-align: left;")
        # self.add_row.setIcon(plus_ico)
        self.add_row.setToolTip("Добавить строку в таблицу")
        # self.add_row.clicked.connect(self.add_in_table)

        self.del_row = QtWidgets.QPushButton("Удалить объект")
        self.del_row.setStyleSheet("text-align: left;")
        # self.del_row.setIcon(minus_ico)
        self.del_row.setToolTip("Удалить строку из таблицу")
        # self.del_row.clicked.connect(self.del_in_table)

        self.example_obj = QtWidgets.QPushButton("Пример объекта")
        self.example_obj.setStyleSheet("text-align: left;")
        # self.example_obj.setIcon(book_ico)
        self.example_obj.setToolTip("Добавить примерный объект")
        # self.example_obj.clicked.connect(self.add_example_obj)

        self.draw_obj = QtWidgets.QPushButton("Координаты")
        self.draw_obj.setStyleSheet("text-align: left;")
        self.draw_obj.setToolTip('Указать координаты выбранного в таблице объекта')
        # self.draw_obj.setIcon(object_ico)
        # self.draw_obj.clicked.connect(self.change_draw_obj)
        self.draw_obj.setCheckable(True)
        self.draw_obj.setChecked(False)

        self.del_last_coordinate = QtWidgets.QPushButton("")
        self.del_last_coordinate.setToolTip('Удалить последнюю координату')
        # self.del_last_coordinate.setIcon(minus_ico)
        # self.del_last_coordinate.clicked.connect(self.delete_last_coordinate)

        self.del_all_coordinate = QtWidgets.QPushButton("")
        self.del_all_coordinate.setToolTip('Удалить все координаты')
        # self.del_all_coordinate.setIcon(dbl_minus_ico)
        # self.del_all_coordinate.clicked.connect(self.delete_all_coordinates)

        self.save_table = QtWidgets.QPushButton("Сохранить объекты")
        self.save_table.setToolTip('Сохранить объекты в базу данных')
        # self.save_table.setIcon(save_ico)
        # self.save_table.clicked.connect(self.save_table_in_db)

        layout_control.addRow("", self.add_row)
        layout_control.addRow("", self.del_row)
        layout_control.addRow("", self.example_obj)
        layout_control.addRow("", self.draw_obj)
        hbox_coordinate = QtWidgets.QHBoxLayout()
        hbox_coordinate.addWidget(self.del_last_coordinate)
        hbox_coordinate.addWidget(self.del_all_coordinate)
        layout_control.addRow("", hbox_coordinate)
        layout_control.addRow("", self.save_table)
        GB_control.setLayout(layout_control)

        data_grid.addWidget(self.table_data, 0, 0, 1, 1)
        data_grid.addWidget(GB_control, 0, 1, 1, 1)
        layout_data.addRow("", data_grid)
        GB_data.setLayout(layout_data)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        # 4. Размещение основных элементов на центральной сетке
        central_grid.addWidget(GB_organization, 0, 0, 1, 0)
        central_grid.addWidget(tabs, 1, 0, 1, 1)
        central_grid.addWidget(GB_data, 1, 1, 1, 1)
        central_widget.setLayout(central_grid)
        self.setCentralWidget(central_widget)
        # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        # 5. Меню (тулбар)
        # # База данных (меню)
        # db_menu = QtWidgets.QMenu('База данных', self)
        # # db_create = QtWidgets.QAction(ok_ico, 'Создать', self)
        # # db_create.setStatusTip('Создать новую базу данных')
        # # db_create.triggered.connect(self.db_create)
        # # db_menu.addAction(db_create)
        # # db_connect = QtWidgets.QAction(db_ico, 'Подключиться', self)
        # # db_connect.setStatusTip('Подключиться к существующей базе данных')
        # # db_connect.triggered.connect(self.db_connect)
        # # db_menu.addAction(db_connect)
        #
        # # Генплан (меню)
        # plan_menu = QtWidgets.QMenu('Ген.план', self)
        # plan_add = QtWidgets.QAction(ok_ico, 'Добавить', self)
        # plan_add.setStatusTip('Добавить новый план объекта')
        # # plan_add.triggered.connect(self.plan_add_func)
        # plan_menu.addAction(plan_add)
        # plan_replace = QtWidgets.QAction(replace_ico, 'Заменить', self)
        # plan_replace.setStatusTip('Заменить план объекта')
        # # plan_replace.triggered.connect(self.plan_replace)
        # plan_menu.addAction(plan_replace)
        # plan_save = QtWidgets.QAction(save_ico, 'Coхранить', self)
        # plan_save.setStatusTip('Сохранить текущее изображение плана объекта как файл')
        # # plan_save.triggered.connect(self.plan_save)
        # plan_menu.addAction(plan_save)
        # plan_clear = QtWidgets.QAction(clear_ico, 'Очистить', self)
        # plan_clear.setStatusTip('Очистить план объекта')
        # # plan_clear.triggered.connect(self.plan_clear)
        # plan_menu.addAction(plan_clear)
        # plan_del = QtWidgets.QAction(del_ico, 'Удалить план с объектами', self)
        # plan_del.setStatusTip('Удалить изображение плана объекта')
        # # plan_del.triggered.connect(self.plan_del)
        # plan_menu.addAction(plan_del)
        #
        # # Выход из приложения
        # exit_prog = QtWidgets.QAction(exit_ico, 'Выход', self)
        # exit_prog.setShortcut('Ctrl+Q')
        # exit_prog.setStatusTip('Выход из Painter')
        # # exit_prog.triggered.connect(self.close_event)
        #
        # # Вид +/- и "рука"
        # scale_plus = QtWidgets.QAction(plus_ico, 'Увеличить план', self)
        # scale_plus.setShortcut('Ctrl+P')
        # scale_plus.setStatusTip('Увеличить план')
        # # scale_plus.triggered.connect(self.scale_view_plus)
        #
        # scale_min = QtWidgets.QAction(minus_ico, 'Уменьшить план', self)
        # scale_min.setShortcut('Ctrl+M')
        # scale_min.setStatusTip('Уменьшить план')
        # # scale_min.triggered.connect(self.scale_view_min)
        #
        # hand_act = QtWidgets.QAction(hand_ico, 'Рука', self)
        # hand_act.setShortcut('Ctrl+H')
        # hand_act.setStatusTip('Рука')
        # # hand_act.triggered.connect(self.plan_hand)
        #
        # # Справка
        # help_show = QtWidgets.QAction(question_ico, 'Справка', self)
        # help_show.setShortcut('F1')
        # help_show.setStatusTip('Открыть справку Painter')
        # # help_show.triggered.connect(self.help_show)
        #
        # # О приложении
        # about_prog = QtWidgets.QAction(info_ico, 'О приложении', self)
        # about_prog.setShortcut('F2')
        # about_prog.setStatusTip('О приложении Painter')
        # # about_prog.triggered.connect(self.about_programm)
        #
        # # Меню приложения (верхняя плашка)
        # menubar = self.menuBar()
        # file_menu = menubar.addMenu('Файл')
        # file_menu.addMenu(db_menu)
        # file_menu.addMenu(plan_menu)
        # file_menu.addAction(exit_prog)
        # view_menu = menubar.addMenu('Вид')
        # view_menu.addAction(scale_plus)
        # view_menu.addAction(scale_min)
        # view_menu.addAction(hand_act)
        # help_menu = menubar.addMenu('Справка')
        # help_menu.addAction(help_show)
        # help_menu.addAction(about_prog)
        # # Установить статусбар
        # self.statusBar()
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        if not parent:
            self.show()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle(QtWidgets.QStyleFactory.create('Fusion'))
    ex = Painter()
    app.exec_()