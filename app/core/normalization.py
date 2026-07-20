import re


def normalize_account_number(account_number: str) -> str:
    return re.sub(r"\D", "", account_number)
