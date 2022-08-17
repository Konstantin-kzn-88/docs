import mysql.connector as mysql
from faker import Faker

fake = Faker('ru_RU')
ITER = 10  # сколько данных нужно сгенерировать

mysql_conn = mysql.connect(
    host='server167.hosting.reg.ru',
    user='u1082920_qt_cl',
    password='1201kZn1201!',
    database='u1082920_docs_db'
)


def create_insert_sql_request(table: str, fields: tuple) -> str:
    simbol = ('%s, ' * len(fields))[:-2]
    return f'INSERT INTO {table} ({str(fields).strip("()")})  VALUES ({simbol})'.replace("'", "")


with mysql_conn as connection:
    cursor = connection.cursor()
    # vvvvvvvvv___Удаление_таблиц__vvvvvvvvvvvv
    cursor.execute("""DROP TABLE IF EXISTS Device""")
    cursor.execute("""DROP TABLE IF EXISTS Substances""")
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

    # 5 Вещества
    cursor.execute("""CREATE TABLE Substances(Id INT PRIMARY KEY AUTO_INCREMENT, 
                                                Name_sub VARCHAR(50) NOT NULL,
                                                Density VARCHAR(5) NOT NULL,
                                                Density_gas VARCHAR(5) NOT NULL,
                                                Molecular_weight  VARCHAR(5) NOT NULL, 
                                                Steam_pressure  VARCHAR(5) NOT NULL, 
                                                Flash_temperature  VARCHAR(5) NOT NULL,
                                                Boiling_temperature  VARCHAR(5) NOT NULL,
                                                Class_substance  VARCHAR(5) NOT NULL,
                                                Heat_of_combustion VARCHAR(10) NOT NULL,
                                                Sigma VARCHAR(5) NOT NULL,
                                                Energy_level VARCHAR(5) NOT NULL,
                                                Lower_concentration VARCHAR(5) NOT NULL,
                                                Cost VARCHAR(5) NOT NULL)""")

    # 6 Оборудование
    cursor.execute("""CREATE TABLE Device(Id INT PRIMARY KEY AUTO_INCREMENT, ProjectsId INT NOT NULL, SubID INT,
                                              Type_device VARCHAR(10) NOT NULL,  
                                              Pozition VARCHAR(50) NOT NULL, Name VARCHAR(50) NOT NULL,
                                              Locations VARCHAR(50) NOT NULL, Material VARCHAR(50) NOT NULL,
                                              Ground VARCHAR(50) NOT NULL, Target VARCHAR(50) NOT NULL, 
                                              Volume VARCHAR(10) NOT NULL, Completion VARCHAR(5) NOT NULL, 
                                              Pressure VARCHAR(10) NOT NULL, Temperature VARCHAR(10) NOT NULL, 
                                              Spill_square VARCHAR(10) NOT NULL, View_space VARCHAR(10) NOT NULL,
                                              Death_person VARCHAR(10) NOT NULL, Injured_person VARCHAR(10) NOT NULL,
                                              Time_person VARCHAR(10) NOT NULL,
                                              FOREIGN KEY (SubID)  REFERENCES Substances (Id) ON DELETE SET NULL,
                                              CONSTRAINT device_projects_fk FOREIGN KEY (ProjectsId)
                                              REFERENCES Projects (Id) ON DELETE CASCADE)""")

    # vvvvvvvvv___Заполнение_таблиц__vvvvvvvvvvvv
    #  SQL запрос на вставку
    field_dict = {
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
             'Book_dpb', 'Code_dpb', 'Tom_dpb', 'Book_rpz', 'Code_rpz', 'Tom_rpz', 'Book_ifl', 'Code_ifl', 'Tom_ifl',
             'Book_gochs', 'Code_gochs', 'Tom_gochs', 'Section_fire_safety', 'Code_fire_safety', 'Tom_fire_safety'),
        "Substances":
            ('Name_sub', 'Density', 'Density_gas', 'Molecular_weight', 'Steam_pressure', 'Flash_temperature',
             'Boiling_temperature', 'Class_substance', 'Heat_of_combustion', 'Sigma', 'Energy_level',
             'Lower_concentration', 'Cost')
    }

    # 1. Организации
    for _ in range(ITER):
        val = (fake.company(), fake.catch_phrase(),
               fake.job(), fake.name(), fake.job(), fake.name(),
               fake.address(), fake.phone_number(), fake.phone_number(),
               fake.company_email(), fake.random_int(10000, 100000), fake.date_of_birth())

        query = create_insert_sql_request("Organizations", field_dict["Organizations"])
        cursor.execute(query, val)

    # 2. Объекты
    for _ in range(ITER):
        query = create_insert_sql_request("Objects", field_dict["Objects"])

        val = (fake.random_int(1, ITER), fake.text(max_nb_chars=50),
               fake.address(), f"А{fake.random_int(10000, 100000)}", fake.random_int(1, 4))
        cursor.execute(query, val)

    # 3. Проекты
    for _ in range(ITER):
        query = create_insert_sql_request("Projects", field_dict["Projects"])

        val = (fake.random_int(1, ITER), fake.text(max_nb_chars=50),
               f"{fake.random_int(10, 100)}-{fake.random_int(10, 100)}", fake.text(max_nb_chars=200),
               fake.text(max_nb_chars=200))
        cursor.execute(query, val)

    # 4. Наименование томов проекта
    for _ in range(ITER):
        query = create_insert_sql_request("Documents", field_dict["Documents"])
        val = (fake.random_int(1, ITER),
               "Раздел 12 «Иная документация в случаях, предусмотренных федеральными законами»",
               "Часть 1. Декларация промышленной безопасности",
               "Часть 2. «Перечень мероприятий по гражданской обороне»",
               "Книга 1. Декларация промышленной безопасности", "ДПБ1", "12.1.1",
               "Книга 2. Расчентно-пояснительная записка", "ДПБ2", "12.1.2",
               "Книга 3. Информационный лист", "ДПБ3", "12.1.3",
               "", "ГОЧС", "12.2",
               "Раздел 9 «Мероприятия по обеспечению пожарной безопасности»", "ПБ", "9")

        cursor.execute(query, val)

    # 5. Вещества
    for _ in range(ITER):
        query = create_insert_sql_request("Substances", field_dict["Substances"])

        val = ("Нефть", fake.random_int(800, 900), fake.random_int(3, 5),
                fake.random_int(150, 200), fake.random_int(30, 60), fake.random_int(10, 20),
                fake.random_int(300, 400), fake.random_int(1, 4), fake.random_int(45000, 45500),
                "4", "1", fake.random_int(3, 5), "60000")
        cursor.execute(query, val)

    connection.commit()
    connection.close()
