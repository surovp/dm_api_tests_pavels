

def test_get_v1_account(dm_api_facade):
    token = dm_api_facade.login.get_auth_token(
        login='logintest12',
        password='123456',
        remember_me=True
    )
    dm_api_facade.set_headers(headers=token)
    dm_api_facade.account.get_current_user_info(token=token)
    dm_api_facade.login.logout_user()

