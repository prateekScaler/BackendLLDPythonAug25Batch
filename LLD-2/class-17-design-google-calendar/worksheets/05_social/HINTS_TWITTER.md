# Hints: Twitter

## Hint 1: Actors

<details>
<summary>Click to reveal</summary>

1. **User** - Post, like, follow, view feed
2. **System** - Generate feed, track trends, send notifications

</details>

---

## Hint 2: Tweet Types

<details>
<summary>Click to reveal</summary>

**Three types of tweets:**

```python
class TweetType(Enum):
    ORIGINAL = "original"   # Regular tweet
    REPLY = "reply"         # Reply to another tweet
    RETWEET = "retweet"     # Sharing someone's tweet
```

**Single Tweet class with optional fields:**
```python
class Tweet:
    id: str
    author_id: str
    content: str
    type: TweetType
    created_at: datetime

    # For replies
    reply_to_id: Optional[str]  # Parent tweet

    # For retweets
    retweet_of_id: Optional[str]  # Original tweet

    # Extracted from content
    hashtags: List[str]
    mentions: List[str]

    # Counters (denormalized for performance)
    likes_count: int
    retweets_count: int
    replies_count: int
```

</details>

---

## Hint 3: Follow Relationship

<details>
<summary>Click to reveal</summary>

**Never store followers as a list inside User!**

❌ Bad:
```python
class User:
    followers: List[User]  # Won't scale!
```

✅ Good - Separate Follow entity:
```python
class Follow:
    follower_id: str    # Who is following
    followee_id: str    # Who is being followed
    created_at: datetime

# Queries become simple:
# Get followers: SELECT * FROM follows WHERE followee_id = X
# Get following: SELECT * FROM follows WHERE follower_id = X
```

</details>

---

## Hint 4: Like Entity

<details>
<summary>Click to reveal</summary>

```python
class Like:
    user_id: str
    tweet_id: str
    created_at: datetime

    # Unique constraint on (user_id, tweet_id)
```

**Why separate entity?**
- Can query "who liked this tweet"
- Can query "all tweets user liked"
- Easy to unlike (delete record)
- Tweet's `likes_count` is denormalized for display

</details>

---

## Hint 5: Class Diagram

<details>
<summary>Click to reveal</summary>

```
┌─────────────────────────────────────────────────────────┐
│                        User                              │
├─────────────────────────────────────────────────────────┤
│ - id: str                                                │
│ - username: str                                          │
│ - email: str                                             │
│ - bio: str                                               │
│ - profile_image: str                                     │
│ - created_at: datetime                                   │
│ - followers_count: int  (denormalized)                   │
│ - following_count: int  (denormalized)                   │
├─────────────────────────────────────────────────────────┤
│ + postTweet(content): Tweet                              │
│ + follow(userId): void                                   │
│ + unfollow(userId): void                                 │
│ + like(tweetId): void                                    │
│ + retweet(tweetId): Tweet                                │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                        Tweet                             │
├─────────────────────────────────────────────────────────┤
│ - id: str                                                │
│ - author_id: str                                         │
│ - content: str (max 280)                                 │
│ - type: TweetType                                        │
│ - reply_to_id: Optional[str]                             │
│ - retweet_of_id: Optional[str]                           │
│ - hashtags: List[str]                                    │
│ - mentions: List[str]                                    │
│ - media: List[Media]                                     │
│ - created_at: datetime                                   │
│ - likes_count: int                                       │
│ - retweets_count: int                                    │
│ - replies_count: int                                     │
└─────────────────────────────────────────────────────────┘

┌───────────────────┐  ┌───────────────────┐
│      Follow       │  │       Like        │
├───────────────────┤  ├───────────────────┤
│ - follower_id     │  │ - user_id         │
│ - followee_id     │  │ - tweet_id        │
│ - created_at      │  │ - created_at      │
└───────────────────┘  └───────────────────┘

┌───────────────────┐
│     Hashtag       │
├───────────────────┤
│ - tag: str        │
│ - tweet_count: int│
│ - recent_tweets[] │
└───────────────────┘
```

</details>

---

## Hint 6: Feed Generation

<details>
<summary>Click to reveal</summary>

**Pull Model (Fan-out on Read):**
```python
def get_feed(user_id, limit=20):
    following_ids = get_following_ids(user_id)
    tweets = Tweet.query.filter(
        Tweet.author_id.in_(following_ids)
    ).order_by(Tweet.created_at.desc()).limit(limit)
    return tweets
```
- Simple
- Slow for users following many people
- Always fresh

**Push Model (Fan-out on Write):**
```python
def post_tweet(author_id, content):
    tweet = Tweet.create(author_id, content)
    followers = get_followers(author_id)
    for follower in followers:
        FeedItem.create(follower.id, tweet.id)  # Pre-compute

def get_feed(user_id, limit=20):
    return FeedItem.query.filter(user_id=user_id).limit(limit)
```
- Fast reads
- Slow writes for celebrities
- Storage heavy

**Hybrid (Recommended):**
```
Regular users: Push model
Celebrities (>10K followers): Pull model on read
```

</details>

---

## Hint 7: Hashtag Extraction

<details>
<summary>Click to reveal</summary>

```python
import re

class Tweet:
    def __init__(self, content):
        self.content = content
        self.hashtags = self._extract_hashtags()
        self.mentions = self._extract_mentions()

    def _extract_hashtags(self):
        return re.findall(r'#(\w+)', self.content)

    def _extract_mentions(self):
        return re.findall(r'@(\w+)', self.content)

# Example:
# "Hello @john, check out #Python #coding"
# hashtags = ["Python", "coding"]
# mentions = ["john"]
```

</details>

---

## Hint 8: Trending Hashtags

<details>
<summary>Click to reveal</summary>

```python
class TrendingService:
    def __init__(self):
        # Sliding window: last 1 hour
        self.window_size = 3600  # seconds
        self.hashtag_counts = defaultdict(int)

    def record_hashtag(self, hashtag, timestamp):
        # Use time-bucketed counting
        bucket = timestamp // 60  # per-minute buckets
        key = f"{hashtag}:{bucket}"
        self.hashtag_counts[key] += 1

    def get_trending(self, limit=10):
        current_bucket = int(time.time()) // 60
        counts = defaultdict(int)

        # Sum last 60 buckets (1 hour)
        for bucket in range(current_bucket - 60, current_bucket + 1):
            for hashtag, count in self.hashtag_counts.items():
                if hashtag.endswith(f":{bucket}"):
                    tag = hashtag.split(":")[0]
                    counts[tag] += count

        return sorted(counts.items(), key=lambda x: -x[1])[:limit]
```

</details>

---

## Hint 9: API Design

<details>
<summary>Click to reveal</summary>

```
# Tweets
POST   /tweets                       # Create tweet
GET    /tweets/{id}                  # Get tweet
DELETE /tweets/{id}                  # Delete tweet

# Feed
GET    /feed?cursor=xxx&limit=20     # Get home timeline

# User actions
POST   /tweets/{id}/like             # Like
DELETE /tweets/{id}/like             # Unlike
POST   /tweets/{id}/retweet          # Retweet
POST   /tweets/{id}/reply            # Reply
       { "content": "..." }

# Follow
POST   /users/{id}/follow
DELETE /users/{id}/follow
GET    /users/{id}/followers
GET    /users/{id}/following

# Search
GET    /search/tweets?q=keyword
GET    /search/users?q=name
GET    /hashtags/{tag}/tweets

# Trending
GET    /trending
```

**Tweet Response:**
```json
{
    "id": "tweet-123",
    "author": {
        "id": "user-1",
        "username": "johndoe",
        "profile_image": "..."
    },
    "content": "Hello #world @jane",
    "type": "original",
    "hashtags": ["world"],
    "mentions": ["jane"],
    "likes_count": 42,
    "retweets_count": 5,
    "replies_count": 3,
    "liked_by_me": false,
    "retweeted_by_me": false,
    "created_at": "2024-01-15T10:30:00Z"
}
```

</details>

---

## Common Mistakes to Avoid

1. **Followers as list in User** - Use separate Follow entity
2. **No denormalization** - Store counts for performance
3. **Fetching full tweet for feed** - Use projections
4. **Not handling replies as tree** - Track parent_id for threads
5. **Single feed approach** - Use hybrid for celebrities
