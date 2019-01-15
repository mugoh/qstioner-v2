"""
    This module contains the class that creates blacklisted token objects
    and checks for token validity
"""


class Token:

    def __init__(self, token):
        self.signature = token
        self.save()

    def save(self):
        blacklisted_tokens.add(self)

    @classmethod
    def check_if_blacklisted(cls, given_token):
        return [token for token in blacklisted_tokens if
                getattr(token, 'signature') == given_token]


blacklisted_tokens = set()
