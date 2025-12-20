# Design File Storage System (Dropbox/Google Drive)

## Overview

A file storage system allows users to upload, organize, and share files in the cloud. It supports folder hierarchies, file versioning, and collaboration through sharing.

**Key Features:**
- Upload/download files
- Create folder hierarchy
- Share files/folders
- Version history
- Sync across devices

---

## Expectations

* Code should be functionally correct.
* Code should be modular and readable.
* Code should be extensible and scalable.
* Code should have good OOP design principles.

---

## Requirements Gathering

```
1.
2.
3.
4.
5.
```

<details>
<summary><strong>Sample clarifying questions</strong></summary>

1. File size limits?
2. Storage quota per user?
3. How many versions to keep?
4. Share with view-only or edit access?
5. Public shareable links?
6. Trash/recycle bin?
7. Real-time collaboration?

</details>

---

## Requirements

```
1.
2.
3.
4.
5.
6.
7.
8.
```

<details>
<summary><strong>Click to see requirements</strong></summary>

1. Users can upload files.
2. Users can create folders.
3. Users can organize files into folders.
4. Users can share files/folders with others.
5. Sharing can be view-only or edit access.
6. System maintains version history.
7. Users can restore previous versions.
8. Deleted files go to trash (recoverable).

</details>

---

## Class Diagram

**Think about:**
- File and Folder - same base class? (Composite pattern)
- Sharing and permissions
- Version tracking
- Path resolution

**Design Question: Composite Pattern**
```
Should File and Folder share a base class?
What operations are common?

Your approach:

```

List your classes:

```
Class 1:

Class 2:

Class 3:

Class 4:

Class 5:
```

Draw the class diagram:

```




```

---

## Key Design Decisions

**1. Path Storage**
```
Option A: Store full path string "/docs/work/report.pdf"
Option B: Store parent_id reference

Tradeoffs?

```

**2. File Deduplication**
```
Same file uploaded twice. Store twice?

Your approach:

```

**3. Large File Upload**
```
User uploads 2GB file. How to handle?

```

---

## API Design

```
1.
2.
3.
4.
5.
```

---

## Hints

<details>
<summary><strong>Hint 1: Composite Pattern</strong></summary>

```python
class FileSystemItem(ABC):
    id: str
    name: str
    owner_id: str
    parent_id: Optional[str]  # None for root
    created_at: datetime
    modified_at: datetime
    is_deleted: bool
    deleted_at: Optional[datetime]

    @abstractmethod
    def get_size(self) -> int:
        pass

    def get_path(self) -> str:
        if self.parent_id is None:
            return "/" + self.name
        parent = FileSystemItem.get(self.parent_id)
        return parent.get_path() + "/" + self.name

class File(FileSystemItem):
    content_hash: str  # For deduplication
    size: int
    mime_type: str
    versions: List[FileVersion]

    def get_size(self) -> int:
        return self.size

class Folder(FileSystemItem):
    def get_size(self) -> int:
        children = FileSystemItem.get_children(self.id)
        return sum(child.get_size() for child in children)
```

</details>

<details>
<summary><strong>Hint 2: Sharing Model</strong></summary>

```python
class Permission(Enum):
    VIEW = "view"
    EDIT = "edit"
    OWNER = "owner"

class Share:
    id: str
    item_id: str  # File or Folder
    shared_with_id: str  # User ID
    permission: Permission
    shared_by_id: str
    created_at: datetime

class PublicLink:
    id: str
    item_id: str
    token: str  # Random URL-safe token
    permission: Permission
    expires_at: Optional[datetime]
    password: Optional[str]
```

</details>

<details>
<summary><strong>Hint 3: Version History</strong></summary>

```python
class FileVersion:
    id: str
    file_id: str
    version_number: int
    content_hash: str
    size: int
    created_at: datetime
    created_by: str

class File:
    def upload_new_version(self, content, user_id):
        new_version = FileVersion(
            file_id=self.id,
            version_number=len(self.versions) + 1,
            content_hash=hash(content),
            created_by=user_id
        )
        self.versions.append(new_version)
        self.content_hash = new_version.content_hash
        self.modified_at = datetime.now()

    def restore_version(self, version_number):
        version = self.versions[version_number - 1]
        self.upload_new_version(
            get_content(version.content_hash),
            current_user.id
        )
```

</details>

<details>
<summary><strong>Hint 4: Class Diagram</strong></summary>

```
┌─────────────────────────────┐
│   FileSystemItem (ABC)      │
├─────────────────────────────┤
│ - id                        │
│ - name                      │
│ - owner_id                  │
│ - parent_id                 │
│ - created_at                │
│ - is_deleted                │
├─────────────────────────────┤
│ + getPath()                 │
│ + getSize()                 │
│ + move(newParent)           │
│ + rename(newName)           │
│ + delete()                  │
└─────────────────────────────┘
              △
              │
       ┌──────┴──────┐
       ▼             ▼
┌─────────────┐ ┌─────────────┐
│    File     │ │   Folder    │
├─────────────┤ ├─────────────┤
│- content_hash│ │             │
│- size        │ ├─────────────┤
│- mime_type   │ │+ getChildren│
│- versions[]  │ │+ addChild() │
└─────────────┘ └─────────────┘

┌─────────────────┐   ┌─────────────────┐
│     Share       │   │   FileVersion   │
├─────────────────┤   ├─────────────────┤
│ - item_id       │   │ - file_id       │
│ - shared_with   │   │ - version_num   │
│ - permission    │   │ - content_hash  │
│ - created_at    │   │ - created_at    │
└─────────────────┘   └─────────────────┘
```

</details>
