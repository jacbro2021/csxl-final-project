"""
The equipment service allows the API to manipulate equipment in the database.
"""

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..database import db_session
from ..models.equipment import Equipment
from ..entities.equipment_entity import EquipmentEntity
from ..models import User

from .exceptions import EquipmentNotFoundException

# Excluding this import for now, however, we will need to use in later sprints for handling different types of users
# from .permission import PermissionService

__authors__ = ["Jacob Brown"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class EquipmentService:
    """Service that performs all of the actions on the equipment table."""

    def __init__(
        self,
        session: Session = Depends(db_session),
    ):
        """Initialize the session for querying the db."""
        self._session = session

    def get_all(self) -> list[Equipment]:
        """Return a list of all equipment in the db."""
        # Create the query for getting all equipment entities.
        query = select(EquipmentEntity)
        # execute the query grabbing each row from the equipment table
        query_result = self._session.scalars(query).all()
        # convert the query results into 'Equipment' models and return as a list
        return [result.to_model() for result in query_result]

    # TODO: add param for user and save users pid in equipments list of pids and implement permissions
    def update(self, item: Equipment) -> Equipment:
        """
        updates a specific equipment item.

        Args:
            model (Equipment): The model to update.
            TODO: model (User): The user that is checking out the equipment.

        Returns:
            Equipment: the checked out equipment.
        """

        # get item with matching equipment_id from db
        query = select(EquipmentEntity).where(
            EquipmentEntity.equipment_id == item.equipment_id
        )
        entity_item: EquipmentEntity | None = self._session.scalar(query)

        if entity_item:
            entity_item.update(item)

            self._session.commit()
            return entity_item.to_model()

        else:
            raise EquipmentNotFoundException(item.equipment_id)

    def add_item(self, item: Equipment) -> Equipment:
        """
        Creates a new equipment entity and adds to the data base

        Args:
            model (Equipment): The model to insert into the db.


        Returns:
            Equipment: the inserted equipment.
        """

        entity = EquipmentEntity.from_model(item)
        self._session.add(entity)
        self._session.commit()
        return entity.to_model()

    def delete_item(self, item: Equipment) -> Equipment:
        """
        Delets an Equipment item from the database

        Args:
            model (Equipment): The model to delete from the db.


        Returns:
            Equipment: the deleted equipment.
        """

        entity = EquipmentEntity.from_model(item)
        self._session.delete(entity)
        self._session.commit()
        return entity.to_model()
