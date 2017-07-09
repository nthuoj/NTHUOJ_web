from django.conf import settings

SQL_DIR = settings.BASE_DIR + '/sql/'


def get_sql_from_file(file_name, formatting_tuple=()):
    file_location = SQL_DIR + file_name
    sql_statement = ""
    with open(file_location, 'r') as fp:
        sql_statement = fp.read()
    return sql_statement % formatting_tuple
