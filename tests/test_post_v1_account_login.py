def test_post_v1_account_login(dm_api_facade):
    dm_api_facade.login.login_user(
        login='logintest12',
        password='logintest12',
        remember_me=True
    )

