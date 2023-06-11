from generic.assertions.response_checker import check_status_code_http
from data.post_v1_account import PostV1AccountData as user_data
from data.post_v1_account import random_datas
from collections import namedtuple
import pytest
import allure


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

        dm_api_facade.account.register_new_user(login=login, email=email, password=password)
        assertions.check_user_was_created(login=login)
        dm_api_facade.account.activate_registered_user(login=login)
        assertions.check_user_was_activated(login=login)
        dm_api_facade.login.login_user(login=login, password=password)

    @pytest.mark.parametrize('login, email, password, status_code, check', random_datas)
    def test_post_v1_account_with_random_datas(
            self,
            dm_api_facade,
            dm_orm,
            login,
            email,
            password,
            assertions,
            status_code,
            check):
        dm_orm.delete_user_by_login(login=login)
        dm_api_facade.mailhog.delete_all_messages()
        """
        если статус код отличный от 200, то в рамках контекстного менеджера выполнится проверка сообщения 
        и статус кода и тест пройдет. В случае если, метод выполнится успешно (статус код 2хх), 
        мы зайдем в блок if и проведем дальнейшие проверки позитивного сценария.
        """
        with check_status_code_http(expected_status_code=status_code, expected_result=check):
            dm_api_facade.account.register_new_user(login=login, email=email, password=password)
        if status_code == 200:
            dm_orm.get_user_by_login(login=login)
            assertions.check_user_was_created(login=login)
            dm_api_facade.account.activate_registered_user(login=login)
            dm_orm.get_user_by_login(login=login)
            assertions.check_user_was_activated(login=login)
            dm_api_facade.login.login_user(login=login, password=password)
