import json

import pytest

from easy_equities_client import constants
from easy_equities_client.clients import (
    EasyEquitiesClient,
    PlatformClient,
    SatrixClient,
)


@pytest.fixture
def base_platform_url():
    return "https://platform.test.io"


@pytest.fixture
def mock_success_login_response(requests_mock):
    def _mock_success_login_response(base_url):
        url = base_url + constants.PLATFORM_SIGN_IN_PATH
        requests_mock.post(url, status_code=302)

    return _mock_success_login_response


@pytest.fixture
def platform_client(base_platform_url):
    return PlatformClient(base_platform_url)


@pytest.fixture
def easy_equities_client():
    return EasyEquitiesClient()


@pytest.fixture
def satrix_client():
    return SatrixClient()


@pytest.fixture
def account_overview_page():
    with open('./tests/data/account-overview.html', 'r') as f:
        return f.read()


@pytest.fixture
def account_holdings_page():
    with open('./tests/data/account-holdings.html', 'r') as f:
        return f.read()


@pytest.fixture
def valuations():
    with open('./tests/data/account-valuations.json', 'r') as f:
        return f.read()


@pytest.fixture
def account_transactions():
    with open('./tests/data/account-transactions.json', 'r') as f:
        return json.loads(f.read())
