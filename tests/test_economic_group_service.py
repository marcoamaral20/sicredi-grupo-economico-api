import asyncio
from types import SimpleNamespace

from app.services.economic_group_service import EconomicGroupService


class FakeAssociateRepository:
    def __init__(self):
        self.associates = [
            SimpleNamespace(
                account_number="581516",
                name="Joao Pedro Silva",
                cpf_cnpj="94544960659",
                economic_group_code=1003,
            ),
            SimpleNamespace(
                account_number="428421",
                name="Maria Fernanda Alves",
                cpf_cnpj="22872352687",
                economic_group_code=1003,
            ),
            SimpleNamespace(
                account_number="357408",
                name="Carlos Eduardo Santos",
                cpf_cnpj="68346379018",
                economic_group_code=1003,
            ),
        ]

    async def find_associate_by_account_number(self, account_number: str):
        return next(
            (
                associate
                for associate in self.associates
                if associate.account_number == account_number
            ),
            None,
        )

    async def find_associates_by_group_code(self, group_code: int):
        return [
            associate
            for associate in self.associates
            if associate.economic_group_code == group_code
        ]


def build_service() -> EconomicGroupService:
    service = EconomicGroupService()
    service.repository = FakeAssociateRepository()
    return service


def test_returns_associates_from_same_economic_group():
    associates = asyncio.run(
        build_service().get_associate_from_same_group("581516")
    )

    assert [associate.account_number for associate in associates] == [
        "428421",
        "357408",
    ]


def test_returns_none_when_account_is_not_found():
    associates = asyncio.run(
        build_service().get_associate_from_same_group("000000")
    )

    assert associates is None


def test_excludes_queried_associate_when_account_contains_formatting():
    associates = asyncio.run(
        build_service().get_associate_from_same_group("58151-6")
    )

    assert [associate.account_number for associate in associates] == [
        "428421",
        "357408",
    ]
