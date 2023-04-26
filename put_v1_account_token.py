import requests


def put_v1_account_token():
    """
    Activate registered user
    :return:
    """
    token = '124215'
    url = f"http://localhost:5051/v1/account/{token}"

    payload = {}
    headers = {
        'X-Dm-Auth-Token': '<string>',
        'X-Dm-Bb-Render-Mode': '<string>',
        'Accept': 'text/plain'
    }

    response = requests.request(
        method="PUT",
        url=url,
        headers=headers,
        json=payload
    )
    return response
