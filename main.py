import sys
import os
from pathlib import Path
from PySide2.QtSql import QSqlDatabase, QSqlQuery, QSqlRelationalTableModel
from PySide2.QtWidgets import QApplication, QMainWindow, QComboBox, QMessageBox, QWidget, QGridLayout, QFormLayout, QGroupBox, QTableView, QStyleFactory
from PySide2.QtGui import QIcon




db = QSqlDatabase.addDatabase("QMYSQL")
db.setHostName("server167.hosting.reg.ru")
db.setDatabaseName("u1082920_docs_db")
db.setUserName("u1082920_qt_cl")
db.setPassword("1201kZn1201!")
db.open()


if db.open():
    print("Database Open!")
else:
    print("Database NOT Open!")





class MainWindow(QMainWindow):
    def __init__(self, parent=None) -> None:
        super().__init__()
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
        # ___________1_START________________
        # Рамка
        layout_select = QFormLayout(self)
        GB_select = QGroupBox('Выбор')
        GB_select.setStyleSheet("QGroupBox { font-weight : bold; }")
        self.organisation_list = QComboBox()
        layout_select.addRow("", self.organisation_list)
        GB_select.setLayout(layout_select)

        # ___________2_START________________
        # Рамка
        layout_table = QFormLayout(self)
        GB_table = QGroupBox('Выбор')
        GB_table.setStyleSheet("QGroupBox { font-weight : bold; }")
        self.table = QTableView()
        self.model = QSqlRelationalTableModel(db=db)
        self.table.setModel(self.model)
        self.model.setTable("Organizations")
        self.model.select()
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

        self.show()

    def set_ico(self):
        path_ico = str(Path(os.getcwd()))
        print(path_ico)
        self.main_ico = QIcon(path_ico + '/ico/main.png')
        self.setWindowIcon(self.main_ico)



    def closeEvent(self, event):
        reply = QMessageBox.question\
        (self, 'Выход из программы',
            "Вы уверены, что хотите уйти?",
             QMessageBox.Yes,
             QMessageBox.No)
        if reply == QMessageBox.Yes:
            db.close()
            event.accept()
        else:
            event.ignore()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('Fusion'))
    window = MainWindow()
    app.exec_()
