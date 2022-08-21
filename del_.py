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



db.transaction()
query = QSqlQuery()
# query.exec_("DROP TABLE IF EXISTS test;")
# query.exec_()
# query.exec_("CREATE TABLE test (Id INT PRIMARY KEY AUTO_INCREMENT, name_company TEXT NOT NULL, address TEXT NOT NULL);")
# query.exec_()
query.prepare("INSERT INTO Organizations (Name_org, Name_org_full, Director, Name_director, Tech_director, Name_tech_director, Jur_adress, Telephone, Fax, Email, License, Date_get_license) "
              "VALUES (:Name_org, :Name_org_full, :Director, :Name_director, :Tech_director, :Name_tech_director, :Jur_adress, :Telephone, :Fax, :Email, :License, :Date_get_license)")
query.bindValue(":Name_org", 'АО Rjgsnf')
query.bindValue(":Name_org_full", 'sdsdfc')
query.bindValue(":Director", 'АО Rjgsnf')
query.bindValue(":Name_director", 'sdsdfc')
query.bindValue(":Tech_director", 'АО Rjgsnf')
query.bindValue(":Name_tech_director", 'sdsdfc')
query.bindValue(":Jur_adress", 'АО Rjgsnf')
query.bindValue(":Telephone", 'sdsdfc')
query.bindValue(":Fax", 'АО Rjgsnf')
query.bindValue(":Email", 'sdsdfc')
query.bindValue(":License", 'АО Rjgsnf')
query.bindValue(":Date_get_license", 'sdsdfc')

query.exec_()
db.commit()

db.close()




