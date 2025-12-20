# Category Guide: Social & Communication Systems

## Overview

Social systems deal with **user-generated content, relationships, and real-time communication**. They test your ability to model feeds, messaging, and notification systems.

---

## Common Entities

| Entity | Purpose | Example |
|--------|---------|---------|
| User | System participant | UserProfile |
| Post/Tweet | User content | Tweet, Post, Message |
| Relationship | User connections | Follow, Friend, Block |
| Feed | Aggregated content | Timeline, News Feed |
| Notification | User alerts | Push, Email, In-app |

---

## Key Design Patterns

### 1. Observer Pattern - For Notifications
```
User posts tweet → Notify all followers
Message received → Notify recipient
```

### 2. Strategy Pattern - For Feed Generation
```
                    ┌───────────────────────┐
                    │   FeedStrategy        │ (ABC)
                    │   + generateFeed()    │
                    └───────────┬───────────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        ▼                       ▼                       ▼
┌───────────────┐      ┌───────────────┐      ┌───────────────┐
│ Chronological │      │   Ranked      │      │   Trending    │
└───────────────┘      └───────────────┘      └───────────────┘
```

### 3. Factory Pattern - For Message Types
```
class MessageFactory:
    def create(type, content):
        if type == "TEXT": return TextMessage(content)
        if type == "IMAGE": return ImageMessage(content)
        if type == "VIDEO": return VideoMessage(content)
```

---

## System 1: Twitter-like

### Class Design
```
┌─────────────────────┐
│        User         │
├─────────────────────┤
│ - id                │
│ - username          │
│ - email             │
│ - bio               │
│ - followers[]       │
│ - following[]       │
│ - tweets[]          │
└─────────────────────┘

┌─────────────────────────┐
│         Tweet           │
├─────────────────────────┤
│ - id                    │
│ - author_id             │
│ - content               │
│ - media[]               │
│ - created_at            │
│ - likes_count           │
│ - retweets_count        │
│ - reply_to_id (nullable)│
│ - hashtags[]            │
│ - mentions[]            │
└─────────────────────────┘

┌─────────────────────────┐
│        Follow           │
├─────────────────────────┤
│ - follower_id           │
│ - followee_id           │
│ - created_at            │
└─────────────────────────┘

┌─────────────────────────┐
│         Like            │
├─────────────────────────┤
│ - user_id               │
│ - tweet_id              │
│ - created_at            │
└─────────────────────────┘
```

### Feed Generation Approaches

**1. Pull Model (Fan-out on Read)**
```python
def get_feed(user_id, limit=20):
    following = get_following(user_id)
    tweets = Tweet.query.filter(
        Tweet.author_id.in_(following)
    ).order_by(Tweet.created_at.desc()).limit(limit)
    return tweets
```
- Pro: Simple, write is fast
- Con: Read is slow for users following many people

**2. Push Model (Fan-out on Write)**
```python
def post_tweet(author_id, content):
    tweet = Tweet.create(author_id, content)
    followers = get_followers(author_id)
    for follower in followers:
        add_to_feed(follower.id, tweet.id)  # Pre-compute feed
```
- Pro: Read is instant
- Con: Write is slow for users with many followers (celebrities)

**3. Hybrid Model**
```
Regular users → Push model
Celebrities (>10K followers) → Pull model on read
```

---

## System 2: Chat/Messenger

### Class Design
```
┌─────────────────────────┐
│      Conversation       │
├─────────────────────────┤
│ - id                    │
│ - type: DIRECT | GROUP  │
│ - participants[]        │
│ - created_at            │
│ - last_message_at       │
└─────────────────────────┘
         │
         ▼
┌─────────────────────────┐
│        Message          │ (ABC)
├─────────────────────────┤
│ - id                    │
│ - conversation_id       │
│ - sender_id             │
│ - content               │
│ - type                  │
│ - status: SENT|DELIVERED│READ
│ - created_at            │
│ - read_by[]             │
└─────────────────────────┘
         △
         │
    ┌────┴────┬────────────┐
    ▼         ▼            ▼
TextMessage ImageMessage FileMessage

┌─────────────────────────┐
│      MessageStatus      │
├─────────────────────────┤
│ - message_id            │
│ - user_id               │
│ - status                │
│ - timestamp             │
└─────────────────────────┘
```

### Message Status Flow
```
SENT → DELIVERED → READ
  │
  ▼
FAILED
```

### Read Receipts (Group Chat)
```python
class Message:
    def mark_read(self, user_id):
        if user_id not in self.read_by:
            self.read_by.append(user_id)
            # Notify sender of read receipt

    def is_read_by_all(self):
        participants = self.conversation.participants
        return set(self.read_by) >= set(participants) - {self.sender_id}
```

---

## Common Pitfalls

| Pitfall | Problem | Solution |
|---------|---------|----------|
| N+1 queries for feed | Slow feed loading | Batch queries, denormalization |
| No message status | Users don't know if delivered | Add status tracking |
| Followers as list in User | Can't scale | Separate Follow table |
| Sync-only messaging | Poor UX | Use WebSocket for real-time |
| No soft delete | Can't implement "delete for me" | Add deleted_for[] field |

---

## Coding Hacks for Demo

### 1. Tweet with Mentions/Hashtags
```python
import re

class Tweet:
    def __init__(self, content):
        self.content = content
        self.mentions = self._extract_mentions()
        self.hashtags = self._extract_hashtags()

    def _extract_mentions(self):
        return re.findall(r'@(\w+)', self.content)

    def _extract_hashtags(self):
        return re.findall(r'#(\w+)', self.content)
```

### 2. Simple Feed Query
```python
def get_timeline(user_id, cursor=None, limit=20):
    following_ids = Follow.query.filter_by(follower_id=user_id).pluck('followee_id')

    query = Tweet.query.filter(Tweet.author_id.in_(following_ids))

    if cursor:
        query = query.filter(Tweet.created_at < cursor)

    return query.order_by(Tweet.created_at.desc()).limit(limit).all()
```

### 3. Message Status Update
```python
def deliver_message(message_id, recipient_id):
    message = Message.get(message_id)
    if message.status == MessageStatus.SENT:
        message.status = MessageStatus.DELIVERED
        notify_sender(message.sender_id, "delivered", message_id)

def mark_read(message_id, reader_id):
    message = Message.get(message_id)
    if reader_id not in message.read_by:
        message.read_by.append(reader_id)
        notify_sender(message.sender_id, "read", message_id)
```

### 4. Online Status
```python
class PresenceManager:
    def __init__(self):
        self.online_users = {}  # user_id -> last_seen

    def heartbeat(self, user_id):
        self.online_users[user_id] = datetime.now()

    def is_online(self, user_id):
        last_seen = self.online_users.get(user_id)
        if not last_seen:
            return False
        return (datetime.now() - last_seen).seconds < 30
```

---

## API Design

### Twitter-like
```
# Tweets
POST   /tweets                    # Create tweet
GET    /tweets/{id}               # Get tweet
DELETE /tweets/{id}               # Delete tweet
POST   /tweets/{id}/like          # Like tweet
POST   /tweets/{id}/retweet       # Retweet

# Feed
GET    /feed                      # Get home timeline
GET    /users/{id}/tweets         # Get user's tweets

# Follow
POST   /users/{id}/follow         # Follow user
DELETE /users/{id}/follow         # Unfollow
GET    /users/{id}/followers      # List followers
GET    /users/{id}/following      # List following

# Search
GET    /search/tweets?q=keyword   # Search tweets
GET    /search/users?q=name       # Search users
```

### Messenger
```
# Conversations
GET    /conversations             # List conversations
POST   /conversations             # Create conversation
GET    /conversations/{id}        # Get conversation

# Messages
GET    /conversations/{id}/messages  # Get messages
POST   /conversations/{id}/messages  # Send message
PUT    /messages/{id}/read           # Mark as read

# Real-time (WebSocket)
WS     /ws/chat                   # Real-time messaging
```

### Tweet Response
```json
{
    "id": "tweet-123",
    "author": {
        "id": "user-1",
        "username": "johndoe",
        "avatar": "..."
    },
    "content": "Hello #world @jane",
    "media": [],
    "hashtags": ["world"],
    "mentions": ["jane"],
    "likes_count": 42,
    "retweets_count": 5,
    "replies_count": 3,
    "created_at": "2024-01-15T10:30:00Z"
}
```

---

## Interview Questions to Expect

1. "How would you handle **celebrity tweets** (millions of followers)?"
   → Hybrid push/pull, async fan-out, eventual consistency

2. "How to implement **typing indicator**?"
   → WebSocket events, throttle to avoid spam

3. "How would you implement **message search**?"
   → Full-text search index (Elasticsearch), index on send

4. "How to handle **offline messages**?"
   → Queue messages, deliver on reconnect, store last_seen

5. "How to implement **hashtag trending**?"
   → Count hashtags in sliding window, rank by velocity

---

## Checklist Before Interview

- [ ] Can explain feed generation (push vs pull)
- [ ] Know how to model follows (separate table)
- [ ] Understand message status flow
- [ ] Can design conversation (direct + group)
- [ ] Know real-time architecture (WebSocket)
- [ ] Can handle message delivery guarantees
- [ ] Understand presence/online status
