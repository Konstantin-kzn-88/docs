
str_ = "INSERT INTO Organizations (Name_org, Name_org_full, Director, Name_director, Tech_director, Name_tech_director, Jur_adress, Telephone, Fax, Email, License, Date_get_license) VALUES (:Name_org, :Name_org_full, :Director, :Name_director, :Tech_director, :Name_tech_director, :Jur_adress, :Telephone, :Fax, :Email, :License, :Date_get_license)"




table = 'Organizations'
fields = ('Name_org', 'Name_org_full', 'Director', 'Name_director', 'Tech_director', 'Name_tech_director',
          'Jur_adress', 'Telephone', 'Fax', 'Email', 'License', 'Date_get_license')

def __create_insert_sql_request(table: str, fields: tuple) -> str:
    simbol = [f":{i}" for i in fields]
    print(simbol)
    fields = str(fields).strip("()")
    fields = fields.replace("'", "")

    return f'INSERT INTO {table} ({fields}) VALUES ({simbol})'.replace('[', '').replace(']', '').replace("'", "")


my_str = __create_insert_sql_request(table, fields)
print(my_str == str_)