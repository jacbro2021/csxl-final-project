"""Tests for the equipment service"""

from unittest.mock import create_autospec
from .reset_table_id_seq import reset_table_id_seq
from backend.entities.role_entity import RoleEntity
from backend.models.equipment_type import EquipmentType
from backend.models.role import Role
from backend.services.exceptions import UserPermissionException
from ...models.equipment import Equipment
from ...services.equipment import EquipmentService
from ...services.user import UserService
import pytest
from sqlalchemy.orm import Session

from .user_equipment_data import equipment, quest_3, arduino, insert_fake_data
from .user_data import user, ambassador


@pytest.fixture(autouse=True)
def equipment_service(session: Session):
    """This PyTest fixture is injected into each test parameter of the same name below.
    It constructs a new, empty EquipmentService object."""
    equipment_service = EquipmentService(session)
    return equipment_service


@pytest.fixture(autouse=True)
def fake_data_fixture(session: Session):
    """Inserts fake data to the test session."""

    # Add ambassador role for testing permissions specific to ambassadors.
    ambassador_role = Role(id=2, name="ambassadors")
    entity = RoleEntity.from_model(ambassador_role)
    session.add(entity)
    session.commit()
    reset_table_id_seq(session, RoleEntity, RoleEntity.id, 3)

    # Insert fake equipment data for testing
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
    equipment_service._permission = create_autospec(equipment_service._permission)

    update = equipment_service.update(changed_item, ambassador)

    equipment_service._permission.enforce.assert_called_with(
        ambassador, "equipment.update", "equipment"
    )

    assert isinstance(update, Equipment)
    assert update == changed_item


def test_update_not_authorized(equipment_service: EquipmentService):
    """Tests that an item cannot be updated when the user does not have ambassador permissions"""
    changed_item = Equipment(
        equipment_id=1,
        model="Meta Quest 3",
        equipment_image="placeholder",
        condition=8,
        is_checked_out=True,
    )
    with pytest.raises(Exception) as e:
        equipment_service.update(changed_item, user)
        # Fail test if no exception is thrown
        pytest.fail()

def test_update_equipment_not_in_db(equipment_service: EquipmentService):
    """Tests that an error is thrown when the update method is called on an item that is not in the database."""
    changed_item = Equipment(
        equipment_id=100,
        model="Ipod Nano",
        equipment_image="placeholder",
        condition=6,
        is_checked_out=True,
    )

    equipment_service._permission = create_autospec(equipment_service._permission)

    with pytest.raises(Exception) as e:
        # Call update method with data that is not in the database.
        update = equipment_service.update(changed_item, ambassador)

        equipment_service._permission.enforce.assert_called_with(
            ambassador, "equipment.update", "equipment"
        )

        # Fail test if no exception is raised


def test_get_all_equipment_is_correct(equipment_service: EquipmentService):
    """Tests that when all equipment is retrieved the fields are still correct"""
    fetched_equipment = equipment_service.get_all()
    assert fetched_equipment[0] == quest_3
    assert fetched_equipment[1] == arduino


def test_get_all_types(equipment_service: EquipmentService):
    """Tests that all equipment properly converted to equipment type"""
    fetched_equipment_types = equipment_service.get_all_types()
    assert fetched_equipment_types is not None
    assert isinstance(fetched_equipment_types[0], EquipmentType)


def test_get_all_types_inventory_correct(equipment_service: EquipmentService):
    """Tests for correct num_available for each equipment type"""
    fetched_equipment_types = equipment_service.get_all_types()
    assert fetched_equipment_types[0].num_available == 1
    assert fetched_equipment_types[1].num_available == 2


def test_get_all_types_when_zero_available(equipment_service: EquipmentService):
    """Tests for correct num_available when equipment is checked out"""
    # first update database so Meta Quest 3 is checked out
    changed_item = Equipment(
        equipment_id=1,
        model="Meta Quest 3",
        equipment_image="placeholder",
        condition=8,
        is_checked_out=True,
    )
    equipment_service._permission = create_autospec(equipment_service._permission)

    update = equipment_service.update(changed_item, ambassador)

    equipment_service._permission.enforce.assert_called_with(
        ambassador, "equipment.update", "equipment"
    )

    _ = equipment_service.update(changed_item, ambassador)

    fetched_equipment_types = equipment_service.get_all_types()
    assert fetched_equipment_types[1].num_available == 0
