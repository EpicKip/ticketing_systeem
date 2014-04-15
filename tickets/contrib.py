__author__ = 'Aaron'

import uuid


def password_random(string_length):
    random = str(uuid.uuid4())
    random = random.upper()
    random = random.replace("-", "")
    return random[0:string_length]