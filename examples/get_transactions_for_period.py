import json
import os
from datetime import date, timedelta

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
transactions = []
for account in accounts:
    print(f"Getting transactions for account {account.id}")
    start_date = date(2021, 11, 1)
    for _ in range(1):
        end_date = start_date + timedelta(days=28 * 3)
        print(f"Start: {start_date}, End: {end_date}")
        transactions += client.accounts.transactions_for_period(
            account.id, start_date, end_date
        )
        start_date = end_date + timedelta(days=1)
    break
print(json.dumps(transactions, indent=4))

with open("transactions_examples.json", 'w') as f:
    f.write(json.dumps(transactions, indent=4))
