from services.dm_api_account import Facade


def test_get_v1_account():
    api = Facade(host='http://localhost:5051')
    token = api.login.get_auth_token(
        login='logintest14',
        password='logintest14'
    )
    print(token)
    #api.account_api.get_v1_account()
