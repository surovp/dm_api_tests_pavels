import allure
from dm_api_account.models import LoginCredentials


class Login:
    def __init__(self, facade):
        from services.dm_api_account import Facade
        self.facade: Facade = facade

    def set_headers(self, headers):
        self.facade.login_api.api_client.select_header_accept(headers)

    def login_user(self, login: str, password: str, remember_me: bool = True):
        with allure.step("Авторизация пользователя"):
            response = self.facade.login_api.v1_account_login_post(
                _return_http_data_only=False,
                login_credentials=LoginCredentials(
                    login=login,
                    password=password,
                    remember_me=remember_me
                )
            )
        return response

    def get_auth_token(self, login: str, password: str, remember_me: bool = True):
        response = self.login_user(
            login=login,
            password=password,
            remember_me=remember_me)
        token = response[2]['X-DM-Auth-Token']
        print(response)
        return token

    def logout_user(self, x_dm_auth_token):
        response = self.facade.login_api.v1_account_login_delete(x_dm_auth_token=x_dm_auth_token)
        return response

    def logout_user_from_all_devices(self, x_dm_auth_token):
        response = self.facade.login_api.v1_account_login_all_delete(x_dm_auth_token=x_dm_auth_token)
        return response

