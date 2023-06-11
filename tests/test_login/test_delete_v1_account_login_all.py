from data.delete_v1_account_login import DeleteV1AccountLoginData

login = DeleteV1AccountLoginData.login
password = DeleteV1AccountLoginData.password


def test_delete_v1_account_login_all(dm_api_facade):
    x_dm_auth_token = dm_api_facade.login.get_auth_token(
        login=login,
        password=password,
    )
    response = dm_api_facade.login.logout_user_from_all_devices(x_dm_auth_token=x_dm_auth_token)
    print(response)
