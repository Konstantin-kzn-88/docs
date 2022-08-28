from PySide2.QtSql import QSqlDatabase, QSqlQuery

# placeholder [':Name_sub', ':Density', ':Density_gas', ':Molecular_weight', ':Steam_pressure', ':Flash_temperature', ':Boiling_temperature', ':Class_substance', ':Heat_of_combustion', ':Sigma', ':Energy_level', ':Lower_concentration', ':Cost']
# sql_request INSERT INTO Substances (Name_sub, Density, Density_gas, Molecular_weight, Steam_pressure, Flash_temperature, Boiling_temperature, Class_substance, Heat_of_combustion, Sigma, Energy_level, Lower_concentration, Cost) VALUES (:Name_sub, :Density, :Density_gas, :Molecular_weight, :Steam_pressure, :Flash_temperature, :Boiling_temperature, :Class_substance, :Heat_of_combustion, :Sigma, :Energy_level, :Lower_concentration, :Cost)


db = QSqlDatabase.addDatabase("QMYSQL")
db.setHostName("server167.hosting.reg.ru")
db.setDatabaseName("u1082920_default")
db.setUserName("u1082920_test")
db.setPassword("1501kZn1501!")
db.open()

if db.open():
    print("Database Open!")
else:
    print(f"Database NOT Open cause {db.lastError().text()}")

query = QSqlQuery()

query.prepare("""DROP TABLE IF EXISTS Substances""")
query.exec_()

# query.prepare("""CREATE TABLE Substances(Id INT PRIMARY KEY AUTO_INCREMENT,
#                                                 Name_sub VARCHAR(50) NOT NULL)""")
# query.exec_()
#
# # # query.prepare("DELETE FROM Projects WHERE Аutomation=':Аutomation'")
# # query.exec_()
#
# query.prepare(
#     "INSERT INTO Substances (Name_sub, Density, Density_gas, Molecular_weight, Steam_pressure, Flash_temperature, Boiling_temperature, Class_substance, Heat_of_combustion, Sigma, Energy_level, Lower_concentration, Cost) "
#     "VALUES "
#     "(':Name_sub', ':Density', ':Density_gas', ':Molecular_weight', ':Steam_pressure', ':Flash_temperature', ':Boiling_temperature', ':Class_substance', ':Heat_of_combustion', ':Sigma', ':Energy_level', ':Lower_concentration', ':Cost'")

# placeholder = [':Name_sub', ':Density', ':Density_gas', ':Molecular_weight', ':Steam_pressure', ':Flash_temperature', ':Boiling_temperature', ':Class_substance', ':Heat_of_combustion', ':Sigma', ':Energy_level', ':Lower_concentration', ':Cost']
# for i in placeholder:
#     query.bindValue(i, 3)
# query.exec_()
# db.commit()
# query = QSqlQuery('SELECT * FROM Substances')
# while query.next():
#     print(str(query.value(0)) + " " + str(query.value(1)) + " " + query.value(2) + " " + query.value(3)+ " " + query.value(4)+ " " + query.value(5))
db.close()
