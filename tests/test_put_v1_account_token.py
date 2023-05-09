import structlog
from dm_api_account.models.user_envelope_model import UserRole
from services.dm_api_account import DmApiAccount
from hamcrest import assert_that, has_properties

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)
    ]
)


def test_put_v1_account_token():
    api = DmApiAccount(host='http://localhost:5051')
    response = api.account.put_v1_account_token(token='04efc017-32a9-42c7-9389-89f8c23fcccc')
    assert_that(response.resource, has_properties(
        {
            "login": "logintest5",
            "roles": [UserRole.GUEST, UserRole.PLAYER]
        }
    ))
