"""
    This module contains a function which defines the configurations used
    to set up the database connection
"""

import os


def config_db():
    db = {
        'user': os.environ.get('DATABASE_USER'),
        'password': os.environ.get('DATABASE_PASSW'),
        'host': os.environ.get('DATABASE_HOST'),
        'database': os.environ.get('DATABASE')
    }

    return db
