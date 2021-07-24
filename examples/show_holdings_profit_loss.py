"""
Calculate the total profit/loss for each of your accounts.

Requires the colorama package.
"""
from sys import argv

import colorama
from colorama import Fore

from easy_equities_client.clients import (
    EasyEquitiesClient,
    PlatformClient,
    SatrixClient,
)

colorama.init(autoreset=True)

if len(argv) != 4:
    print(
        "Usage:\npython show_holdings_profit_loss.py <platform:satrix/easyequities> <username> <password>"
    )
platform = argv[1]
username = argv[2]
password = argv[3]

client: PlatformClient = (
    EasyEquitiesClient() if platform == 'easyequities' else SatrixClient()
)
client.login(username=username, password=password)

# List of accounts
accounts = client.accounts.list()


def convert_to_float(value: str) -> float:
    """
    Get the float value from, for example, "R9 323.46".
    """
    return float(value[1:].replace(' ', ''))


# Go through each account
for account in accounts:
    print(f"# {account.name}\n")
    # Go through each holding
    holdings = client.accounts.holdings(account.id)
    for holding in holdings:
        print(f"- {holding['name']}: ", end='')
        currency = holding['purchase_value'][0]
        purchase_value = convert_to_float(holding['purchase_value'])
        profit_loss = convert_to_float(holding['current_value']) - convert_to_float(
            holding['purchase_value']
        )
        profit_loss_perc = (profit_loss / purchase_value) * 100
        symbol = '+' if profit_loss >= 0 else '-'
        colour = Fore.GREEN if profit_loss >= 0 else Fore.RED

        str_profit_loss = (
            f"{symbol}{currency}{abs(profit_loss):.2f} ({profit_loss_perc:.2f}%)"
        )
        print(colour + str_profit_loss)
    print("")
