import psycopg2

from .config import config_db
from .queries import *

connection = None


class Database:

    def init_db(self):
        connection = psycopg2.connect(**config_db())

        return connection

    @classmethod
    def create_tables(cls):
        statements = [
            CREATE_TABLE_USERS,
            CREATE_TABLE_MEETUPS,
            CREATE_TABLE_RSVPS,
            CREATE_TABLE_QUESTIONS,
            CREATE_TABLE_TOKENS,
            CREATE_TABLE_QVOTES]

        print("Creating Tables")

        for statement in statements:
            query_db(statement)
        print("Created Tables")

    @classmethod
    def drop_tables(cls):
        query_db(DROP_TABLES)


def query_db(statement, values=None, rowcount=False,
             return_value=False, one=False, many=False):
    result = None
    global connection

    try:
        connection = db_instance.init_db()
        cursor = connection.cursor()

        if one:
            cursor.execute(statement, values)
            result = cursor.fetchone()
        elif many:
            if values:
                cursor.execute(statement, values)
            else:
                cursor.execute(statement)
            result = cursor.fetchall()
        elif rowcount:
            cursor.execute(statement, values)
            result = cursor.rowcount
        else:
            cursor.execute(statement)

        connection.commit()
        cursor.close()

    except (Exception, psycopg2.DatabaseError) as er:
        print(er)
    finally:
        if (connection):
            connection.close()

    return result


db_instance = Database()
