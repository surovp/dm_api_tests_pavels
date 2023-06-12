from dm_api_account.apis.account_api import AccountApi
from dm_api_account.apis.login_api import LoginApi
from generic.helpers.account import Account
from generic.helpers.login import Login
from dm_api_account import Configuration, ApiClient


class Facade:
    def __init__(self, host, mailhog=None):
        with ApiClient(configuration=Configuration(host=host)) as api_client:
            self.account_api = AccountApi(api_client)
            self.login_api = LoginApi(api_client)
        self.mailhog = mailhog
        self.account = Account(self)
        self.login = Login(self)

    def set_headers(self, headers):
        self.account.set_headers(headers)
        self.login.set_headers(headers)


