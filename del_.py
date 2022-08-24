from PySide2.QtSql import QSqlDatabase, QSqlQuery

db = QSqlDatabase.addDatabase("QMYSQL")
db.setHostName("server167.hosting.reg.ru")
db.setDatabaseName("u1082920_default")
db.setUserName("u1082920_test")
db.setPassword("1501kZn1501!")
db.open()


query = QSqlQuery()

# query.prepare("""DROP TABLE IF EXISTS Projects""")
# query.exec_()
#
# query.prepare("""CREATE TABLE Projects(Id INT PRIMARY KEY AUTO_INCREMENT, ObjectsId INT NOT NULL,
#                                               Name_project VARCHAR(200) NOT NULL, Project_code VARCHAR(20) NOT NULL,
#                                               Project_description TEXT NOT NULL, Project_automat TEXT NOT NULL)""")
# query.exec_()

# # query.prepare("DELETE FROM Projects WHERE Аutomation=':Аutomation'")
# query.exec_()

query.prepare(
    "INSERT INTO Projects (ObjectsId, Name_project, Project_code, Project_description, Project_automat) VALUES (:ObjectsId, :Name_project, :Project_code, :Project_description, :Project_automat)")
query.bindValue(':ObjectsId', 3)
query.bindValue(':Name_project', '111')
query.bindValue(':Project_code', '111')
query.bindValue(':Project_description', ':Project_description')
query.bindValue(':Project_automat', 'dfgdgrgrdrgdgrdrgdrgdrg')
query.exec_()
db.commit()
query = QSqlQuery('SELECT * FROM Projects')
while query.next():
    print(str(query.value(0)) + " " + str(query.value(1)) + " " + query.value(2) + " " + query.value(3)+ " " + query.value(4)+ " " + query.value(5))
db.close()
