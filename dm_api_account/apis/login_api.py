from requests import Response, session
from ..models import *
from ..utilities import validate_request_json, validate_status_code


class LoginApi:

    def __init__(self, host, headers=None):
        self.host = host
        self.session = session()
        if headers:
            self.session.headers = headers

    def post_v1_account_login(self, json: LoginCredentials, status_code: int, **kwargs) -> Response | UserEnvelope:
        """
        Authenticate via credentials
        :param json login_credentials_model
        :return:
        """
        response = self.session.post(
            url=f"{self.host}/v1/account/login",
            json=validate_request_json(json),
            **kwargs
        )
        validate_status_code(response, status_code)
        if response.status_code == 200:
            return UserEnvelope(**response.json())
        return response

    def delete_v1_account_login(self, status_code: int, **kwargs) -> Response:
        """
        Logout as current user
        :return:
        """
        response = self.session.delete(
            url=f"{self.host}/v1/account/login",
            **kwargs
        )
        validate_status_code(response, status_code)
        return response

    def delete_v1_account_login_all(self, status_code: int, **kwargs) -> Response:
        """
        Logout from every device
        :return:
        """
        response = self.session.delete(
            url=f"{self.host}/v1/account/login/all",
            **kwargs
        )
        validate_status_code(response, status_code)
        return response
