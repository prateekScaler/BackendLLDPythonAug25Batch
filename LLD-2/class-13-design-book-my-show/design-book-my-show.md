# Design BookMyShow

## Context

BookMyShow is India's biggest online movie and events ticketing brand. The platform enables users to discover movies, view showtimes across different theaters and screens, and book tickets seamlessly.

![BookMyShow](https://ideausher.com/wp-content/uploads/2021/09/Frame-14.jpg)

## Overview

- **One-liner overview**: This design focuses on building the core movie ticket booking management system. 
- **Persistence**: We will implement a production-grade solution that persists data in a database (rather than in-memory storage), handles real-world concurrency issues during seat booking, and includes comprehensive schema design. 
- **How'd we take input from user/admin**: The system will accept inputs through REST API endpoints.

## Requirements gathering

What are some questions you would ask to gather requirements?

1. Can a cinema theater have multiple screens?
2. Can a movie be shown in multiple screens?
3. Can a movie be of multiple languages?
4. Can a user book multiple tickets for a single movie?
5. Are there multiple types of tickets?
6. How does user find a movie?
7. How does a user book a ticket?
8. How does a user pay for a ticket?
9. How does a new movie get added to the system?
10. Are there any discounts available?

## Requirements

Build an online movie ticket booking system that can support the following requirements:

* Support for multiple cities
* Each city will have multiple cinemas
* Each cinema can have multiple screens
* Each screen will play one movie at a time
* A cinema will play multiple movies
* Each screen can have multiple types of seats
  * GOLD
  * DIAMOND
  * PLATINUM
* Allow the user to search a movie by name
* Allow the user to filter movies by the following fields
  * Location
  * Cinema
  * Language
  * Rating
  * Category
* Each movie can have multiple slots
* Users can book tickets and pay via multiple payment methods
  * UPI
  * Credit Card
  * Netbanking
* A user can apply a coupon or a promo code at checkout
* A user can see the availability of seats in a screen
* The price of a ticket will be decided by multiple parameters
  * Seat Type
  * Day of the week
  * Time of the Day
  * Movie
  * Cinema screen
* A user can also cancel or update a booking
* A user cannot book or cancel after the cutoff time which is 1 hour before the movie starts


## Use case diagrams

Are the requirements clear enough to define use cases?
If not, try to think of the actors and their interactions with the system.

### Actors

What would be the actors in this system?

1. User
2. Admin

### Use cases

What would be the use cases i.e. the interactions between the actors and the system?

#### Actor 1

Name of actor - `Admin`

Use cases:
* Add a new movie
* Add a new cinema screen
* Add a new show

#### Actor 2

Name of actor - `User`

Use cases:
* Search for a movie
* Book a ticket
* Pay for a ticket
* Cancel a ticket


---

Refer [use case diagram file](USE-CASE-DIAGRAM.puml) in this directory. 


## Class diagrams

Refer [class diagram mermaid file](BMS-CLASS-DIAGRAM.md) in this directory.

What will be the major classes and their attributes?

* City
  * name
  * Theaters
* Theater
  * name
  * address
  * Screens
  * Shows
* Screen
  * name
  * Seats
  * Shows
* Seat
  * Number
  * Type - `GOLD, DIAMOND, PLATINUM`
* Show
  * Movie
  * start time
  * duration
  * Language
  * ShowSeats
* Movie
  * name
  * rating
  * category
  * languages
  * Shows
* Ticket
  * amount
  * Seats
  * Show
  * User
  * Payment
  * Status
* Payment
  * amount
  * Mode - `UPI, CREDIT_CARD, NETBANKING`
  * Status - `SUCCESS, FAILED`
  * Ticket


## API design

What will be some APIs that you would design for this system?

Look at the use cases and try to design APIs for each of them.

You can simply write the APIs in the following format:
`API name` - `HTTP method` - `URL` - `?Request body` - `?Response body`

You could also use a tool like [Swagger](https://swagger.io/) to design the APIs or follow [this](https://github.com/jamescooke/restapidocs) repository for a simple way to use Markdown to structure your API documentation.