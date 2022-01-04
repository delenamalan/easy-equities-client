import json
from datetime import date

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
        self,
        base_platform_url,
        requests_mock,
        mocker,
        account_holdings_page,
        holding_details_page,
    ):
        mocker.patch(
            'easy_equities_client.accounts.clients.AccountsClient._switch_account'
        )
        # Mock holdings
        requests_mock.get(
            base_platform_url + constants.PLATFORM_HOLDINGS_PATH,
            status_code=200,
            content=str.encode(account_holdings_page),
        )
        # Mock holding stocks
        requests_mock.get(
            base_platform_url
            + "/AccountOverview/GetInstrumentDetailAction/?IsinCode=ZAE000249512",
            status_code=200,
            content=str.encode(holding_details_page),
        )
        requests_mock.get(
            base_platform_url
            + "/AccountOverview/GetInstrumentDetailAction/?IsinCode=ZAE000249538",
            status_code=200,
            content=str.encode(holding_details_page),
        )

        client = AccountsClient(base_platform_url)
        holdings = client.holdings('1', include_shares=True)
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
                "shares": "200.0123",
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
                "shares": "200.0123",
            },
        ]

        assert sorted(holdings, key=lambda x: x['name']) == expected_data

    def test_account_transactions_for_period(
        self,
        base_platform_url,
        requests_mock,
        mocker,
        account_transactions_page1,
        account_transactions_empty,
    ):
        mocker.patch(
            'easy_equities_client.accounts.clients.AccountsClient._switch_account'
        )
        start_date = date(2021, 8, 1)
        end_date = date(2021, 8, 31)
        page1_url = (
            base_platform_url
            + constants.PLATFORM_TRANSACTIONS_SEARCH_PATH_NEXT_PAGE.format(
                start_date=f"{start_date.month}/{start_date.day}/{start_date.year}",
                end_date=f"{end_date.month}/{end_date.day}/{end_date.year}",
                page_number=1,
            )
        )
        page2_url = (
            base_platform_url
            + constants.PLATFORM_TRANSACTIONS_SEARCH_PATH_NEXT_PAGE.format(
                start_date=f"{start_date.month}/{start_date.day}/{start_date.year}",
                end_date=f"{end_date.month}/{end_date.day}/{end_date.year}",
                page_number=2,
            )
        )
        requests_mock.get(
            page1_url,
            status_code=200,
            content=str.encode(account_transactions_page1),
        )
        requests_mock.get(
            page2_url, status_code=200, content=str.encode(account_transactions_empty)
        )
        expected_output = [
            {
                "date": "2021-08-31",
                "description": "Account Balance Carried Forward",
                "amount": "R63.55",
                "currency": "R",
                "value": 63.55,
            },
            {
                "date": "2021-08-16",
                "description": "Schroder European Real Estate Inv Trust PLC-Foreign Dividends @31.49625",
                "amount": "R52.21",
                "currency": "R",
                "value": 52.21,
            },
            {
                "date": "2021-08-16",
                "description": "Dividend Withholding Tax SCD-Dividend Withholding Tax @20%",
                "amount": "-R10.44",
                "currency": "R",
                "value": -10.44,
            },
            {
                "date": "2021-08-01",
                "description": "Interest",
                "amount": "R0.03",
                "currency": "R",
                "value": 0.03,
            },
            {
                "date": "2021-08-01",
                "description": "Cash Management Fee",
                "amount": "-R0.01",
                "currency": "R",
                "value": -0.01,
            },
            {
                "date": "2021-08-01",
                "description": "VAT on Cash Management Fee",
                "amount": "R0.00",
                "currency": "R",
                "value": 0,
            },
            {
                "date": "2021-08-01",
                "description": "Account Balance Brought Forward",
                "amount": "R21.77",
                "currency": "R",
                "value": 21.77,
            },
        ]
        client = AccountsClient(base_platform_url)
        assert (
            client.transactions_for_period('1', start_date, end_date) == expected_output
        )
