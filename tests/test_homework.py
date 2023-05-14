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
        password=password
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
        password=password
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

