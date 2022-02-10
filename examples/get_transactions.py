import json
import os

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
    transactions += client.accounts.transactions(account.id)
print(json.dumps(transactions, indent=4))
