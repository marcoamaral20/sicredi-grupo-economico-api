from fastapi import APIRouter, HTTPException

from app.core.logging import logger
from app.schemas.associate import AssociateResponse
from app.services.economic_group_service import EconomicGroupService

router = APIRouter(
    prefix="/associates",
    tags=["Associates"],
)

service = EconomicGroupService()


@router.get(
    "/{account_number}",
    status_code=200,
    response_model=list[AssociateResponse],
)
async def get_economic_group(account_number: str):
    logger.info(
        "Processing economic group request for account_number=%s",
        account_number,
    )

    associates = await service.get_associate_from_same_group(
        account_number=account_number
    )

    if associates is None:
        raise HTTPException(
            status_code=404,
            detail="Associate not found.",
        )

    return associates
