from generic.helpers.orm_db import OrmDatabase
from services.dm_api_account import Facade
import structlog


structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)
    ]
)


def test_create_and_logout_user1():
    api = Facade(host='http://localhost:5051')
    login = 'logintest15'
    email = 'logintest15@test'
    password = 'logintest15'
    response = api.account.register_new_user(
        login=login,
        email=email,
        password=password,
        status_code=201
    )
    api.account.activate_registered_user(login=login)
    api.login.login_user(
        login=login,
        password=password
    )
    token = api.login.get_auth_token(
        login=login,
        password=password
    )
    api.login.set_headers(headers=token)
    api.login.logout_user()


def test_create_and_logout_user2():
    api = Facade(host='http://localhost:5051')
    login = 'logintest16'
    email = 'logintest16@test'
    password = 'logintest16'
    response = api.account.register_new_user(
        login=login,
        email=email,
        password=password,
        status_code=201
    )
    api.account.activate_registered_user(login=login)
    api.login.login_user(
        login=login,
        password=password
    )
    token = api.login.get_auth_token(
        login=login,
        password=password
    )
    api.login.logout_user(headers=token)


# тест активации активированного пользователя
def test_activate_activated_user():

    api = Facade(host='http://localhost:5051')
    login = 'logintest26'
    email = 'logintest26@test'
    password = 'logintest26'

    response = api.account.register_new_user(
        login=login,
        email=email,
        password=password,
        status_code=201
    )
    orm = OrmDatabase(user='postgres', password='admin', host='localhost', database='dm3.5')
    orm.activate_user(login=login, is_activate=True)
    api.account.activate_registered_user(login=login)

    dataset = orm.get_user_by_login(login=login)
    for row in dataset:
        assert row.Activated is True, f'User {login} not activated'
    orm.db.close_connection()


