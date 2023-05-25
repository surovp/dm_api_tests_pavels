import pytest
import structlog
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
