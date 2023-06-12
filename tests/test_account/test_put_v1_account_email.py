from data.put_v1_account_email import PutV1AccountEmailData as data_user


def test_put_v1_account_email(dm_api_facade):
    login = data_user.login
    password = data_user.password
    email = data_user.email

    dm_api_facade.account.change_email_user(
        login=login,
        password=password,
        email=email
    )

