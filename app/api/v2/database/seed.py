"""
    This module contains a function that default
    columns the applicaiton database.
"""
from ..models.users import UserModel


def seed_user():
    """
        Creates a default admin user on initialization
        of the aplpication.
    """
    user_details = dict(firstname="namecow",
                        lastname="unnamecow",
                        othername="justAdmin",
                        email="admincow@mammals.milk",
                        phonenumber=723487,
                        username="DomesticableAdminCow",
                        isadmin=True,
                        password="pa555word")
    seeded = UserModel(**user_details).save()
    if seeded:
        print("Admin created")
