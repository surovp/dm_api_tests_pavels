from hamcrest import assert_that, has_entries
import pytest
import time


def test_post_v1_account(dm_api_facade, dm_orm, prepare_user):
    login = prepare_user.login
    email = prepare_user.email
    password = prepare_user.password

    response = dm_api_facade.account.register_new_user(
        login=login,
        email=email,
        password=password
    )
    dataset = dm_orm.get_user_by_login(login=login)
    for row in dataset:
        assert_that(row, has_entries(
            {
                'Login': login,
                'Activated': False
            }
        ))

    dm_api_facade.account.activate_registered_user(login=login)
    dataset = dm_orm.get_user_by_login(login=login)
    time.sleep(2)
    for row in dataset:
        assert row.Activated is True, f'User {login} not activated'

    dm_api_facade.login.login_user(
        login=login,
        password=password
    )


@pytest.mark.parametrize('login, email, password', [
    ('logintest12', 'logintest12@test.com', 'logintest12'),
    ('87589', '87589@123.com', '87589'),
    ('qwerty124#$%', 'qwe123!$%@mail.com', 'qwe123!$%')
])
def test_post_v1_account_with_datas(dm_api_facade, dm_orm, login, email, password):
    dm_orm.delete_user_by_login(login=login)
    dm_api_facade.mailhog.delete_all_messages()
    response = dm_api_facade.account.register_new_user(
        login=login,
        email=email,
        password=password
    )
    dataset = dm_orm.get_user_by_login(login=login)
    for row in dataset:
        assert_that(row, has_entries(
            {
                'Login': login,
                'Activated': False
            }
        ))

    dm_api_facade.account.activate_registered_user(login=login)
    dataset = dm_orm.get_user_by_login(login=login)
    time.sleep(2)
    for row in dataset:
        assert row.Activated is True, f'User {login} not activated'

    dm_api_facade.login.login_user(
        login=login,
        password=password
    )
