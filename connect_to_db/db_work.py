import mysql.connector as mysql

mysql_conn = mysql.connect(
    host='server167.hosting.reg.ru',
    user='u1082920_qt_cl',
    password='1201kZn1201!',
    database='u1082920_docs_db'
)

with mysql_conn as connection:
    cursor = connection.cursor()
    # vvvvvvvvv___Удаление_таблиц__vvvvvvvvvvvv
    cursor.execute("""DROP TABLE IF EXISTS Projects""")
    cursor.execute("""DROP TABLE IF EXISTS Objects""")
    cursor.execute("""DROP TABLE IF EXISTS Organizations""")
    # vvvvvvvvv___Создание таблиц__vvvvvvvvvvvv
    # 1 Организации
    cursor.execute("""CREATE TABLE Organizations(Id INT PRIMARY KEY AUTO_INCREMENT,
                                                Name_org CHAR NOT NULL, Name_org_full CHAR NOT NULL,
                                                Director CHAR NOT NULL, Name_director CHAR NOT NULL,
                                                Tech_director CHAR NOT NULL, Name_tech_director CHAR NOT NULL,
                                                Jur_adress CHAR NOT NULL, Telephone CHAR NOT NULL,
                                                Fax CHAR NOT NULL, Email CHAR NOT NULL,
                                                License CHAR NOT NULL, Date_get_license CHAR NOT NULL)""")
    # 2 Объекты
    cursor.execute("""CREATE TABLE Objects(Id INT PRIMARY KEY AUTO_INCREMENT, OrganizationId INT NOT NULL,
                                              Name_opo CHAR NOT NULL, Address_opo CHAR NOT NULL,
                                              Reg_number_opo CHAR NOT NULL, Class_opo CHAR NOT NULL,
                                              CONSTRAINT objects_organizations_fk FOREIGN KEY (OrganizationId)
                                              REFERENCES Organizations (Id) ON DELETE CASCADE)""")
    # 3 Проекты
    cursor.execute("""CREATE TABLE Projects(Id INT PRIMARY KEY AUTO_INCREMENT, ObjectsId INT NOT NULL,
                                              Name_project CHAR NOT NULL, Project_code CHAR NOT NULL,
                                              CONSTRAINT projects_objects_fk FOREIGN KEY (ObjectsId)
                                              REFERENCES Objects (Id) ON DELETE CASCADE)""")

    # # # SQL запрос на вставку
    # query = f"INSERT INTO objects (id, data,plan,name_plan) VALUES ('{1}', '{str(2)}', '{str(3)}', '{str(4)}')"
    # cursor.execute(query)
    # query = f"INSERT INTO objects (id, data,plan,name_plan) VALUES ('{2}', '{str(2)}', '{str(3)}', '{str(4)}')"
    # cursor.execute(query)

    connection.commit()
    connection.close()
