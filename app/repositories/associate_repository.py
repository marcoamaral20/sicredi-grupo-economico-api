from app.core.logging import logger
from app.models.associate import Associate


class AssociateRepository:
    async def find_associate_by_account_number(
        self,
        account_number: str,
    ) -> Associate | None:
        """Find associate by account number."""
        logger.info("Searching associate by account number=%s", account_number)

        associate = await Associate.find_one(
            Associate.account_number == account_number
        )

        if not associate:
            logger.warning("Associate not found: account_number=%s", account_number)
            return None

        return associate

    async def find_associates_by_group_code(
        self,
        group_code: int,
    ) -> list[Associate]:
        """Find all associates belonging to the given economic group."""
        logger.info("Searching associates by group code=%s", group_code)

        associates = await Associate.find(
            Associate.economic_group_code == group_code
        ).to_list()

        if not associates:
            logger.warning("No associates found for economic_group_code=%s", group_code)
            return []

        return associates

    async def bulk_upsert(
        self,
        associates: list[Associate],
    ) -> None:
        for associate in associates:
            await Associate.find_one(
                Associate.account_number == associate.account_number
            ).upsert(
                {
                    "$set": associate.model_dump(
                        exclude={"id", "revision_id"}
                    )
                },
                on_insert=associate,
            )
