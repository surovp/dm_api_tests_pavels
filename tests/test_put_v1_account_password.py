from services.dm_api_account import Facade


def test_put_v1_account_password():
    api = Facade(host='http://localhost:5051')
    json = {
        "login": "<string>",
        "token": "<uuid>",
        "oldPassword": "<string>",
        "newPassword": "<string>"
    }
    response = api.account_api.put_v1_account_password(
        json=json
    )
    print(response)
