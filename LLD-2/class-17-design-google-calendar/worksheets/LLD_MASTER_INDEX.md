# LLD Design Case Studies - Master Index

A comprehensive collection of Low-Level Design case studies organized by category to help master object-oriented design for interviews.

---

## Category Overview

| # | Category | Key Focus | Case Studies |
|---|----------|-----------|--------------|
| 1 | [Board & Strategy Games](#1-board--strategy-games) | Game loop, Turn management, Move validation | Chess, Snake & Ladder, Sudoku |
| 2 | [Booking & Reservation Systems](#2-booking--reservation-systems) | Seat selection, Concurrency, Payment flow | Movie Ticket, Hotel, Flight |
| 3 | [Financial & Transaction Systems](#3-financial--transaction-systems) | State machines, Transaction integrity | ATM, Splitwise, Digital Wallet |
| 4 | [E-commerce & Marketplace](#4-e-commerce--marketplace) | Catalog, Cart, Order lifecycle | Shopping Cart, Food Delivery |
| 5 | [Social & Communication](#5-social--communication) | Feed generation, Messaging, Notifications | Twitter, Chat System |
| 6 | [Content & Media Management](#6-content--media-management) | Catalog, Search, Access control | Library, File Storage |
| 7 | [Real-world Physical Systems](#7-real-world-physical-systems) | Resource allocation, State management | Parking Lot, Elevator, Vending Machine |
| 8 | [Scheduling & Calendar](#8-scheduling--calendar) | Recurring events, Timezone, Conflicts | Calendar, Meeting Scheduler |

---

## 1. Board & Strategy Games

**Guide:** [GUIDE_GAMES.md](./01_games/GUIDE_GAMES.md)

| Case Study | Difficulty | Key Concepts | Worksheet |
|------------|------------|--------------|-----------|
| Chess | Hard | Piece inheritance, Move validation, Check/Checkmate | [DESIGN_CHESS.md](./01_games/DESIGN_CHESS.md) |
| Snake & Ladder | Easy | Random dice, Board traversal, Win condition | [DESIGN_SNAKE_LADDER.md](./01_games/DESIGN_SNAKE_LADDER.md) |
| Sudoku | Medium | Grid validation, Backtracking hints | [DESIGN_SUDOKU.md](./01_games/DESIGN_SUDOKU.md) |

---

## 2. Booking & Reservation Systems

**Guide:** [GUIDE_BOOKING.md](./02_booking/GUIDE_BOOKING.md)

| Case Study | Difficulty | Key Concepts | Worksheet |
|------------|------------|--------------|-----------|
| Movie Ticket Booking | Medium | Seat locking, Show management | [DESIGN_MOVIE_BOOKING.md](./02_booking/DESIGN_MOVIE_BOOKING.md) |
| Hotel Reservation | Medium | Room types, Date range booking | [DESIGN_HOTEL_BOOKING.md](./02_booking/DESIGN_HOTEL_BOOKING.md) |
| Flight Booking | Hard | Seat classes, Passenger details, PNR | [DESIGN_FLIGHT_BOOKING.md](./02_booking/DESIGN_FLIGHT_BOOKING.md) |

---

## 3. Financial & Transaction Systems

**Guide:** [GUIDE_FINANCIAL.md](./03_financial/GUIDE_FINANCIAL.md)

| Case Study | Difficulty | Key Concepts | Worksheet |
|------------|------------|--------------|-----------|
| ATM | Medium | State machine, Card/PIN auth, Cash dispensing | [DESIGN_ATM.md](./03_financial/DESIGN_ATM.md) |
| Expense Sharing (Splitwise) | Medium | Split strategies, Balance settlement | [DESIGN_SPLITWISE.md](./03_financial/DESIGN_SPLITWISE.md) |
| Digital Wallet | Medium | Transaction types, Balance management | [DESIGN_WALLET.md](./03_financial/DESIGN_WALLET.md) |

---

## 4. E-commerce & Marketplace

**Guide:** [GUIDE_ECOMMERCE.md](./04_ecommerce/GUIDE_ECOMMERCE.md)

| Case Study | Difficulty | Key Concepts | Worksheet |
|------------|------------|--------------|-----------|
| Shopping Cart | Medium | Cart operations, Inventory, Pricing | [DESIGN_SHOPPING_CART.md](./04_ecommerce/DESIGN_SHOPPING_CART.md) |
| Food Delivery | Hard | Restaurant, Menu, Order tracking, Delivery | [DESIGN_FOOD_DELIVERY.md](./04_ecommerce/DESIGN_FOOD_DELIVERY.md) |

---

## 5. Social & Communication

**Guide:** [GUIDE_SOCIAL.md](./05_social/GUIDE_SOCIAL.md)

| Case Study | Difficulty | Key Concepts | Worksheet |
|------------|------------|--------------|-----------|
| Twitter | Hard | Tweet, Follow, Feed generation | [DESIGN_TWITTER.md](./05_social/DESIGN_TWITTER.md) |
| Chat/Messenger | Medium | Message types, Conversation, Status | [DESIGN_MESSENGER.md](./05_social/DESIGN_MESSENGER.md) |

---

## 6. Content & Media Management

**Guide:** [GUIDE_CONTENT.md](./06_content/GUIDE_CONTENT.md)

| Case Study | Difficulty | Key Concepts | Worksheet |
|------------|------------|--------------|-----------|
| Library Management | Easy | Book, Member, Issue/Return | [DESIGN_LIBRARY.md](./06_content/DESIGN_LIBRARY.md) |
| File Storage (Dropbox) | Medium | File/Folder hierarchy, Sharing | [DESIGN_FILE_STORAGE.md](./06_content/DESIGN_FILE_STORAGE.md) |

---

## 7. Real-world Physical Systems

**Guide:** [GUIDE_PHYSICAL.md](./07_physical/GUIDE_PHYSICAL.md)

| Case Study | Difficulty | Key Concepts | Worksheet |
|------------|------------|--------------|-----------|
| Parking Lot | Easy | Spot types, Vehicle tracking | [DESIGN_PARKING_LOT.md](./07_physical/DESIGN_PARKING_LOT.md) |
| Elevator System | Medium | Request scheduling, Multi-elevator | [DESIGN_ELEVATOR.md](./07_physical/DESIGN_ELEVATOR.md) |
| Vending Machine | Easy | State machine, Inventory, Payment | [DESIGN_VENDING_MACHINE.md](./07_physical/DESIGN_VENDING_MACHINE.md) |

---

## 8. Scheduling & Calendar

**Guide:** [GUIDE_SCHEDULING.md](./08_scheduling/GUIDE_SCHEDULING.md)

| Case Study | Difficulty | Key Concepts | Worksheet |
|------------|------------|--------------|-----------|
| Google Calendar | Hard | Recurring events, Timezone, Slots | *(See main class notes)* |
| Meeting Scheduler | Medium | Availability, Conflict detection | [DESIGN_MEETING_SCHEDULER.md](./08_scheduling/DESIGN_MEETING_SCHEDULER.md) |

---

## How to Use These Worksheets

### For Self-Practice
1. Start with the **Category Guide** to understand patterns
2. Read the **Overview** section of the worksheet
3. Try **Requirements Gathering** without looking at hints
4. Design **Use Cases** and **Class Diagram**
5. Check hints only after attempting

### For Interview Prep
1. Practice 1-2 from each category
2. Time yourself: 45 mins for design, 30 mins for core code
3. Focus on **extensibility** - interviewers love asking "what if we add X?"

### Difficulty Progression
```
Easy → Medium → Hard

Parking Lot → Elevator → Calendar
Snake & Ladder → Chess → -
Library → File Storage → -
```

---

## Quick Reference: Common Patterns

| Pattern | Used In | Purpose |
|---------|---------|---------|
| Strategy | Games, Payment, Split types | Interchangeable algorithms |
| State Machine | ATM, Vending Machine, Order | State transitions |
| Factory | Piece creation, Vehicle types | Object creation |
| Observer | Notifications, Game events | Event broadcasting |
| Singleton | Board, Parking Lot | Single instance |
| Composite | File/Folder, Menu categories | Tree structures |

---