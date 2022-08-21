import sys
import os
from pathlib import Path
from PySide2.QtSql import QSqlDatabase, QSqlQuery, QSqlRelationalTableModel, QSqlRelation
from PySide2.QtWidgets import QApplication, QMainWindow, QComboBox, QMessageBox, QWidget, QGridLayout, \
    QFormLayout, QGroupBox, QTableView, QStyleFactory, QStyledItemDelegate, QHeaderView, QMenu, QAction, QDialog, \
    QDialogButtonBox, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, QTableWidget, QTableWidgetItem
from PySide2.QtGui import QIcon
from PySide2.QtCore import Qt
from itertools import count

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
                ('ObjectsId', 'Name_project', 'Project_code', 'Project_description', 'Аutomation'),
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
                ('ProjectsId', 'SubId', 'Type_device', 'Pozition', 'Name', 'Locations', 'Material', 'Ground', 'Target',
                 'Volume', 'Completion', 'Pressure', 'Temperature', 'Spill_square', 'View_space', 'Death_person',
                 'Injured_person', 'Time_person'),
            "Pipelines":
                ('ProjectsId', 'SubId', 'Pozition', 'Name', 'Locations', 'Material', 'Ground', 'Target',
                 'Length', 'Diameter', 'Pressure', 'Temperature', 'Flow', 'View_space', 'Death_person',
                 'Injured_person', 'Time_person')
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
        GB_select = QGroupBox('Выбор')
        GB_select.setStyleSheet("QGroupBox { font-weight : bold; }")
        self.select_table = QComboBox()
        self.select_table.addItems(self.table_list)
        self.select_table.currentIndexChanged.connect(self.show_table)
        layout_select.addRow("", self.select_table)
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

        query = QSqlQuery()
        query.exec_("SELECT Name_org FROM Organizations")
        while query.next():
            print(query.value(0))

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
        # 1. Файл
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
        # del_object.triggered.connect(self.database_connect)
        # Меню приложения (верхняя плашка)
        menubar = self.menuBar()
        data_menu = menubar.addMenu('Данные')
        data_menu.addMenu(add_menu)
        data_menu.addAction(del_object)
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

        self.model.select()

    def add_data_in_db(self):
        sender = self.sender()
        if self.sender_list.index(sender.text()) == 0:
            inputDialog = Add_Dialog(state=sender.text(), header_dict=self.field_dict)
            rez = inputDialog.exec()
            if not rez:
                _ = QMessageBox.information(self, 'Внимание!', 'Добавление в базу данных отменено')
                return

            data = []
            for row in range(inputDialog.tableWidget.rowCount()):
                if inputDialog.tableWidget.item(row, 1) is not None:
                    data.append(inputDialog.tableWidget.item(row, 1).text())
                else:
                    _ = QMessageBox.information(self, 'Внимание!',
                                                'Данные не заполнены. Добавление в базу данных не возможно!')
                    return

            print(self.__create_insert_sql_request(table = "Organizations", fields = self.field_dict_in_db["Organizations"]))
            db.transaction()
            query = QSqlQuery()
            query.prepare(
                "INSERT INTO Organizations (Name_org, Name_org_full, Director, Name_director, Tech_director, Name_tech_director, Jur_adress, Telephone, Fax, Email, License, Date_get_license) "
                "VALUES (:Name_org, :Name_org_full, :Director, :Name_director, :Tech_director, :Name_tech_director, :Jur_adress, :Telephone, :Fax, :Email, :License, :Date_get_license)")
            query.bindValue(":Name_org", data[0])
            query.bindValue(":Name_org_full", data[1])
            query.bindValue(":Director", data[2])
            query.bindValue(":Name_director", data[3])
            query.bindValue(":Tech_director", data[4])
            query.bindValue(":Name_tech_director", data[5])
            query.bindValue(":Jur_adress", data[6])
            query.bindValue(":Telephone", data[7])
            query.bindValue(":Fax", data[8])
            query.bindValue(":Email", data[9])
            query.bindValue(":License", data[10])
            query.bindValue(":Date_get_license", data[11])

            query.exec_()
            db.commit()


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
        self.setWindowIcon(self.main_ico)

    def __create_insert_sql_request(self, table: str, fields: tuple) -> str:
        simbol = [f':{i}' for i in fields]
        return f'INSERT INTO {table} ({str(fields).strip("()")})  VALUES ({simbol})'.replace('[', '').replace(']', '')

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


class Add_Dialog(QDialog):
    def __init__(self, state: str, header_dict: dict):
        super().__init__()
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)  # убрать знак вопроса

        path_ico = str(Path(os.getcwd()))
        main_ico = QIcon(path_ico + '/ico/main.png')
        self.setWindowIcon(main_ico)
        self.setWindowTitle('Добавление информации')
        print(f"state={state}")
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(2)

        if state == 'Организация':
            row_count = len(header_dict['Organizations'])
            self.tableWidget.setRowCount(row_count)
            for i in range(row_count):
                self.tableWidget.setItem(i, 0, QTableWidgetItem(header_dict['Organizations'][i]))

        button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.tableWidget)
        main_layout.addWidget(button_box)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('Fusion'))
    window = MainWindow()
    app.exec_()
