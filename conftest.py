import pytest
import structlog
from collections import namedtuple
from services.dm_api_account import Facade
from generic.helpers.mailhog import MailHogApi
from generic.helpers.orm_db import OrmDatabase


structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)
    ]
)


@pytest.fixture()
def mailhog():
    return MailHogApi(host='http://localhost:5025')


@pytest.fixture()
def dm_api_facade(mailhog):
    return Facade(host='http://localhost:5051', mailhog=mailhog)


@pytest.fixture()
def dm_orm():
    orm = OrmDatabase(user='postgres', password='admin', host='localhost', database='dm3.5')
    yield orm
    orm.db.close_connection()


@pytest.fixture
def prepare_user(dm_api_facade, dm_orm):
    data = namedtuple('user', 'login, email, password')
    user = data(
        login='logintest12',
        email='logintest12@test',
        password='logintest12'
    )
    dm_orm.delete_user_by_login(login=user.login)
    dataset = dm_orm.get_user_by_login(login=user.login)
    assert len(dataset) == 0
    dm_api_facade.mailhog.delete_all_messages()

    return user
