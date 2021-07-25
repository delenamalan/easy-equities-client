from easy_equities_client import constants
from easy_equities_client.instruments.types import HistoricalPrices, Period
from easy_equities_client.types import Client


class InstrumentsClient(Client):
    def historical_prices(self, contract_code: str, period: Period) -> HistoricalPrices:
        """
        Fetch the historical prices of a given instrument.

        @param contract_code: Contract code for the instrument, e.g. "EQU.ZA.SYGJP"
        @param period: Time period for which to fetch the historical data.
        """
        response = self.session.get(
            self._url(
                constants.PLATFORM_GET_CHART_DATA_PATH,
                f"code={contract_code}&period={period.value}",
            )
        )
        assert (
            response.status_code == 200
        ), "Chart data request should return 200 status code"
        response.raise_for_status()
        return response.json()
