# Design Chat/Messenger System

## Overview

A messaging system allows users to send messages to each other in real-time. It supports direct messages, group chats, message status tracking (sent/delivered/read), and media sharing.

**Key Features:**
- Direct messaging (1:1)
- Group chats
- Message status (sent → delivered → read)
- Media attachments
- Online/typing indicators

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

1. Real-time or polling based?
2. Message size limits?
3. Group size limits?
4. Message editing/deletion?
5. End-to-end encryption?
6. Offline message queueing?
7. Read receipts required?

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

1. Users can send text messages to other users.
2. Users can create group conversations.
3. Messages have status: sent, delivered, read.
4. Users can see when others are typing.
5. Users can share media (images, files).
6. Messages persist and sync across devices.
7. Users can see online status of others.
8. Support for message deletion.

</details>

---

## Class Diagram

**Think about:**
- Conversation (Direct vs Group)
- Message types (Text, Image, File)
- Message status tracking per recipient
- Participant management

**Design Question: Message Status in Groups**
```
Group has 5 members. How to track who has read?

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

**1. Conversation Model**
```
Direct chat vs Group chat - same or different class?

Your approach:

```

**2. Message Delivery**
```
User is offline. How to ensure they get message later?

```

**3. Real-time Updates**
```
How to push new messages to connected clients?

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
<summary><strong>Hint 1: Conversation Model</strong></summary>

```python
class ConversationType(Enum):
    DIRECT = "direct"
    GROUP = "group"

class Conversation:
    id: str
    type: ConversationType
    participants: List[str]  # user_ids
    created_at: datetime
    last_message_at: datetime

    # For groups
    name: Optional[str]
    admin_ids: List[str]
```

</details>

<details>
<summary><strong>Hint 2: Message with Status</strong></summary>

```python
class MessageStatus(Enum):
    SENT = "sent"          # Server received
    DELIVERED = "delivered" # Recipient's device received
    READ = "read"          # Recipient opened

class Message:
    id: str
    conversation_id: str
    sender_id: str
    content: str
    type: MessageType  # TEXT, IMAGE, FILE
    created_at: datetime
    # For media
    media_url: Optional[str]

class MessageReceipt:
    """Track status per recipient (for groups)"""
    message_id: str
    user_id: str
    status: MessageStatus
    updated_at: datetime
```

</details>

<details>
<summary><strong>Hint 3: Class Structure</strong></summary>

```
┌─────────────────────────┐
│     Conversation        │
├─────────────────────────┤
│ - id                    │
│ - type: DIRECT|GROUP    │
│ - participants[]        │
│ - name (groups)         │
│ - last_message_at       │
├─────────────────────────┤
│ + addParticipant()      │
│ + removeParticipant()   │
│ + getMessages()         │
└─────────────────────────┘
         │
         │ 1:N
         ▼
┌─────────────────────────┐
│        Message          │ (ABC)
├─────────────────────────┤
│ - id                    │
│ - conversation_id       │
│ - sender_id             │
│ - created_at            │
│ - is_deleted            │
└─────────────────────────┘
         △
         │
    ┌────┴────┬──────────┐
    ▼         ▼          ▼
TextMessage ImageMsg  FileMessage
- content   - url     - url
            - caption - filename
                      - size

┌─────────────────────────┐
│    MessageReceipt       │
├─────────────────────────┤
│ - message_id            │
│ - user_id               │
│ - status                │
│ - timestamp             │
└─────────────────────────┘
```

</details>

<details>
<summary><strong>Hint 4: Online & Typing Status</strong></summary>

```python
class PresenceService:
    # In-memory or Redis
    online_users: Dict[str, datetime]  # user_id -> last_seen
    typing_users: Dict[str, Set[str]]  # conversation_id -> {user_ids}

    def heartbeat(self, user_id):
        self.online_users[user_id] = datetime.now()

    def is_online(self, user_id) -> bool:
        last_seen = self.online_users.get(user_id)
        if not last_seen:
            return False
        return (datetime.now() - last_seen).seconds < 30

    def set_typing(self, conversation_id, user_id):
        self.typing_users[conversation_id].add(user_id)
        # Auto-clear after 3 seconds

    def get_typing_users(self, conversation_id) -> Set[str]:
        return self.typing_users.get(conversation_id, set())
```

</details>

<details>
<summary><strong>Hint 5: API Design</strong></summary>

```
# REST APIs
GET  /conversations                    # List user's conversations
POST /conversations                    # Create conversation
GET  /conversations/{id}/messages      # Get messages (paginated)
POST /conversations/{id}/messages      # Send message

# Message status
PUT  /messages/{id}/delivered          # Mark delivered
PUT  /messages/{id}/read               # Mark read

# WebSocket Events (Real-time)
→ new_message          # Incoming message
→ message_status       # Status update
→ typing_start         # User started typing
→ typing_stop          # User stopped typing
→ presence_update      # Online/offline
```

</details>
