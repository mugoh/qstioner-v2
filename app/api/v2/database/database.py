import psycopg2

from .config import config_db


class Database:

    def init_db(self):
        conn = psycopg2.connect(**config_db())

        return conn

    @classmethod
    def create_tables(cls):
        statements = [
            CREATE_TABLE_USERS,
            CREATE_TABLE_MEETUPS,
            CREATE_TABLE_RSVPS,
            CREATE_TABLE_QUESTIONS,
            CREATE_TABLE_TOKENS]

        for statement in statements:
            query_db(statement)
