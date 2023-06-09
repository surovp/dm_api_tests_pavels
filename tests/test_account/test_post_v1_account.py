from data.post_v1_account import PostV1AccountData as user_data
from hamcrest import assert_that, has_entries
from string import ascii_letters, digits
from collections import namedtuple
import random
import pytest
import allure


def random_string():
    symbols = ascii_letters + digits
    string = ''
    for _ in range(10):
        string += random.choice(symbols)
    return string


def random_short_password():
    string = ''
    for _ in range(random.randint(1, 5)):
        string += random.choice(ascii_letters + digits)
    return string


def random_long_password():
    string = ''
    for _ in range(random.randint(6, 100)):
        string += random.choice(ascii_letters + digits)
    return string


@allure.suite("Тесты на проверку метода POST{host}/v1/account")
@allure.sub_suite('Позитивные тесты')
class TestsPostV1Account:

    @allure.step("Подготовка тестового пользователя")
    @pytest.fixture
    def prepare_user(self, dm_api_facade, dm_orm):
        data = namedtuple('user', 'login, email, password')
        user = data(
            login=user_data.login,
            email=user_data.email,
            password=user_data.password
        )
        dm_orm.delete_user_by_login(login=user.login)
        dataset = dm_orm.get_user_by_login(login=user.login)
        assert len(dataset) == 0
        dm_api_facade.mailhog.delete_all_messages()

        return user

    @allure.title('Проверка регистрации и активации пользователя')
    def test_register_and_activate_user(self, dm_api_facade, dm_orm, prepare_user, assertions):
        """
        Тест проверяет создание и активацию пользователя в БД
        """
        login = prepare_user.login
        email = prepare_user.email
        password = prepare_user.password

        dm_api_facade.account.register_new_user(login=login, email=email, password=password, status_code=201)
        assertions.check_user_was_created(login=login)
        dm_api_facade.account.activate_registered_user(login=login)
        assertions.check_user_was_activated(login=login)
        dm_api_facade.login.login_user(login=login, password=password)

    @pytest.mark.parametrize('login', [random_string() for _ in range(3)])
    @pytest.mark.parametrize('email', [random_string() + '@' + random_string() + '.ru' for _ in range(3)])
    @pytest.mark.parametrize('password', [random_string() for _ in range(3)])
    def test_post_v1_account_with_random_datas(self, dm_api_facade, dm_orm, login, email, password, assertions):
        dm_orm.delete_user_by_login(login=login)
        dm_api_facade.mailhog.delete_all_messages()
        dm_api_facade.account.register_new_user(login=login, email=email, password=password, status_code=201)
        dm_orm.get_user_by_login(login=login)
        assertions.check_user_was_created(login=login)
        dm_api_facade.account.activate_registered_user(login=login)
        dm_orm.get_user_by_login(login=login)
        assertions.check_user_was_activated(login=login)
        dm_api_facade.login.login_user(login=login, password=password)


@pytest.mark.parametrize('login, email, password', [
    ('logintest12', 'logintest12@test.com', 'logintest12'),
    ('87589', '87589@123.com', '87589'),
    ('qwerty124#$%', 'qwe123!$%@mail.com', 'qwe123!$%')
])
def test_post_v1_account_with_datas(dm_api_facade, dm_orm, login, email, password, assertions):
    dm_orm.delete_user_by_login(login=login)
    dm_api_facade.mailhog.delete_all_messages()
    dm_api_facade.account.register_new_user(login=login, email=email, password=password, status_code=201)
    dm_orm.get_user_by_login(login=login)
    assertions.check_user_was_created(login=login)
    dm_api_facade.account.activate_registered_user(login=login)
    dm_orm.get_user_by_login(login=login)
    assertions.check_user_was_activated(login=login)
    dm_api_facade.login.login_user(login=login, password=password)


@pytest.mark.parametrize('login', ['logintest16', '2156236', '@#$%^&'])
@pytest.mark.parametrize('email', ['logintest16@test.ru', '2156236@mail.com', '@#$%^&@gwe.weh'])
@pytest.mark.parametrize('password', ['logintest16', '2156236', '@#$%^&'])
def test_post_v1_account_with_datas_pairwise(dm_api_facade, dm_orm, login, email, password, assertions):
    dm_orm.delete_user_by_login(login=login)
    dm_api_facade.mailhog.delete_all_messages()
    dm_api_facade.account.register_new_user(login=login, email=email, password=password, status_code=201)
    dm_orm.get_user_by_login(login=login)
    assertions.check_user_was_created(login=login)
    dm_api_facade.account.activate_registered_user(login=login)
    dm_orm.get_user_by_login(login=login)
    assertions.check_user_was_activated(login=login)
    dm_api_facade.login.login_user(login=login, password=password)


@pytest.mark.parametrize('login, password, email, check_password_error, status_code', [
    ('logintest20', random_long_password(), 'logintest20@test.com', '', 201),
    ('logintest20', random_short_password(), 'logintest20@test.com', 'Short', 400)
])
def test_post_v1_account_password(
        dm_api_facade,
        dm_orm,
        login,
        email,
        password,
        status_code,
        check_password_error,
        assertions
):
    dm_orm.delete_user_by_login(login=login)
    dm_api_facade.mailhog.delete_all_messages()
    response = dm_api_facade.account.register_new_user(
        login=login,
        email=email,
        password=password,
        status_code=status_code
    )
    if status_code != 201 and len(password) <= 5:
        assert_that(response.json()['errors'], has_entries(
            {
                "Password": [check_password_error]
            }
        ))
    else:
        assertions.check_user_was_created(login=login)
        dm_api_facade.account.activate_registered_user(login=login)
        dm_orm.get_user_by_login(login=login)
        assertions.check_user_was_activated(login=login)
        dm_api_facade.login.login_user(login=login, password=password)


@pytest.mark.parametrize('login, password, email, check_login_error, status_code', [
    ('logintest20', random_long_password(), 'logintest20@test.com', '', 201),
    ('logintest20', random_long_password(), 'logintest20@test.com', 'Taken', 400)
])
def test_post_v1_account_login(
        dm_api_facade,
        dm_orm,
        login,
        email,
        password,
        status_code,
        check_login_error,
        assertions
):
    response = dm_api_facade.account.register_new_user(
        login=login,
        email=email,
        password=password,
        status_code=status_code
    )
    if status_code != 201:
        assert_that(response.json()['errors'], has_entries(
            {
                "Login": [check_login_error]
            }
        ))
    else:
        assertions.check_user_was_created(login=login)
        dm_api_facade.account.activate_registered_user(login=login)
        dm_orm.get_user_by_login(login=login)
        assertions.check_user_was_activated(login=login)
        dm_api_facade.login.login_user(login=login, password=password)


@pytest.mark.parametrize('login, password, email, check_email_error, status_code', [
    ('logintest21', random_long_password(), 'logintest21@test.com', '', 201),
    ('logintest22', random_long_password(), 'logintest21@test.com', 'Taken', 400)
])
def test_post_v1_account_email(
        dm_api_facade,
        dm_orm,
        login,
        email,
        password,
        status_code,
        check_email_error,
        assertions
):
    response = dm_api_facade.account.register_new_user(
        login=login,
        email=email,
        password=password,
        status_code=status_code
    )
    if status_code != 201:
        assert_that(response.json()['errors'], has_entries(
            {
                "Email": [check_email_error]
            }
        ))
    else:
        assertions.check_user_was_created(login=login)
        dm_api_facade.account.activate_registered_user(login=login)
        dm_orm.get_user_by_login(login=login)
        assertions.check_user_was_activated(login=login)
        dm_api_facade.login.login_user(login=login, password=password)
