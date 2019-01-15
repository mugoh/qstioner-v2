"""
    This module contains validators for user data passed in request
    arguments.
"""

import re
import datetime

name_pattern = re.compile(r'^[A-Za-z]+$')


def verify_pass(value):
    if len(value) < 6:
        raise ValueError("Password should be at least 6 charcters")
    return value


def verify_name(value, item):
    if ' ' in value:
        raise ValueError(f'{value} has spaces. {item} should not have spaces')

    elif not name_pattern.match(value):
        raise ValueError(f'Oops! {value} has NUMBERS.' +
                         f' {item} should contain letters only')
    return value


def validate_date(value):
    """
        Ensures passing of valid datetime format in date inputs
    """
    try:
        datetime.datetime.strptime(value, '%Y-%m-%dT%H:%M:%S')
    except ValueError:
        raise ValueError(
            "Incorrect data format, should be YYYY-MM-DDTHH:MM:SS")
    return value
