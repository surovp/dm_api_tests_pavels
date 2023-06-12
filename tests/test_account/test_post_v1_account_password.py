from data.post_v1_account_password import PostV1AccountPasswordResetData as data_user


def test_post_v1_account_password(dm_api_facade):
    login = data_user.login
    email = data_user.email

    dm_api_facade.account.reset_password_user(login=login, email=email)
