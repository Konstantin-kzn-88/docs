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
    cursor.execute("""DROP TABLE IF EXISTS Documents""")
    cursor.execute("""DROP TABLE IF EXISTS Projects""")
    cursor.execute("""DROP TABLE IF EXISTS Objects""")
    cursor.execute("""DROP TABLE IF EXISTS Organizations""")
    # vvvvvvvvv___Создание таблиц__vvvvvvvvvvvv
    # 1 Организации
    cursor.execute("""CREATE TABLE Organizations(Id INT PRIMARY KEY AUTO_INCREMENT,
                                                Name_org VARCHAR(100) NOT NULL, Name_org_full VARCHAR(100) NOT NULL,
                                                Director VARCHAR(100) NOT NULL, Name_director VARCHAR(100) NOT NULL,
                                                Tech_director VARCHAR(100) NOT NULL, Name_tech_director VARCHAR(100) NOT NULL,
                                                Jur_adress VARCHAR(100) NOT NULL, Telephone VARCHAR(100) NOT NULL,
                                                Fax VARCHAR(20) NOT NULL, Email VARCHAR(20) NOT NULL,
                                                License VARCHAR(20) NOT NULL, Date_get_license VARCHAR(20) NOT NULL)""")
    # 2 Объекты
    cursor.execute("""CREATE TABLE Objects(Id INT PRIMARY KEY AUTO_INCREMENT, OrganizationId INT NOT NULL,
                                              Name_opo VARCHAR(100) NOT NULL, Address_opo VARCHAR(100) NOT NULL,
                                              Reg_number_opo VARCHAR(20) NOT NULL, Class_opo VARCHAR(20) NOT NULL,
                                              CONSTRAINT objects_organizations_fk FOREIGN KEY (OrganizationId)
                                              REFERENCES Organizations (Id) ON DELETE CASCADE)""")
    # 3 Проекты
    cursor.execute("""CREATE TABLE Projects(Id INT PRIMARY KEY AUTO_INCREMENT, ObjectsId INT NOT NULL,
                                              Name_project VARCHAR(200) NOT NULL, Project_code VARCHAR(20) NOT NULL,
                                              Project_description TEXT NOT NULL, Аutomation TEXT NOT NULL,
                                              CONSTRAINT projects_objects_fk FOREIGN KEY (ObjectsId)
                                              REFERENCES Objects (Id) ON DELETE CASCADE)""")

    # 4 Наименование томов проекта
    cursor.execute("""CREATE TABLE Documents(Id INT PRIMARY KEY AUTO_INCREMENT, ProjectsId INT NOT NULL,
                                              Section_other_documentation VARCHAR(50) NOT NULL,
                                              Part_other_documentation_dpb VARCHAR(50) NOT NULL,
                                              Part_other_documentation_gochs VARCHAR(50) NOT NULL,
                                              Book_dpb VARCHAR(50) NOT NULL,
                                              Code_dpb VARCHAR(10) NOT NULL,
                                              Tom_dpb VARCHAR(10) NOT NULL,
                                              Book_rpz VARCHAR(50) NOT NULL,
                                              Code_rpz VARCHAR(10) NOT NULL,
                                              Tom_rpz VARCHAR(10) NOT NULL,
                                              Book_ifl VARCHAR(50) NOT NULL,
                                              Code_ifl VARCHAR(10) NOT NULL,
                                              Tom_ifl VARCHAR(10) NOT NULL,
                                              Book_gochs VARCHAR(50) NOT NULL,
                                              Code_gochs VARCHAR(10) NOT NULL,
                                              Tom_gochs VARCHAR(10) NOT NULL,
                                              Section_fire_safety VARCHAR(50) NOT NULL,
                                              Code_fire_safety VARCHAR(10) NOT NULL,
                                              Tom_fire_safety VARCHAR(10) NOT NULL,
                                              CONSTRAINT documents_projects_fk FOREIGN KEY (ProjectsId)
                                              REFERENCES Projects (Id) ON DELETE CASCADE)""")



    # vvvvvvvvv___Заполнение_таблиц__vvvvvvvvvvvv
    #  SQL запрос на вставку
    # 1. Организации
    query = f"INSERT INTO Organizations (Name_org, Name_org_full, Director, Name_director, " \
            f"Tech_director, Name_tech_director, Jur_adress, " \
            f"Telephone, Fax, Email, License, Date_get_license) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = ("ООО «Карбон-Ойл»", "Общество с ограниченной ответственностью ООО «Карбон-Ойл»",
           "Генеральный директор", "Хузин Р.Р.", "", "",
           "423450, Республика Татарстан, Альметьевский район, город Альметьевск, Сургутская улица, дом 25",
           "8(8553)37-47-00", "8(8553)37-47-00", "-",
           'ЭВ-00-007624', '17.07.2007')
    cursor.execute(query, val)

    query2 = f"INSERT INTO Organizations (Name_org, Name_org_full, Director, Name_director, " \
             f"Tech_director, Name_tech_director, Jur_adress, " \
             f"Telephone, Fax, Email, License, Date_get_license) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val2 = ("АО «Татех»", "Акционерное общество «Татех»",
            "Генеральный директор", "Хайруллин Ирек Акрамович", "Главный инженер", "Верия Евгений Иванович",
            "Республика Татарстан, г. Альметьевск, ул. Маяковского, д. 116",
            "8(8553)39-70-01", "8(8553)39-70-70", "-",
            'ВП-00-010185', '14.04.2016')
    cursor.execute(query2, val2)
    # 2. Объекты
    query3 = f"INSERT INTO Objects (OrganizationId, Name_opo, Address_opo, " \
             f"Reg_number_opo, Class_opo) VALUES (%s, %s, %s, %s, %s)"
    val3 = (1, "Система промысловых трубопроводов Фомкинского месторождения нефти",
            "Российская Федерация, Республика Татарстан, Нурлатский муниципальный район", "А43-04735-0015", "III")
    cursor.execute(query3, val3)

    query4 = f"INSERT INTO Objects (OrganizationId, Name_opo, Address_opo, " \
             f"Reg_number_opo, Class_opo) VALUES (%s, %s, %s, %s, %s)"
    val4 = (2, "Система промысловых трубопроводов Демкинского месторождения нефти",
            "Российская Федерация, Республика Татарстан, Аксубаевский муниципальный район", "А43-00625-0048", "II")
    cursor.execute(query4, val4)

    # 3. Проекты
    query5 = f"INSERT INTO Projects (ObjectsId, Name_project, Project_code, Project_description, Аutomation) " \
             f"VALUES (%s, %s, %s, %s, %s)"
    val5 = (1, "Строительство нефтесборного трубопровода от МНС-644 Максимкинского нефтяного "
               "месторождения до МНС-645 с СПН-250 Фомкинского нефтяного месторождения",
            "65-20", "Проектом предусмотрено...", "Проектом предусмотрена автоматизация...")
    cursor.execute(query5, val5)

    query6 = f"INSERT INTO Projects (ObjectsId, Name_project, Project_code, Project_description, Аutomation) " \
             f"VALUES (%s, %s, %s, %s, %s)"
    val6 = (2, "Обустройство куста скважин К-Д8 Демкинского нефтяного месторождения АО «Татех",
            "70-20", "Проектом предусмотрено...", "Проектом предусмотрена автоматизация...")
    cursor.execute(query6, val6)

    # 4. Документы
    query7 = f"INSERT INTO Documents " \
             f"(ProjectsId, " \
             f"Section_other_documentation, " \
             f"Part_other_documentation_dpb, " \
             f"Part_other_documentation_gochs, " \
             f"Book_dpb, Code_dpb, Tom_dpb, " \
             f"Book_rpz, Code_rpz, Tom_rpz, " \
             f"Book_ifl, Code_ifl, Tom_ifl, " \
             f"Book_gochs, Code_gochs, Tom_gochs, " \
             f"Section_fire_safety, " \
             f"Code_fire_safety, Tom_fire_safety) " \
             f"VALUES " \
             f"(%s, %s, %s, " \
             f"%s, %s, %s, " \
             f"%s, %s, %s, " \
             f"%s, %s, %s, " \
             f"%s, %s, %s, " \
             f"%s, %s, %s, " \
             f"%s)"

    val7 = (1,
            "Раздел 12 «Иная документация в случаях, предусмотренных федеральными законами»",
            "Часть 1. Декларация промышленной безопасности",
            "Часть 2. «Перечень мероприятий по гражданской обороне»",
            "Книга 1. Декларация промышленной безопасности", "ДПБ1", "12.1.1",
            "Книга 2. Расчентно-пояснительная записка", "ДПБ2", "12.1.2",
            "Книга 3. Информационный лист", "ДПБ3", "12.1.3",
            "", "ГОЧС", "12.2",
            "Раздел 9 «Мероприятия по обеспечению пожарной безопасности»", "ПБ", "9")

    cursor.execute(query7, val7)

    query8 = f"INSERT INTO Documents " \
             f"(ProjectsId, " \
             f"Section_other_documentation, " \
             f"Part_other_documentation_dpb, " \
             f"Part_other_documentation_gochs, " \
             f"Book_dpb, Code_dpb, Tom_dpb, " \
             f"Book_rpz, Code_rpz, Tom_rpz, " \
             f"Book_ifl, Code_ifl, Tom_ifl, " \
             f"Book_gochs, Code_gochs, Tom_gochs, " \
             f"Section_fire_safety, " \
             f"Code_fire_safety, Tom_fire_safety) " \
             f"VALUES " \
             f"(%s, %s, %s, " \
             f"%s, %s, %s, " \
             f"%s, %s, %s, " \
             f"%s, %s, %s, " \
             f"%s, %s, %s, " \
             f"%s, %s, %s, " \
             f"%s)"

    val8 = (1,
            "Раздел 10 «Иная документация в случаях, предусмотренных федеральными законами»",
            "Часть 1. Декларация промышленной безопасности",
            "Часть 2. «Перечень мероприятий по гражданской обороне»",
            "Книга 1. Декларация промышленной безопасности", "ДПБ1", "10.1.1",
            "Книга 2. Расчентно-пояснительная записка", "ДПБ2", "10.1.2",
            "Книга 3. Информационный лист", "ДПБ3", "10.1.3",
            "", "ГОЧС", "10.2",
            "Раздел 9 «Мероприятия по обеспечению пожарной безопасности»", "ПБ", "9")

    cursor.execute(query8, val8)

    connection.commit()
    connection.close()
