from data.put_v1_account_password import PutV1AccountPasswordData as data_user


def test_put_v1_account_password(dm_api_facade, assertions, dm_orm):

    login = data_user.login
    email = data_user.email
    password = data_user.password
    old_password = data_user.old_password
    new_password = data_user.new_password

    dm_orm.delete_user_by_login(login=login)
    dm_api_facade.mailhog.delete_all_messages()
    dm_api_facade.account.register_new_user(login=login, email=email, password=password)
    assertions.check_user_was_created(login=login)
    dm_api_facade.account.activate_registered_user(login=login)
    assertions.check_user_was_activated(login=login)

    token = dm_api_facade.mailhog.get_token_by_login(login=login)
    dm_api_facade.account.change_password_user(
        login=login,
        token=token,
        old_password=old_password,
        new_password=new_password
    )
