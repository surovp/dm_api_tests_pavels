import pytest
import structlog
from vyper import v
from pathlib import Path
from services.dm_api_account import Facade
from generic.helpers.mailhog import MailHogApi
from generic.helpers.orm_db import OrmDatabase
from generic.assertions.post_v1_account import AssertionsPostV1Account


structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)
    ]
)

options = {
    'service.dm_api_account',
    'service.mailhog',
    'database.dm3_5.host'
}


@pytest.fixture()
def mailhog():
    return MailHogApi(host=v.get('service.mailhog'))


@pytest.fixture()
def dm_api_facade(mailhog):
    return Facade(
        host=v.get('service.dm_api_account'),
        mailhog=mailhog
    )


@pytest.fixture()
def dm_orm():
    connect = None
    if connect is None:
        connect = OrmDatabase(
            user=v.get('database.dm3_5.user'),
            password=v.get('database.dm3_5.password'),
            host=v.get('database.dm3_5.host'),
            database=v.get('database.dm3_5.database')
        )
    yield connect
    connect.db.close_connection()


@pytest.fixture()
def assertions(dm_orm):
    return AssertionsPostV1Account(dm_orm)


@pytest.fixture(autouse=True)
def set_config(request):
    config = Path(__file__).parent.joinpath('config')
    config_name = request.config.getoption('--env') #в config_name передаем из виртуального окружения --env наш файл stage
    v.set_config_name(config_name)
    v.add_config_path(config)
    v.read_in_config()
    for option in options:
        v.set(option, request.config.getoption(f'--{option}'))


def pytest_addoption(parser):
    parser.addoption('--env', action='store', default='stage') #добавляем в виртуальное окружение "env" наш файл stage
    for option in options:
        parser.addoption(f'--{option}', action='store', default=None) #считываем переменные из options для смены урл в ходе теста

