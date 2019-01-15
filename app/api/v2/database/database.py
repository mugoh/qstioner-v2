import psycopg2

from .config import config_db

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
            CREATE_TABLE_TOKENS]

        print("Created Tables")

        for statement in statements:
            query_db(statement)


def query_db(statement, rowcount=False, return_value=False, one=False, many=False):

    try:
        global connection

        connection = db_instance.init_db()
        cursor = connection.cursor()

        connection.commit()
        cursor.close()

    except (Exception, psycopyg2.DatabaseError) as er:
        print(er)
    finally:
        if connection:
            connection.close()

    return


db_instance = Database()
