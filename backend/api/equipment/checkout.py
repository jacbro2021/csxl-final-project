"""Equipment Checkout API

This API is used to manage and list user equipment checkouts"""

from fastapi import APIRouter, Depends, HTTPException
from ...models.equipment import Equipment
from ...services.equipment import EquipmentService

__authors__ = ["Nicholas Mountain", "Jacob Brown", "Ayden Franklin", "David Sprague"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"

api = APIRouter(prefix="/api/equipment")
openapi_tags = {
    "name": "Equipment",
    "description": "Get Equipment and update equipment properties.",
}


@api.get("/get_all", tags=["Equipment"])
def get_all(equipment_service: EquipmentService = Depends()) -> list[Equipment]:
    """Gets all equipment in the database and returns to the user as a list of equipment models."""
    return equipment_service.get_all()


@api.put("/update", tags=["Equipment"])
def update(
    item: Equipment, equipment_service: EquipmentService = Depends()
) -> Equipment:
    """Updates an item of equipment and returns the updated item as an equipment model"""
    return equipment_service.update(item)

