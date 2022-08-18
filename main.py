import sys

from PySide2.QtCore import QSize
from PySide2.QtSql import QSqlDatabase, QSqlQuery
from PySide2.QtWidgets import QApplication, QMainWindow, QComboBox





db = QSqlDatabase.addDatabase("QMYSQL")
db.setHostName("server167.hosting.reg.ru")
db.setDatabaseName("u1082920_docs_db")
db.setUserName("u1082920_root")
db.setPassword("1501kZn1501!")
db.open()

print(db, type(db))
if db.open():
    print("Database Open!")
else:
    print("Database NOT Open!")




class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.qbox = QComboBox()
        query = QSqlQuery()



        self.setMinimumSize(QSize(1024, 600))
        self.setCentralWidget(self.QComboBox)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
