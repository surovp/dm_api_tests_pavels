from dm_api_account.models import Registration


class Account:
    def __init__(self, facade):
        from services.dm_api_account import Facade
        self.facade: Facade = facade

    def set_headers(self, headers):
        self.facade.account_api.api_client.select_header_accept(headers)

    def register_new_user(self, login: str, email: str, password: str):
        response = self.facade.account_api.register(
            registration=Registration(
                login=login,
                email=email,
                password=password,
            ),
        )
        return response

    def activate_registered_user(self, login: str):
        token = self.facade.mailhog.get_token_by_login(login=login)
        response = self.facade.account_api.activate(
            token=token
        )
        print('Получили такой токен:', token)
        return response

    def get_current_user_info(self, token):
        response = self.facade.account_api.get_current(x_dm_auth_token=token)
        return response


