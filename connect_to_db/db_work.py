import mysql.connector as mysql

mysql_conn = mysql.connect(
    host='server167.hosting.reg.ru',
    user='u1082920_root',
    password='1501kZn1501!',
    database = 'u1082920_docs_db'
)

with mysql_conn as connection:
    cursor = connection.cursor()
    cursor.execute("""DROP TABLE IF EXISTS objects""")
    cursor.execute("""CREATE TABLE objects(id INTEGER PRIMARY KEY, data TEXT NOT NULL,
                                            plan TEXT NOT NULL, name_plan TEXT NOT NULL)""")
    # # SQL запрос на вставку
    query = f"INSERT INTO objects (id, data,plan,name_plan) VALUES ('{1}', '{str(2)}', '{str(3)}', '{str(4)}')"
    cursor.execute(query)
    query = f"INSERT INTO objects (id, data,plan,name_plan) VALUES ('{2}', '{str(2)}', '{str(3)}', '{str(4)}')"
    cursor.execute(query)

    connection.commit()
    connection.close()