from easy_equities_client import constants
from easy_equities_client.instruments.clients import InstrumentsClient
from easy_equities_client.instruments.types import Period


class TestInstrumentsClient:
    def test_historical_prices(
        self, base_platform_url, requests_mock, mocker, historical_prices
    ):
        period = Period.ONE_MONTH
        contract_code = "EQU.ZA.SYGJP"
        url = f"{base_platform_url}{constants.PLATFORM_GET_CHART_DATA_PATH}?period={period.value}&code={contract_code}"
        requests_mock.get(url, status_code=200, json=historical_prices)
        client = InstrumentsClient(base_platform_url)
        assert (
            client.historical_prices("EQU.ZA.SYGJP", Period.ONE_MONTH)
            == historical_prices
        )
