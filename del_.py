from PySide2.QtSql import QSqlDatabase, QSqlQuery

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
par = "ДНС"
query = QSqlQuery(f'SELECT * FROM Projects  WHERE Project_code="51-91"')
# print(f'SELECT * FROM Projects  WHERE Name_project={par}')
while query.next():
    print(str(query.value(0)) + " " + query.value(3) + " " + query.value(2))
query.exec_()

db.close()
