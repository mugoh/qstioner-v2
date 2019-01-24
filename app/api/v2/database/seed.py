"""
    This module contains a function that default
    columns the applicaiton database.
"""
from .database import query_db
from .queries import CREATE_USER


def seed_user():
    user_details = dict(firstname="namecow",
                        lastname="unnamecow",
                        othername="justAdmin",
                        email="admincow@mammals.milk",
                        phonenumber=723487,
                        username="DomesticableAdminCow",
                        isAdmin=True,
                        password="pa555word")
    seeded = query_db(CREATE_USER, tuple(user_details.values()), one=True)
    if seeded:
        print("Admin created")
