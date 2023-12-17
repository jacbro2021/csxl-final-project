# Computer Science Experience Labs

The Experience Labs' (XL) mission is to accelerate technical experience and build community among undergraduate CS majors at The University of North Carolina at Chapel Hill. The XL's web app, found in production at `csxl.unc.edu`, is backed by this repository.

## Purpose

This project was built by various students in UNC Chapel Hill's COMP 590 Special topics course, as well as Kris Jordan. More specifically I worked alongside Ayden Franklin, David Sprague, and Nicholas Mountain to implement an equipment reservation system that enables students to check equipment (like Meta Quest 3's or Arduino Uno's) in and out of the CSXL.
The equipment feature was implemented over the course of three, two week, sprints. All team members made significant contributions to the feature in both the frontend and backend of the project.  

## Tech Stack

The stack for this project uses Angular, Rxjs, and Angular Material UI for the Frontend. The project uses Fast API and SQL Alchemy for the backend. For the data layer, this project uses a Postgres SQL database. 

## Equipment Specific Documentation

* [Equipment Reservation Design Doc & Specs](docs/docs/equipment-reservation-system-design-doc-spec.md)
* [Equipment Reservation Wireframes and Planning](docs/docs/equipment-reservation-system-design-doc.md)

## Developer Docs

* [Get Started with a Development Environment](docs/get_started.md)
* [Authentication, Authorization, and Permissions](docs/auth.md)
* [Testing Tools](docs/testing.md)

## Feature Docs

* [Github Integration](docs/github_integration.md)

## Equipment Reservation System Images

![Equipment Page](docs/images/equipment-page.png "Equipment Page")

![Equipment Checkouts](docs/images/stage_and_checkout_requests.png "Equipment Checkouts")

![Equipment Checkouts](docs/images/equipment_checkouts.png "Equipment Checkouts")
