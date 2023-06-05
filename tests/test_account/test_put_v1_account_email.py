from services.dm_api_account import Facade


def test_put_v1_account_email():
    api = Facade(host='http://localhost:5051')
    json = {
        "login": "<string>",
        "password": "<string>",
        "email": "<string>"
    }
    response = api.account_api.put_v1_account_email(
        json=json
    )
    print(response)
