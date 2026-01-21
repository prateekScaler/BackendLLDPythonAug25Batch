# Email Notification Service - Demo Project

A demonstration project showing how to build an asynchronous email notification service using Django, Apache Kafka, and SMTP.

## Architecture

```
┌──────────────┐      ┌─────────────┐      ┌──────────────┐      ┌────────────┐
│   Django     │      │   Kafka     │      │   Email      │      │   SMTP     │
│   API        │─────>│   Broker    │─────>│   Consumer   │─────>│   Server   │
│              │      │             │      │              │      │            │
│ POST /signup │      │ Topic:      │      │ Sends email  │      │ MailHog/   │
│ POST /order  │      │ email-topic │      │ via SMTP     │      │ Gmail      │
└──────────────┘      └─────────────┘      └──────────────┘      └────────────┘
```

## Quick Start

### 1. Install Dependencies

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Start Kafka and MailHog

Choose **Option A (Docker)** or **Option B (Homebrew)**:

---

#### Option A: Using Docker (Recommended)

```bash
docker-compose up -d
```

This starts:
- **Zookeeper** - Kafka coordination service
- **Kafka** - Message broker (localhost:9092)
- **Kafka UI** - Web interface at http://localhost:8080
- **MailHog** - Email testing server at http://localhost:8025

---

#### Option B: Using Homebrew (macOS)

**Step 1: Install Kafka and MailHog**

```bash
# Install Kafka (includes Zookeeper)
brew install kafka

# Install MailHog
brew install mailhog
```

**Step 2: Start Zookeeper (Terminal 1)**

```bash
# Start Zookeeper first (Kafka depends on it)
zookeeper-server-start /opt/homebrew/etc/kafka/zookeeper.properties
```

> Note: On Intel Mac, path is `/usr/local/etc/kafka/zookeeper.properties`

**Step 3: Start Kafka (Terminal 2)**

```bash
# Start Kafka broker
kafka-server-start /opt/homebrew/etc/kafka/server.properties
```

> Note: On Intel Mac, path is `/usr/local/etc/kafka/server.properties`

**Step 4: Create the email-topic (Terminal 3)**

```bash
# Create topic for email messages
kafka-topics --create --topic email-topic --bootstrap-server localhost:9092 --partitions 3 --replication-factor 1
```

**Step 5: Start MailHog (Terminal 4)**

```bash
# Start MailHog email testing server
mailhog
```

MailHog will be available at:
- **Web UI**: http://localhost:8025
- **SMTP**: localhost:1025

**Useful Kafka Commands:**

```bash
# List all topics
kafka-topics --list --bootstrap-server localhost:9092

# Describe a topic
kafka-topics --describe --topic email-topic --bootstrap-server localhost:9092

# View messages in topic (consumer)
kafka-console-consumer --topic email-topic --from-beginning --bootstrap-server localhost:9092
```

---

### 3. Start Django Server

```bash
python3 manage.py migrate
python3 manage.py runserver
```

### 4. Start Email Consumer

In a new terminal:
```bash
source venv/bin/activate
python3 email_consumer.py
```

### 5. Test the API

```bash
# Register a user (sends welcome email)
curl -X POST http://localhost:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "name": "John Doe"}'

# Request password reset
curl -X POST http://localhost:8000/api/password-reset/ \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com"}'

# Confirm order
curl -X POST http://localhost:8000/api/order-confirm/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "order_id": "ORD-12345",
    "items": [{"name": "Widget", "quantity": 2, "price": "$19.99"}],
    "total": "$39.98"
  }'
```

### 6. View Emails

Open http://localhost:8025 to see emails in MailHog.

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/register/` | POST | Register user (sends welcome email) |
| `/api/password-reset/` | POST | Request password reset email |
| `/api/order-confirm/` | POST | Send order confirmation email |
| `/api/payment-receipt/` | POST | Send payment receipt email |
| `/api/shipping-update/` | POST | Send shipping update email |
| `/api/health/` | GET | Health check |

## Configuration

Copy `.env.example` to `.env` and update:

```env
# For MailHog (local testing)
SMTP_HOST=localhost
SMTP_PORT=1025

# For Gmail (real emails)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

## Project Structure

```
email_notification_project/
├── config/                 # Django settings
│   ├── settings.py
│   └── urls.py
├── users/                  # User API endpoints
│   ├── views.py           # API views
│   └── urls.py
├── notifications/          # Notification logic
│   ├── kafka_producer.py  # Kafka producer
│   └── email_templates.py # Email templates
├── email_consumer.py       # Standalone email consumer
├── docker-compose.yml      # Kafka + MailHog
└── requirements.txt
```

## Scaling

To handle more emails, run multiple consumer instances:

```bash
# Terminal 1
python3 email_consumer.py

# Terminal 2
python3 email_consumer.py

# Terminal 3
python3 email_consumer.py
```

All consumers in the same group share the load automatically!
