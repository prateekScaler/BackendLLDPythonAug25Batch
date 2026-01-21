# Email Service - Intro to Message Queues

A comprehensive teaching package for understanding message queues, asynchronous architecture, and building email notification services.

## Contents

```
message-queues-email-service/
├── index.html                          # Interactive HTML guide (main teaching material)
├── docs/
│   ├── theory-message-queues.md        # Theory on message queues
│   └── kafka-email-integration-guide.md # Step-by-step Kafka integration guide
├── diagrams/
│   └── *.svg                           # Architecture diagrams
└── email_notification_project/         # Working Django + Kafka project
    ├── README.md                       # Project-specific instructions
    ├── docker-compose.yml              # Kafka + MailHog setup
    ├── email_consumer.py               # Email consumer service
    └── ...                             # Django project files
```

## How to Use This Package

### 1. Teaching / Learning

**Open `index.html` in a browser** for an interactive learning experience with:
- Expandable sections
- Thinking questions that lead to next topics
- Architecture diagrams
- Code examples

### 2. Reference Documentation

- **`docs/theory-message-queues.md`** - Complete theory on synchronous vs async, message queues, Kafka
- **`docs/kafka-email-integration-guide.md`** - Step-by-step guide to build the project

### 3. Hands-On Practice

**Run the demo project:**

```bash
cd email_notification_project

# Start Kafka and MailHog
docker-compose up -d

# In terminal 1: Start Django
python manage.py runserver

# In terminal 2: Start Email Consumer
python email_consumer.py

# Test it
curl -X POST http://localhost:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "name": "John"}'

# View email at http://localhost:8025
```

## Topics Covered

1. **Synchronous vs Asynchronous Architecture**
   - Why async is needed
   - Comparison with real-world examples

2. **Basic Async Approaches**
   - Background threads
   - Database queues
   - Polling

3. **Message Queues**
   - What they are
   - How they help
   - Throttling and backpressure

4. **Types of Message Queues**
   - Simple queues (SQS, RabbitMQ)
   - Pub/Sub (Redis, Google Pub/Sub)
   - Log-based (Kafka, Kinesis)

5. **Apache Kafka Architecture**
   - Topics
   - Partitions
   - Producers
   - Consumers & Consumer Groups
   - Brokers

6. **Real-World Examples**
   - YouTube video upload
   - E-commerce order flow

7. **Notification Services**
   - Multi-channel notifications
   - Routing and templating
   - Rate limiting

8. **Hands-On Project**
   - Django REST API
   - Kafka integration
   - Email consumer service
   - SMTP setup

## External Resources

- [Kafka Visualization Tool](https://softwaremill.com/kafka-visualisation/)
- [Apache Kafka Documentation](https://kafka.apache.org/documentation/)
- [Confluent Kafka Tutorials](https://developer.confluent.io/tutorials/)

## Prerequisites

- Python 3.8+
- Docker and Docker Compose
- Basic understanding of REST APIs
- Familiarity with Django (helpful but not required)

## Quick Start Commands

```bash
# Clone/navigate to this directory
cd message-queues-email-service

# Open interactive guide
open index.html  # macOS
# or
xdg-open index.html  # Linux
# or just open in browser

# Run the project
cd email_notification_project
docker-compose up -d
pip install -r requirements.txt
python manage.py runserver
# In another terminal:
python email_consumer.py
```
