# Hints: Library Management System

## Hint 1: Actors

<details>
<summary>Click to reveal</summary>

1. **Member** - Search, borrow, return, reserve books
2. **Librarian** - Manage inventory, manage members, handle issues
3. **System** - Track due dates, calculate fines, send notifications

</details>

---

## Hint 2: Book vs BookCopy (Critical!)

<details>
<summary>Click to reveal</summary>

**Always separate Book (metadata) from BookCopy (physical instance)**

```
Book (ISBN: 978-0-13-468599-1, Title: "Clean Code")
├── BookCopy #1 (Available, Shelf A-15)
├── BookCopy #2 (Issued to Member #123)
├── BookCopy #3 (Reserved for Member #456)
└── BookCopy #4 (Lost)

Why?
- Book = Title, Author, ISBN (same for all copies)
- BookCopy = Physical item with its own status, location
```

```python
class Book:
    isbn: str
    title: str
    author: str
    publisher: str
    copies: List[BookCopy]

class BookCopy:
    id: str
    book: Book  # Reference to parent
    status: BookCopyStatus  # AVAILABLE, ISSUED, RESERVED, LOST
    rack_location: str
```

</details>

---

## Hint 3: BookCopy States

<details>
<summary>Click to reveal</summary>

```python
class BookCopyStatus(Enum):
    AVAILABLE = "available"      # On shelf, can be issued
    ISSUED = "issued"            # Currently borrowed
    RESERVED = "reserved"        # Returned but reserved for someone
    LOST = "lost"                # Reported lost
    UNDER_REPAIR = "repair"      # Being repaired
```

**State Transitions:**
```
AVAILABLE → ISSUED (on issue)
ISSUED → AVAILABLE (on return, no reservations)
ISSUED → RESERVED (on return, has reservations)
RESERVED → ISSUED (when reserved member picks up)
ANY → LOST (when reported lost)
```

</details>

---

## Hint 4: Issue/Loan Entity

<details>
<summary>Click to reveal</summary>

```python
class BookIssue:
    id: str
    book_copy: BookCopy
    member: Member
    issue_date: date
    due_date: date
    return_date: Optional[date]  # None if not returned
    fine_amount: int

    def is_overdue(self) -> bool:
        if self.return_date:
            return self.return_date > self.due_date
        return date.today() > self.due_date

    def calculate_fine(self) -> int:
        if not self.is_overdue():
            return 0
        return_or_today = self.return_date or date.today()
        overdue_days = (return_or_today - self.due_date).days
        return overdue_days * FINE_PER_DAY
```

</details>

---

## Hint 5: Reservation Queue

<details>
<summary>Click to reveal</summary>

```python
class Reservation:
    id: str
    book: Book  # Not BookCopy! User wants any copy
    member: Member
    created_at: datetime
    status: ReservationStatus  # PENDING, FULFILLED, CANCELLED, EXPIRED
    expires_at: Optional[datetime]  # After fulfillment, member has X days to pick up

class ReservationQueue:
    def __init__(self, book):
        self.book = book
        self.queue: List[Reservation] = []

    def add_reservation(self, member):
        # Check if member already has reservation
        reservation = Reservation(book=self.book, member=member)
        self.queue.append(reservation)
        return reservation

    def get_next_reservation(self):
        # Get oldest pending reservation
        pending = [r for r in self.queue if r.status == 'PENDING']
        return pending[0] if pending else None
```

</details>

---

## Hint 6: Member with Limits

<details>
<summary>Click to reveal</summary>

```python
class Member:
    id: str
    name: str
    email: str
    membership_type: MembershipType
    issued_books: List[BookIssue]
    reservations: List[Reservation]
    total_fine_due: int

    def can_issue_book(self) -> Tuple[bool, str]:
        # Check max books limit
        if len(self.get_current_issues()) >= self.membership_type.max_books:
            return False, "Maximum book limit reached"

        # Check for overdue books
        if any(issue.is_overdue() for issue in self.get_current_issues()):
            return False, "Return overdue books first"

        # Check for unpaid fines
        if self.total_fine_due > 0:
            return False, "Pay pending fine first"

        return True, "OK"

    def get_current_issues(self):
        return [i for i in self.issued_books if i.return_date is None]
```

</details>

---

## Hint 7: Class Diagram

<details>
<summary>Click to reveal</summary>

```
┌─────────────────────────────────────────────────────────┐
│                       Library                            │
├─────────────────────────────────────────────────────────┤
│ - books: Dict[ISBN, Book]                               │
│ - members: Dict[id, Member]                             │
│ - active_issues: List[BookIssue]                        │
├─────────────────────────────────────────────────────────┤
│ + searchBooks(query): List[Book]                        │
│ + issueBook(bookCopyId, memberId): BookIssue            │
│ + returnBook(issueId): int  # returns fine              │
│ + reserveBook(bookId, memberId): Reservation            │
│ + addBook(book): void                                   │
└─────────────────────────────────────────────────────────┘

┌─────────────────────┐       ┌─────────────────────┐
│        Book         │       │      BookCopy       │
├─────────────────────┤       ├─────────────────────┤
│ - isbn              │       │ - id                │
│ - title             │ 1:N   │ - book              │
│ - author            │──────▶│ - status            │
│ - publisher         │       │ - rack_location     │
│ - copies[]          │       └─────────────────────┘
│ - reservations[]    │
└─────────────────────┘

┌─────────────────────┐       ┌─────────────────────┐
│       Member        │       │     BookIssue       │
├─────────────────────┤       ├─────────────────────┤
│ - id                │       │ - id                │
│ - name              │ 1:N   │ - book_copy         │
│ - email             │──────▶│ - member            │
│ - membership_type   │       │ - issue_date        │
│ - fine_due          │       │ - due_date          │
│ - issued_books[]    │       │ - return_date       │
└─────────────────────┘       │ - fine_amount       │
                              └─────────────────────┘

┌─────────────────────┐
│    MembershipType   │
├─────────────────────┤
│ - type: STANDARD |  │
│         PREMIUM     │
│ - max_books         │
│ - loan_period_days  │
│ - fine_per_day      │
└─────────────────────┘
```

</details>

---

## Hint 8: Issue and Return Flow

<details>
<summary>Click to reveal</summary>

```python
class Library:
    def issue_book(self, book_copy_id: str, member_id: str) -> BookIssue:
        member = self.members[member_id]
        book_copy = self.get_book_copy(book_copy_id)

        # Validate
        can_issue, reason = member.can_issue_book()
        if not can_issue:
            raise IssueNotAllowedError(reason)

        if book_copy.status != BookCopyStatus.AVAILABLE:
            raise BookNotAvailableError()

        # Create issue
        issue = BookIssue(
            book_copy=book_copy,
            member=member,
            issue_date=date.today(),
            due_date=date.today() + timedelta(days=member.membership_type.loan_period_days)
        )

        # Update states
        book_copy.status = BookCopyStatus.ISSUED
        member.issued_books.append(issue)

        return issue

    def return_book(self, issue_id: str) -> int:
        issue = self.get_issue(issue_id)
        issue.return_date = date.today()

        # Calculate fine
        fine = issue.calculate_fine()
        issue.fine_amount = fine
        issue.member.total_fine_due += fine

        # Check for reservations
        reservations = issue.book_copy.book.get_pending_reservations()
        if reservations:
            # Mark as reserved for next person
            issue.book_copy.status = BookCopyStatus.RESERVED
            self.notify_member(reservations[0].member, "Book available!")
        else:
            issue.book_copy.status = BookCopyStatus.AVAILABLE

        return fine
```

</details>

---

## Hint 9: API Design

<details>
<summary>Click to reveal</summary>

```
# Search
GET    /books?q=harry+potter&author=rowling

# Book details
GET    /books/{isbn}
GET    /books/{isbn}/copies         # Available copies

# Issue/Return
POST   /issues                      # Issue book
       { "book_copy_id": "...", "member_id": "..." }
PUT    /issues/{id}/return          # Return book

# Reservations
POST   /reservations
       { "book_isbn": "...", "member_id": "..." }
DELETE /reservations/{id}           # Cancel reservation

# Member
GET    /members/{id}
GET    /members/{id}/issued-books
GET    /members/{id}/fines
POST   /members/{id}/pay-fine       # Pay fine
```

</details>

---

## Common Mistakes to Avoid

1. **Not separating Book and BookCopy** - This is critical!
2. **Storing issued_books only in Member** - Also track in Library for queries
3. **No reservation queue** - Reservations need ordering
4. **Fine calculation at return only** - Should be calculable anytime
5. **Missing validation** - Check eligibility before issue
