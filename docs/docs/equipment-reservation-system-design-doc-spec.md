# Equipment Reservation Technical Specification Documentation

## #1: Descriptions and sample data representations of new or modified model representation(s) and API routes supporting your feature’s stories

### Models

[New: Equipment Checkout Request Model Permalink](https://github.com/comp423-23f/csxl-final-team-d9/blob/d304096272b3f7eee05019938bc392cc9889ad48/backend/models/equipment_checkout_request.py#L11-L21)

This is a new model to represent a request to check out a piece of equipment. Request is made by the user and approved by the ambassador.

[Changed: Equipment Model](https://github.com/comp423-23f/csxl-final-team-d9/blob/d304096272b3f7eee05019938bc392cc9889ad48/backend/models/equipment.py#L23-L24)

Added condition notes array and checkout history array that will eventually store a list of PIDs.

[Changed: User Model](https://github.com/comp423-23f/csxl-final-team-d9/blob/d304096272b3f7eee05019938bc392cc9889ad48/backend/models/user.py#L39)

Added has_signed_waiver field to user model to track whether they have signed the equipment liability wavier.

### API Routes

[New: /add_request](https://github.com/comp423-23f/csxl-final-team-d9/blob/d304096272b3f7eee05019938bc392cc9889ad48/backend/api/equipment/checkout.py#L95-L122)

This new API route allows a user to create and add an equipment checkout request to backend database.

[New: /get_all_requests](https://github.com/comp423-23f/csxl-final-team-d9/blob/d304096272b3f7eee05019938bc392cc9889ad48/backend/api/equipment/checkout.py#L155-L170)

This new API route allows an ambassador to view all equipment checkout requests.

[New: /delete_request](https://github.com/comp423-23f/csxl-final-team-d9/blob/d304096272b3f7eee05019938bc392cc9889ad48/backend/api/equipment/checkout.py#L126-L151)

This allows an ambassador to delete a users equipment checkout request to either approve or cancel the request.

[New: /get_all_for_request](https://github.com/comp423-23f/csxl-final-team-d9/blob/d304096272b3f7eee05019938bc392cc9889ad48/backend/api/equipment/checkout.py#L174-L191)

This allows an ambassador to see all of the available equipment that can be checked out for a certain equipment type. This is necessary for selecting an item to be checked out for an equipment checkout request.

[New: /update_waiver_field](https://github.com/comp423-23f/csxl-final-team-d9/blob/d304096272b3f7eee05019938bc392cc9889ad48/backend/api/equipment/checkout.py#L195-L215https://github.com/comp423-23f/csxl-final-team-d9/blob/d304096272b3f7eee05019938bc392cc9889ad48/backend/api/equipment/checkout.py#L195-L215)

This allows a user to update their has_signed_waiver field after signing waiver.

## #2: Description of underlying database/entity-level representation decisions

We have created two new entities with corresponding tables: Equipment and EquipmentCheckoutRequest. We needed an equipment entity because we need to sotre each individual piece of equipment. We decided to include an array to store notes about the condition of the equipment. An ambassador will eventually be able to evaluate condition of equipment upon return. Additionally, we needed an eqiupment checkout request entity to appropriately manage users requests for equipment checkouts. Each equipment checkout request has a model field. We decided to do this rather than having a specific piece of equipment tied to the request so that an ambassador can select the piece of equipment that will be checked out.

## #3: At least one technical and one user experience design choice your team weighed the trade-offs with justification for the decision (we chose X over Y, because…)

#### Technical Design Choice:

We decided to have seperate data representations for checkout requests and checkouts rather than having them be the same model/entity and having a status field(request, checked_out, returned). We chose this because need to be able to easily differentiate between checkouts that are pending and checkouts that are confirmed. In the future, ambassadors may be able to view past checkouts and information about requests would be not needed.

#### User Experience Design Choice

For the ambassador view we decided to have a table containing "staged checkouts". This is used to show checkouts that are in the process of being confirmed by the ambassador(Ambassador is physically going to get the device and then selecting corresponding ID). We did this instead of directly confirming to allow the ambassador to "stage" a request, go look at equipment that is available, choose a piece of equipment, and select this piece of equipment on the application. This gives the ambassador control over what piece of equipment is being checked out.

## #4 Development concerns: How does a new developer get started on your feature? Brief guide/tour of the files and concerns they need to understand to get up-to-speed.

#### Frontend

- Equipment Module: This declares each component and widget related to equipment feature. This module imports any angular material components/modules used for the feature.
- User-Equipment Component: This contains the equipment card widgets for each equipment type. Calls the equipment service, which in turn calls the API route for getting all equipment_types.
- Equipment Card Widget: This widget displays equipment type information including model, picture, and number available.
- Ambassador Component: This component contains the checkout request card and staged checkout request card widgets.
- Checkout request card: This displays all checkout request that have been made by users.
- Staged checkout request card: This widget displays all staged checkout requests. Ambassador can select a piece of equipment by it's id in this table.
- Waiver Component: This component displays a fake waiver and requires an input to the signiture field. It is only routed to if the user has not yet signed the waiver. After submission, it routes back to the user equipment component.
- EquipmentCheckoutConfirmationComponent: Confirms that a user has requested an equipment checkout request.
- EquipmentService: Communicates with the backend, to control everything that the frontend needs to know to manage the creation and confirmation of checkout requests.

#### Backend

- Entities: Equipment Entity: Stores data about a specific piece of equipment.
  Checkout Request Entity: Stores data about a checkout request made by a user.
- Equipment Service: Handles all the logic for manipulating the database, called by the api routes.
- user_equipment_tests: Tests all methods in the equipment service.
- API Routes: Calls equipment service methods to communicate data changes and logic to and from the frontend.
- user_equipment_data: Stores and inserts mock data for equipment, fake requests, and permissions.
