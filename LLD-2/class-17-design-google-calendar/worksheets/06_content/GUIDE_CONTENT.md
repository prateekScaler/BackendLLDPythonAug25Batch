# Category Guide: Content & Media Management

## Overview

Content management systems deal with **organizing, storing, and providing access to digital content**. They test hierarchical data structures, access control, and search capabilities.

---

## Common Entities

| Entity | Purpose | Example |
|--------|---------|---------|
| Content | The managed item | Book, File, Document |
| Container | Groups content | Folder, Category, Shelf |
| User | System participant | Member, Admin |
| Access | Permission control | Read, Write, Share |
| Metadata | Content description | Tags, Author, Size |

---

## Key Design Patterns

### 1. Composite Pattern - For Hierarchical Content
```
                    ┌───────────────────────┐
                    │   FileSystemItem      │ (ABC)
                    │   + getName()         │
                    │   + getSize()         │
                    └───────────┬───────────┘
                                │
                ┌───────────────┴───────────────┐
                ▼                               ▼
        ┌───────────────┐              ┌───────────────┐
        │     File      │              │    Folder     │
        ├───────────────┤              ├───────────────┤
        │ - content     │              │ - children[]  │
        │ + getSize()   │              │ + add()       │
        └───────────────┘              │ + remove()    │
                                       │ + getSize()   │ ← Sum of children
                                       └───────────────┘
```

### 2. Strategy Pattern - For Search
```
                    ┌───────────────────────┐
                    │   SearchStrategy      │ (ABC)
                    │   + search(query)     │
                    └───────────┬───────────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        ▼                       ▼                       ▼
┌───────────────┐      ┌───────────────┐      ┌───────────────┐
│  TitleSearch  │      │ ContentSearch │      │   TagSearch   │
└───────────────┘      └───────────────┘      └───────────────┘
```

### 3. Observer Pattern - For Sync
```
File modified → Notify all subscribers → Sync to their devices
```

---

## System 1: Library Management

### Class Design
```
┌─────────────────────────┐
│        Library          │
├─────────────────────────┤
│ - id                    │
│ - name                  │
│ - address               │
│ - books[]               │
│ - members[]             │
│ + addBook()             │
│ + registerMember()      │
└─────────────────────────┘

┌─────────────────────────┐
│          Book           │
├─────────────────────────┤
│ - isbn                  │
│ - title                 │
│ - author                │
│ - publisher             │
│ - copies[]              │
└─────────────────────────┘
         │
         ▼
┌─────────────────────────┐
│       BookCopy          │
├─────────────────────────┤
│ - id                    │
│ - book_id               │
│ - rack_location         │
│ - status: AVAILABLE |   │
│   ISSUED | RESERVED |   │
│   LOST                  │
└─────────────────────────┘

┌─────────────────────────┐
│        Member           │
├─────────────────────────┤
│ - id                    │
│ - name                  │
│ - email                 │
│ - membership_type       │
│ - issued_books[]        │
│ - max_books_allowed     │
│ + issueBook()           │
│ + returnBook()          │
│ + reserveBook()         │
└─────────────────────────┘

┌─────────────────────────┐
│      BookIssue          │
├─────────────────────────┤
│ - id                    │
│ - book_copy_id          │
│ - member_id             │
│ - issue_date            │
│ - due_date              │
│ - return_date           │
│ - fine_amount           │
└─────────────────────────┘
```

### Book vs BookCopy
```
Book (ISBN: 978-0-13-468599-1)
├── Copy 1 (Available, Rack A-15)
├── Copy 2 (Issued to Member #123)
├── Copy 3 (Reserved by Member #456)
└── Copy 4 (Lost)

Book = The title/metadata
BookCopy = Physical instance
```

---

## System 2: File Storage (Dropbox-like)

### Class Design
```
┌─────────────────────────┐
│   FileSystemItem (ABC)  │
├─────────────────────────┤
│ - id                    │
│ - name                  │
│ - owner_id              │
│ - parent_id             │
│ - created_at            │
│ - modified_at           │
│ + getPath()             │
│ + getSize()             │
│ + move(newParent)       │
│ + rename(newName)       │
└─────────────────────────┘
         △
         │
    ┌────┴────────────────┐
    ▼                     ▼
┌───────────────┐   ┌─────────────────────┐
│     File      │   │       Folder        │
├───────────────┤   ├─────────────────────┤
│ - content_hash│   │ - children[]        │
│ - size        │   ├─────────────────────┤
│ - mime_type   │   │ + addChild()        │
│ - versions[]  │   │ + removeChild()     │
└───────────────┘   │ + getSize()         │
                    │ + listContents()    │
                    └─────────────────────┘

┌─────────────────────────┐
│       FileVersion       │
├─────────────────────────┤
│ - id                    │
│ - file_id               │
│ - version_number        │
│ - content_hash          │
│ - size                  │
│ - created_at            │
│ - created_by            │
└─────────────────────────┘

┌─────────────────────────┐
│        Share            │
├─────────────────────────┤
│ - id                    │
│ - item_id               │
│ - shared_with           │
│ - permission: VIEW|EDIT │
│ - share_link (optional) │
│ - expires_at            │
└─────────────────────────┘
```

### Path Resolution
```python
class FileSystemItem:
    def get_path(self):
        if self.parent_id is None:
            return "/" + self.name
        parent = FileSystemItem.get(self.parent_id)
        return parent.get_path() + "/" + self.name

# /root/documents/work/report.pdf
```

---

## Common Pitfalls

| Pitfall | Problem | Solution |
|---------|---------|----------|
| Book = BookCopy | Can't track multiple copies | Separate entities |
| No versioning | Can't recover old versions | Store FileVersion |
| Path as string | Hard to move/rename | Store parent_id reference |
| Recursive size calc | Slow for deep folders | Cache folder sizes |
| No soft delete | Permanent deletion | Add `is_deleted` + `deleted_at` |

---

## Coding Hacks for Demo

### 1. Fine Calculation (Library)
```python
class BookIssue:
    FINE_PER_DAY = 5  # rupees

    def calculate_fine(self):
        if self.return_date is None:
            return_date = date.today()
        else:
            return_date = self.return_date

        if return_date <= self.due_date:
            return 0

        overdue_days = (return_date - self.due_date).days
        return overdue_days * self.FINE_PER_DAY
```

### 2. Check Issue Eligibility
```python
class Member:
    def can_issue_book(self):
        if len(self.issued_books) >= self.max_books_allowed:
            return False, "Max limit reached"
        if self.has_overdue_books():
            return False, "Return overdue books first"
        if self.outstanding_fine > 0:
            return False, "Pay pending fine"
        return True, "OK"
```

### 3. Folder Size (Composite)
```python
class Folder(FileSystemItem):
    def get_size(self):
        total = 0
        for child in self.children:
            total += child.get_size()  # Recursive for folders, direct for files
        return total
```

### 4. File Deduplication
```python
class FileStorage:
    def upload(self, content, filename, folder_id):
        content_hash = hashlib.sha256(content).hexdigest()

        # Check if content already exists
        existing = ContentBlock.get_by_hash(content_hash)
        if existing:
            # Just create file metadata pointing to existing content
            return File.create(filename, folder_id, content_hash)

        # Upload new content
        ContentBlock.create(content_hash, content)
        return File.create(filename, folder_id, content_hash)
```

### 5. Share Link Generation
```python
class Share:
    @classmethod
    def create_public_link(cls, item_id, expires_in_days=7):
        token = secrets.token_urlsafe(32)
        return cls.create(
            item_id=item_id,
            share_link=token,
            permission=Permission.VIEW,
            expires_at=datetime.now() + timedelta(days=expires_in_days)
        )

    def get_public_url(self):
        return f"https://drive.example.com/s/{self.share_link}"
```

---

## API Design

### Library Management
```
# Books
GET    /books                      # Search/list books
GET    /books/{isbn}               # Get book details
GET    /books/{isbn}/copies        # Get copy availability

# Members
POST   /members                    # Register member
GET    /members/{id}               # Get member details
GET    /members/{id}/issued        # Get issued books

# Issue/Return
POST   /issues                     # Issue book
PUT    /issues/{id}/return         # Return book
POST   /reservations               # Reserve book
```

### File Storage
```
# Files/Folders
GET    /files/{id}                 # Get file/folder details
POST   /files                      # Upload file
POST   /folders                    # Create folder
PUT    /files/{id}                 # Update/rename
DELETE /files/{id}                 # Delete (soft)
PUT    /files/{id}/move            # Move to different folder

# Versions
GET    /files/{id}/versions        # List versions
GET    /files/{id}/versions/{v}    # Get specific version
POST   /files/{id}/restore/{v}     # Restore version

# Sharing
POST   /files/{id}/share           # Share with user
GET    /files/{id}/shares          # List shares
DELETE /shares/{id}                # Remove share
POST   /files/{id}/share-link      # Create public link
```

### Issue Book Request
```json
POST /issues
{
    "book_copy_id": "copy-123",
    "member_id": "member-456"
}

Response:
{
    "issue_id": "issue-789",
    "book": {"title": "...", "isbn": "..."},
    "member": {"name": "..."},
    "issue_date": "2024-01-15",
    "due_date": "2024-01-29"
}
```

---

## Interview Questions to Expect

1. "How would you implement **book search**?"
   → Full-text search on title/author, filters for availability

2. "How to handle **concurrent reservations**?"
   → Queue-based, first-come-first-serve, notify on availability

3. "How would you implement **file sync** across devices?"
   → Track file changes with timestamps, sync deltas

4. "How to handle **large file uploads**?"
   → Chunked upload, resume capability, content-addressable storage

5. "How to implement **trash/recycle bin**?"
   → Soft delete with `deleted_at`, restore within 30 days

---

## Checklist Before Interview

- [ ] Understand Book vs BookCopy distinction
- [ ] Can implement Composite pattern for files/folders
- [ ] Know fine calculation logic
- [ ] Can design sharing with permissions
- [ ] Understand file versioning
- [ ] Know path resolution approach
- [ ] Can explain deduplication concept
