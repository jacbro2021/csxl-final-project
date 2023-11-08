"""Tests for the equipment service"""

from ...models.equipment import Equipment
from ...services.equipment import EquipmentService
import pytest
from sqlalchemy.orm import Session

from .user_equipment_data import equipment, quest_3, arduino, insert_fake_data


@pytest.fixture(autouse=True)
def equipment_service(session: Session):
    """This PyTest fixture is injected into each test parameter of the same name below.

    It constructs a new, empty EquipmentService object."""
    equipment_service = EquipmentService(session)
    return equipment_service


@pytest.fixture(autouse=True)
def fake_data_fixture(session: Session):
    """Inserts fake data to the test session."""
    insert_fake_data(session)
    session.commit()
    yield


def test_get_all(equipment_service: EquipmentService):
    """Tests that all equipment can be retrieved"""
    fetched_equipment = equipment_service.get_all()
    assert fetched_equipment is not None
    assert len(fetched_equipment) == len(equipment)
    assert isinstance(fetched_equipment[0], Equipment)


def test_update(equipment_service: EquipmentService):
    """Tests that an item can be updated"""
    changed_item = Equipment(
        equipment_id=1,
        model="Meta Quest 3",
        equipment_image="placeholder",
        condition=8,
        is_checked_out=True,
    )
    update = equipment_service.update(changed_item)
    assert isinstance(update, Equipment)
    assert update == changed_item


def test_get_all_equipment_is_correct(equipment_service: EquipmentService):
    """Tests that when all equipment is retrieved the fields are still correct"""
    fetched_equipment = equipment_service.get_all()
    assert fetched_equipment[0] == quest_3
    assert fetched_equipment[1] == arduino
