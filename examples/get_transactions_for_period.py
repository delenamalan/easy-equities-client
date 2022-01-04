import json
import os
from datetime import date

from easy_equities_client.clients import (
    EasyEquitiesClient,
    PlatformClient,
    SatrixClient,
)

platform = 'easyequities'
username = os.environ['EE_USERNAME']
password = os.environ['EE_PASSWORD']

client: PlatformClient = (
    EasyEquitiesClient() if platform == 'easyequities' else SatrixClient()
)
client.login(username=username, password=password)

accounts = client.accounts.list()
account = accounts[0]

transactions = client.accounts.transactions_for_period(
    account.id, date(2021, 8, 1), date(2021, 8, 31)
)
print(json.dumps(transactions, indent=4))
