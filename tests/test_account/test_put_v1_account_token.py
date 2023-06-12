import structlog
from dm_api_account.models import UserRole
from hamcrest import assert_that, has_properties
from data.post_v1_account import PostV1AccountData as data_user

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)
    ]
)

login = data_user.login
password = data_user.password
email = data_user.email


def test_put_v1_account_token(dm_api_facade, assertions, dm_orm):

    dm_orm.delete_user_by_login(login=login)
    dm_api_facade.mailhog.delete_all_messages()

    dm_api_facade.account.register_new_user(login=login, email=email, password=password)
    assertions.check_user_was_created(login=login)
    token = dm_api_facade.mailhog.get_token_by_login(login=login)
    response = dm_api_facade.account_api.activate(token=token)

    assert_that(response.resource, has_properties(
        {
            "login": login,
            "roles": [
                UserRole('Guest'),
                UserRole('Player')
            ]
        }
    ))
