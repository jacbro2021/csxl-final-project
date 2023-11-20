"""
The equipment service allows the API to manipulate equipment in the database.
"""

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from backend.entities.equipment_checkout_request_entity import (
    EquipmentCheckoutRequestEntity,
)
from backend.entities.user_entity import UserEntity
from backend.models.equipment_checkout_request import EquipmentCheckoutRequest

from backend.models.equipment_type import EquipmentType
from .permission import PermissionService

from ..database import db_session
from ..models.equipment import Equipment
from ..entities.equipment_entity import EquipmentEntity
from ..models import User

from .exceptions import EquipmentNotFoundException, WaiverNotSignedException

# Excluding this import for now, however, we will need to use in later sprints for handling different types of users
# from .permission import PermissionService

__authors__ = ["Jacob Brown, Ayden Franklin"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class DuplicateEquipmentCheckoutRequestException(Exception):
    """DuplicateEquipmentCheckoutRequestException is raised when a user tries to make a second checkout request for the same equipment type"""

    def __init__(self, model: str):
        super().__init__(f"User has already requested a checkout for {model}")


class EquipmentCheckoutRequestNotFoundException(Exception):
    """EquipmentCheckoutRequestNotFoundException is raised when an equipment checkout request is searched for and does not exist"""

    def __init__(self, request: EquipmentCheckoutRequest):
        super().__init__(f"Could not find request: {request}")


class EquipmentService:
    """Service that performs all of the actions on the equipment table."""

    def __init__(
        self,
        session: Session = Depends(db_session),
    ):
        """Initialize the session for querying the db."""
        self._session = session
        self._permission = PermissionService(session=self._session)

    def get_all(self) -> list[Equipment]:
        """Return a list of all equipment in the db."""
        # Create the query for getting all equipment entities.
        query = select(EquipmentEntity)
        # execute the query grabbing each row from the equipment table
        query_result = self._session.scalars(query).all()
        # convert the query results into 'Equipment' models and return as a list
        return [result.to_model() for result in query_result]

    # TODO: add param for user and save users pid in equipments list of pids
    def update(self, item: Equipment, subject: User) -> Equipment:
        """
        updates a specific equipment item.

        Args:
            model (Equipment): The model to update.
            TODO: model (User): The user that is checking out the equipment.

        Returns:
            Equipment: the checked out equipment.
        """

        # ensure user has ambassador permissions
        self._permission.enforce(subject, "equipment.update", "equipment")

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

    def get_all_types(self) -> list[EquipmentType]:
        """
        Converts equipment into list of EquipmentType models

        Args:
            None.

        Returns:
            the unique names of all equipment and the number of each type of equipment.
        """

        all_equipment = self.get_all()
        equipment_types = []

        for equipment in all_equipment:
            # flag to keep track whether the equipment model was succesfully mapped to a equipment_type entry
            caught = False
            for equipment_type in equipment_types:
                if equipment.model == equipment_type.model:
                    # If equipment is currently checked out, not added to num_available
                    if not equipment.is_checked_out:
                        equipment_type.num_available += 1

                    # equipment was successfully mapped to an existing equipment type in the return list
                    caught = True
                    break
            if not caught:
                # If equipment passed through type list without getting caught, this is the first time encountering its type

                if equipment.is_checked_out:
                    # If the equipment is checked out, add its type to the type list, but initialize num_available to 0
                    new_type = EquipmentType(
                        model=equipment.model,
                        num_available=0,
                        equipment_img_URL=equipment.equipment_image,
                    )
                else:
                    # If the equipment is not checked out, add its type to the type list and initialize num_available to 1
                    new_type = EquipmentType(
                        model=equipment.model,
                        num_available=1,
                        equipment_img_URL=equipment.equipment_image,
                    )
                equipment_types.append(new_type)

        return equipment_types

    def add_request(
        self, request: EquipmentCheckoutRequest, user: User
    ) -> EquipmentCheckoutRequest:
        """
        creates an equipment checkout request.

        Args:
            request (EquipmentCheckoutRequest): the checkout request to add.
            user (User): the user trying to request a checkout.

        Returns:
            EquipmentCheckoutRequest: the checkout request we added.

        Raises:
            WaiverNotSignedException if the user has not signed the liability waiver.
        """

        # check if the user has signed the liability waiver
        if not user.signed_equipment_wavier:
            raise WaiverNotSignedException

        # check if the user has already submitted a checkout request for the same type of equipment
        obj = (
            self._session.query(EquipmentCheckoutRequestEntity)
            .filter(
                EquipmentCheckoutRequestEntity.model == request.model,
                EquipmentCheckoutRequestEntity.pid == request.pid,
            )
            .one_or_none()
        )

        # if the user is trying to send a duplicate request, raise exception
        if obj:
            raise DuplicateEquipmentCheckoutRequestException(request.model)

        # create new object
        equipment_checkout_request_entity = EquipmentCheckoutRequestEntity.from_model(
            request
        )

        # add new object to table and commit changes
        self._session.add(equipment_checkout_request_entity)
        self._session.commit()

        # return added object
        return equipment_checkout_request_entity.to_model()

    def delete_request(self, subject: User, request: EquipmentCheckoutRequest) -> None:
        """
        Delete an equipment checkout request

        Args:
            subject (User): the user trying to delete the request
            request (EquipmentCheckoutRequest): the request to be deleted
        """

        self._permission.enforce(
            subject, "equipment.delete_request", resource="equipment"
        )
        # find object to delete
        obj = (
            self._session.query(EquipmentCheckoutRequestEntity)
            .filter(
                EquipmentCheckoutRequestEntity.model == request.model,
                EquipmentCheckoutRequestEntity.pid == request.pid,
            )
            .one_or_none()
        )

        # ensure object exists
        if obj:
            # delete object and commit
            self._session.delete(obj)
            self._session.commit()
        else:
            # raise exception
            raise EquipmentCheckoutRequestNotFoundException(request)

    def get_all_requests(self, subject: User) -> list[EquipmentCheckoutRequest]:
        """Return a list of all equipment checkout requests in the db"""
        # enforce ambasssador permission
        self._permission.enforce(
            subject, "equipment.get_all_requests", resource="equipment"
        )
        # create the query for getting all equipment checkout request entities.
        query = select(EquipmentCheckoutRequestEntity)
        # execute the query grabbing each row from the equipment table
        query_result = self._session.scalars(query).all()
        # convert the query results into 'EquipmentReservationRequest' models and return as a list
        return [result.to_model() for result in query_result]

    def get_equipment_for_request(self, subject: User, model: str) -> list[Equipment]:
        """returns a list of all available equipment corresponding to the checkout request's model"""

        # enforce ambassador permission
        self._permission.enforce(
            subject, "equipment.get_equipment_for_request", "equipment"
        )

        # query for all equipment that matches the checkout request model type AND is not checked out
        query = select(EquipmentEntity).where(
            EquipmentEntity.model == model,
            EquipmentEntity.is_checked_out == False,
        )

        # return list of queried equipment entities as equipment models
        return [result.to_model() for result in self._session.scalars(query).all()]

    def update_waiver_signed_field(self, user: User) -> User:
        """Updates the signed_equipment_waiver field of a user after they have signed a waiver"""
        # create new user model that is the same as the one to be updated,
        # but with the signed_equipment_waiver being true
        updated_user: User = user
        updated_user.signed_equipment_wavier = True

        # query for user to be updated
        query = select(UserEntity).where(UserEntity.pid == user.pid)
        entity_item: UserEntity | None = self._session.scalar(query)

        # if user was found, update signed waiver field
        if entity_item:
            entity_item.update(updated_user)

            self._session.commit()
            return entity_item.to_model()

        # if user not found, raise exception
        else:
            raise Exception(f"Could not find user {user.first_name} {user.last_name}")

    # TODO: Uncomment during sp02 if we decide to add admin functions for adding/deleting equipment.
    # def add_item(self, item: Equipment) -> Equipment:
    #     """
    #     Creates a new equipment entity and adds to the data base

    #     Args:
    #         model (Equipment): The model to insert into the db.

    #     Returns:
    #         Equipment: the inserted equipment.
    #     """

    #     entity = EquipmentEntity.from_model(item)
    #     self._session.add(entity)
    #     self._session.commit()
    #     return entity.to_model()

    # def delete_item(self, item: Equipment) -> Equipment:
    #     """
    #     Delets an Equipment item from the database

    #     Args:
    #         model (Equipment): The model to delete from the db.

    #     Returns:
    #         Equipment: the deleted equipment.
    #     """

    #     entity = EquipmentEntity.from_model(item)
    #     self._session.delete(entity)
    #     self._session.commit()
    #     return entity.to_model()
