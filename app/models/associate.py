from typing import Annotated

from beanie import Document, Indexed


class Associate(Document):
    account_number: Annotated[str, Indexed(unique=True)]
    name: str
    cpf_cnpj: str
    economic_group_code: Annotated[int, Indexed()]
