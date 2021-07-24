import json
from typing import List

from easy_equities_client import constants
from easy_equities_client.accounts.parsers import (
    AccountHoldingsParser,
    AccountOverviewParser,
)
from easy_equities_client.accounts.types import Account, Holding, Transaction, Valuation
from easy_equities_client.types import Client


class AccountsClient(Client):
    def _get_account_overview_page(self) -> str:
        response = self.session.get(self._url(constants.PLATFORM_ACCOUNT_OVERVIEW_PATH))
        assert (
            response.status_code == 200
        ), "Account overview page should return 200 status code"
        assert "My Investments" in str(response.content)
        return str(response.content)

    def list(self) -> List[Account]:
        page = self._get_account_overview_page()
        parser = AccountOverviewParser(page)
        return parser.extract_accounts()

    def _switch_account(self, account_id: str) -> None:
        """
        Switch the currently selected account.
        """
        data = {'trustAccountId': account_id}
        response = self.session.post(
            self._url(constants.PLATFORM_UPDATE_CURRENCY_PATH), data
        )
        response.raise_for_status()
        assert (
            response.status_code == 200
        ), "Update currency request should return 200 status code"

    def valuations(self, account_id: str) -> Valuation:
        self._switch_account(account_id)
        response = self.session.get(
            self._url(constants.PLATFORM_ACCOUNT_VALUATIONS_PATH)
        )
        response.raise_for_status()
        return json.loads(response.json())

    def transactions(self, account_id) -> List[Transaction]:
        self._switch_account(account_id)
        response = self.session.get(self._url(constants.PLATFORM_TRANSACTIONS_PATH))
        response.raise_for_status()
        return response.json()

    def holdings(self, account_id) -> List[Holding]:
        self._switch_account(account_id)
        response = self.session.get(self._url(constants.PLATFORM_HOLDINGS_PATH))
        response.raise_for_status()
        parser = AccountHoldingsParser(response.content)
        return parser.extract_holdings()
