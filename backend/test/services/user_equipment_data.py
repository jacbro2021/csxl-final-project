"""Mock data for equipment.

"""

import pytest
from sqlalchemy.orm import Session
from .reset_table_id_seq import reset_table_id_seq
from ...entities.equipment_entity import EquipmentEntity
from ...models.equipment import Equipment


__authors__ = ["Nicholas Mountain, Jacob Brown"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


quest_3 = Equipment(
    equipment_id=1,
    model="Meta Quest 3",
    equipment_image="placeholder",
    condition=10,
    is_checked_out=False,
)
arduino = Equipment(
    equipment_id=2,
    model="Arduino Uno",
    equipment_image="placeholder",
    condition=10,
    is_checked_out=False,
)

equipment = [quest_3, arduino]


def insert_fake_data(session: Session):
    global equipment

    # Create entities for test equipment data
    print("is this running?")
    entities = []
    for item in equipment:
        entity = EquipmentEntity.from_model(item)
        session.add(entity)
        entities.append(entity)

    # Reset table IDs to prevent ID conflicts
    reset_table_id_seq(session, EquipmentEntity, EquipmentEntity.id, len(equipment) + 1)

    # Commit all changes
    session.commit()
