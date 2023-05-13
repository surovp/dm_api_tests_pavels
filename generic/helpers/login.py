from dm_api_account.models import LoginCredentials


class Login:
    def __init__(self, facade):
        self.facade = facade

    def login_user(self, login: str, password: str, remember_me: bool = True):
        response = self.facade.login_api.post_v1_account_login(
            json=LoginCredentials(
                login=login,
                password=password,
                rememberMe=remember_me
            )
        )
        return response

    def get_auth_token(self, login: str, password: str, remember_me: bool = True):
        response = self.login_user(
            login=login,
            password=password,
            remember_me=remember_me)
        token = {'X-DM-Auth-Token': response.headers['X-DM-Auth-Token']}
        return token
