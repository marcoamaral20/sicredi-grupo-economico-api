from app.core.normalization import normalize_account_number
from app.models.associate import Associate
from app.repositories.associate_repository import AssociateRepository


class EconomicGroupService:
    def __init__(self):
        self.repository = AssociateRepository()

    async def get_associate_from_same_group(
        self,
        account_number: str,
    ) -> list[Associate] | None:
        """Return associates in the same group, excluding the requested associate."""
        normalized_account_number = normalize_account_number(account_number)

        target_associate = await self.repository.find_associate_by_account_number(
            account_number=normalized_account_number
        )

        if not target_associate:
            return None

        group_associates = await self.repository.find_associates_by_group_code(
            group_code=target_associate.economic_group_code
        )

        return [
            current_associate
            for current_associate in group_associates
            if current_associate.account_number != normalized_account_number
        ]
