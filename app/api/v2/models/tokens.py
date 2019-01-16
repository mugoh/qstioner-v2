"""
    This module contains the class that creates blacklisted token objects
    and checks for token validity
"""

from ..database.queries import CREATE_TOKEN, GET_TOKEN
from ..database.database import query_db


class Token:

    def __init__(self, token):
        self.signature = token
        self.save()

    def save(self):
        query_db(CREATE_TOKEN, (self.signature,), one=True)

    @classmethod
    def check_if_blacklisted(cls, given_token):
        return query_db(GET_TOKEN, (given_token,), one=True)
