import json
import time

from requests import Response, session
from restclient.restclient import RestClient


class MailHogApi:
    def __init__(self, host='http://localhost:5025'):
        self.host = host
        self.client = RestClient(host=host)

    def get_api_v2_messages(self, limit: int = 50) -> Response:
        """
        Get messages by limit
        :param limit:
        :return:
        """
        response = self.client.get(
            path=f"/api/v2/messages",
            params={
                'limit': limit
            }
        )
        return response

    def get_token_from_last_email(self) -> str:
        """
        Get user activation user token from last email
        json.loads - преобразовывает строку в словарь
        :return:
        """
        emails = self.get_api_v2_messages(limit=1).json()
        token_url = json.loads(emails['items'][0]['Content']['Body'])['ConfirmationLinkUrl']
        token = token_url.split('/')[-1]
        return token

    def get_token_by_login(self, login: str, attempt=5):
        if attempt == 0:
            raise AssertionError(f'Не удалось получить письмо логина {login}')
        emails = self.get_api_v2_messages(limit=100).json()['items']
        for email in emails:
            user_data = json.loads(email['Content']['Body'])
            if login == user_data.get('Login'):
                token = user_data['ConfirmationLinkUrl'].split('/')[-1]
                print(token)
                return token
        time.sleep(2)
        print('Попытка получить письмо')
        return self.get_token_by_login(login=login, attempt=attempt-1)
