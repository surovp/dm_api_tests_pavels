from string import ascii_letters, digits
import random


class PostV1AccountData:
    login = 'logintest12'
    password = '123456'
    email = 'logintest12@test'


def random_string(start=1, end=30):
    symbols = ascii_letters + digits
    string = ''
    for _ in range(random.randint(start, end)):
        string += random.choice(symbols)
    return string


random_email = f'{random_string()}@{random_string()}.{random_string()}'
invalid_email = f'{random_string(6)}@'
invalid_email_1 = random_string(1, 2).replace('@', '')

valid_login = random_string(2)
invalid_login = random_string(1, 1)

valid_password = random_string(6)
invalid_password = random_string(1, 5)

random_datas = [
    (valid_login, random_email, valid_password, 201, ''),
    (valid_login, random_email, invalid_password, 400, {"Password": ["Short"]}),
    (invalid_login, random_email, valid_password, 400, {"Login": ["Short"]}),
    (valid_login, invalid_email, valid_password, 400, {"Email": ["Invalid"]}),
    (valid_login, invalid_email_1, valid_password, 400, {"Email": ["Invalid"]}),
]

