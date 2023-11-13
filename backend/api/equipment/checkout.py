"""Equipment Checkout API

This API is used to manage and list user equipment checkouts"""

from fastapi import APIRouter, Depends, HTTPException

from backend.models.equipment_type import EquipmentType
from backend.models.user import User
from ...models.equipment import Equipment
from ...services.equipment import EquipmentService

from backend.api.authentication import registered_user

__authors__ = ["Nicholas Mountain", "Jacob Brown", "Ayden Franklin", "David Sprague"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"

api = APIRouter(prefix="/api/equipment")
openapi_tags = {
    "name": "Equipment",
    "description": "Get Equipment and update equipment properties.",
}


@api.get("/get_all", tags=["Equipment"])
def get_all(
    equipment_service: EquipmentService = Depends(),
) -> list[Equipment]:
    """
    Gets all equipment

    Parameters:
        equipment_service: dependency on 'EquipmentService'

    Returns:
        List of equipment in the database
    """
    
    return equipment_service.get_all()


@api.put("/update", tags=["Equipment"])
def update(
    item: Equipment,
    equipment_service: EquipmentService = Depends(),
    subject: User = Depends(registered_user),
) -> Equipment:
    """
    Update an equipment item

    Parameters:
        item: Item to be updated in the database
        subject: a valid User model representing the currently logged in User
        equipmentService: a valid 'EquipmentService'

    Returns:
        Equipment: the updated Equipment item

    Raises:
        HTTPException 422 if update() raises an Exception
    """

    try:
        # Attempt to update the equipment item.
        return equipment_service.update(item, subject)
    except Exception as e:
        # Raise exception if data incorrectly formatted / not authorized.
        raise HTTPException(status_code=422, detail=str(e))


@api.get("/get_all_types", tags=["Equipment"])
def get_all_types(
    equipment_service: EquipmentService = Depends(),
) -> list[EquipmentType]:
    """
    Gets equipment types and the respective number of items of that type.

    Parameters:
        equipment_service: a valid 'EquipmentService'

    Returns:
        Organization: Created organization

    Raises:
        HTTPException 422 if create() raises an Exception
    """

    return equipment_service.get_all_types()
