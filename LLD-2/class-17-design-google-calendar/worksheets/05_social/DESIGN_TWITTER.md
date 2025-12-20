# Design Twitter

- [Design Twitter](#design-twitter)
  - [Overview](#overview)
  - [Expectations](#expectations)
  - [Requirements Gathering](#requirements-gathering)
  - [Requirements](#requirements)
  - [Use Case Diagrams](#use-case-diagrams)
  - [Class Diagram](#class-diagram)
  - [Key Design Decisions](#key-design-decisions)
  - [API Design](#api-design)

---

## Overview

Twitter is a social media platform where users can post short messages (tweets), follow other users, and see a feed of tweets from people they follow. Core features include posting, liking, retweeting, replying, and following.

**Key Features:**
- Post tweets (text, images, videos)
- Follow/unfollow users
- Like and retweet
- Reply to tweets (threads)
- Home feed (timeline)
- Search (users, tweets, hashtags)
- Notifications

---

## Expectations

* Code should be functionally correct.
* Code should be modular and readable. Clean and professional level code.
* Code should be extensible and scalable. Means it should be able to accommodate new requirements with minimal changes.
* Code should have good OOP design principles.

---

## Requirements Gathering

What are some questions you would ask to gather requirements?

```
1.
2.
3.
4.
5.
```

<details>
<summary><strong>Sample clarifying questions</strong></summary>

1. What is the character limit for tweets?
2. Can users upload media (images, videos)?
3. Can users edit tweets after posting?
4. How is the feed generated? (Chronological or ranked?)
5. Can users block or mute other users?
6. Are there verified accounts?
7. Can users send direct messages?
8. How are hashtags and mentions handled?

</details>

---

## Requirements

What will be 8-10 requirements of the system, according to you?

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
<summary><strong>Click to see the actual requirements</strong></summary>

1. Users can post tweets (max 280 characters).
2. Users can follow/unfollow other users.
3. Users can see a home feed with tweets from followed users.
4. Users can like tweets.
5. Users can retweet (share) tweets.
6. Users can reply to tweets (creating threads).
7. Tweets can contain hashtags (#topic) and mentions (@user).
8. Users can search for tweets, users, and hashtags.
9. System should track tweet engagement (likes, retweets, replies).
10. Users receive notifications for likes, retweets, mentions.

</details>

---

## Use Case Diagrams

### Actors

What would be the actors in this system?

```
1.
2.
```

### Use Cases

#### Actor 1

Name of the actor - ` `

Use cases:
```
1.
2.
3.
4.
5.
6.
```

**Create a use case diagram for the system.**

```



```

---

## Class Diagram

What will be the major classes and their attributes?

**Think about:**
- How to model a tweet? (original, reply, retweet)
- How to model the follow relationship?
- How to extract hashtags and mentions?
- How to model the feed?

List down your classes:

```
Class 1:

Class 2:

Class 3:

Class 4:

Class 5:
```

**Design Question: How to model Retweet?**
```
Option A: Retweet is a new Tweet with reference to original
Option B: Separate Retweet entity
Option C: Just a counter on the original tweet

Your choice and reasoning:

```

List down the relationships between classes:

```
1.
2.
3.
4.
```

Draw the class diagram:

```




```

---

## Key Design Decisions

**1. Feed Generation: Pull vs Push?**
```
Pull: Calculate feed when user opens app
Push: Pre-compute feed when someone tweets

Which would you choose? Why?

```

**2. How to handle celebrities (millions of followers)?**
```
Your approach:

```

**3. How to implement hashtag trending?**
```
Your approach:

```

---

## API Design

What APIs would you design for this system?

```
1.
2.
3.
4.
5.
6.
7.
```

---

## Hints

See [HINTS_TWITTER.md](./HINTS_TWITTER.md) for detailed hints after attempting.
