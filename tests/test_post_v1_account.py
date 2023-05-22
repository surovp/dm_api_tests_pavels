import time

from hamcrest import assert_that, has_properties

from generic.helpers.orm_db import OrmDatabase
from services.dm_api_account import Facade
import structlog


structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)
    ]
)


def test_post_v1_account():
    api = Facade(host='http://localhost:5051')

    login = 'logintest12'
    email = 'logintest12@test'
    password = 'logintest12'
    orm = OrmDatabase(user='postgres', password='admin', host='localhost', database='dm3.5')
    orm.delete_user_by_login(login=login)
    dataset = orm.get_user_by_login(login=login)
    assert len(dataset) == 0

    api.mailhog.delete_all_messages()

    response = api.account.register_new_user(
        login=login,
        email=email,
        password=password
    )
    dataset = orm.get_user_by_login(login=login)
    for row in dataset:
        assert_that(row, has_properties(
            {
                'Login': login,
                'Activated': False
            }
        ))
        # assert row.Login == login, f'User {login} not registered'
        # assert row.Activated is False, f'User {login} was activated'

    api.account.activate_registered_user(login=login)
    dataset = orm.get_user_by_login(login=login)
    time.sleep(2)
    for row in dataset:
        assert row.Activated is True, f'User {login} not activated'

    api.login.login_user(
        login=login,
        password=password
    )
    orm.db.close_connection()
