import json

from easy_equities_client import constants
from easy_equities_client.accounts.clients import AccountsClient
from easy_equities_client.accounts.types import Account


class TestAccountsClient:
    def test_get_account_overview_page(self, base_platform_url, requests_mock):
        url = base_platform_url + constants.PLATFORM_ACCOUNT_OVERVIEW_PATH
        text = b"My Investments"
        requests_mock.get(url, status_code=200, content=text)
        client = AccountsClient(base_platform_url)
        assert client._get_account_overview_page() == str(text)

    def test_list(self, mocker):
        get_account_overview_page_mock = mocker.patch(
            'easy_equities_client.accounts.clients.AccountsClient._get_account_overview_page'
        )
        account_overview_parser_mock = mocker.patch(
            'easy_equities_client.accounts.clients.AccountOverviewParser'
        )
        accounts = [Account('1', 'Test', '1000')]
        get_account_overview_page_mock.return_value = None
        account_overview_parser_mock.return_value.extract_accounts.return_value = (
            accounts
        )
        client = AccountsClient()
        assert client.list() == accounts

    def test_account_valuations(
        self, base_platform_url, requests_mock, mocker, valuations
    ):
        mocker.patch(
            'easy_equities_client.accounts.clients.AccountsClient._switch_account'
        )
        url = base_platform_url + constants.PLATFORM_ACCOUNT_VALUATIONS_PATH
        requests_mock.get(url, status_code=200, json=valuations)
        client = AccountsClient(base_platform_url)
        assert client.valuations('1') == json.loads(valuations)

    def test_account_transactions(
        self, base_platform_url, requests_mock, mocker, account_transactions
    ):
        mocker.patch(
            'easy_equities_client.accounts.clients.AccountsClient._switch_account'
        )
        url = base_platform_url + constants.PLATFORM_TRANSACTIONS_PATH
        requests_mock.get(url, status_code=200, json=account_transactions)
        client = AccountsClient(base_platform_url)
        assert client.transactions('1') == account_transactions

    def test_account_holdings(
        self, base_platform_url, requests_mock, mocker, account_holdings_page
    ):
        mocker.patch(
            'easy_equities_client.accounts.clients.AccountsClient._switch_account'
        )
        url = base_platform_url + constants.PLATFORM_HOLDINGS_PATH
        requests_mock.get(
            url, status_code=200, content=str.encode(account_holdings_page)
        )
        client = AccountsClient(base_platform_url)
        holdings = client.holdings('1')
        expected_data = [
            {
                "name": "SYGNIA ITRIX EUROSTOXX50",
                "purchase_value": "R2 490.68",
                "current_value": "R2 605.45",
                "current_price": "R64.08",
                "img": "https://resources.easyequities.co.za/logos/TFSA.SYGEU.png",
                "view_url": "/AccountOverview/GetInstrumentDetailAction/?IsinCode=ZAE000249512",
                "isin": "ZAE000249512",
                "contract_code": "TFSA.SYGEU",
            },
            {
                "name": "SYGNIA ITRIX MSCI JAPAN",
                "purchase_value": "R2 527.83",
                "current_value": "R2 621.85",
                "current_price": "R15.81",
                "img": "https://resources.easyequities.co.za/logos/TFSA.SYGJP.png",
                "view_url": "/AccountOverview/GetInstrumentDetailAction/?IsinCode=ZAE000249538",
                "isin": "ZAE000249538",
                "contract_code": "TFSA.SYGJP",
            },
        ]

        assert sorted(holdings, key=lambda x: x['name']) == expected_data
