from PySide2.QtSql import QSqlDatabase, QSqlQuery

db = QSqlDatabase.addDatabase("QMYSQL")
db.setHostName("server167.hosting.reg.ru")
db.setDatabaseName("u1082920_docs_db")
db.setUserName("u1082920_qt_cl")
db.setPassword("1201kZn1201!")
db.open()

db.transaction()
query = QSqlQuery()
query.prepare(
    "INSERT INTO Projects (ObjectsId, Name_project, Project_code, Project_description, Аutomation) VALUES (3, ':Name_project', ':Project_code', ':Project_description', ':Аutomation')")
# query.bindValue(':ObjectsId', 3)
# query.bindValue(':Name_project', '111')
# query.bindValue(':Project_code', '111')
# query.bindValue(':Project_description', '111')
# query.bindValue(':Аutomation', '111')
query.exec_()
db.commit()
db.close()
