# Logging & Monitoring - Class Notes

## 1. Why Not Print/Debugger?

### The Problem with `print()`
| Issue | print() | Logging |
|-------|---------|---------|
| Add to running production? | No | Yes (already there) |
| Persists after restart? | No | Yes (to file/cloud) |
| Log levels? | No | DEBUG, INFO, WARN, ERROR |
| Structured data? | No | JSON with fields |
| Centralized search? | No | Yes (ELK, CloudWatch) |

### The Problem with Debuggers
```
Your Laptop                    Production
┌─────────────┐               ┌─────────────┐
│ 1 process   │               │ 100 servers │
│ You control │               │ No access   │
│ Can pause   │               │ Can't pause │
└─────────────┘               └─────────────┘
      ✓ Debugger works              ✗ Debugger useless
```

---

## 2. Log Levels

```
DEBUG  →  INFO  →  WARNING  →  ERROR  →  CRITICAL
 ↑                                            ↑
 Most verbose                          Most severe
 (dev only)                           (always log)
```

| Level | When to Use | Example |
|-------|-------------|---------|
| DEBUG | Development details | `Variable x = 42` |
| INFO | Normal operations | `User logged in` |
| WARNING | Something unexpected | `Retrying connection...` |
| ERROR | Something failed | `Payment declined` |
| CRITICAL | System is down | `Database unreachable` |

**Production tip**: Set level to INFO (not DEBUG) to reduce noise and cost.

---

## 3. Distributed Logging

### The Problem: Which Logs Belong Together?

```
Without Request ID:
──────────────────
10:23:45 [auth]    User validated        ← Which request?
10:23:45 [order]   Order created         ← Same user?
10:23:45 [payment] Payment failed        ← Related?
10:23:45 [auth]    User validated        ← Different request?

With Request ID:
────────────────
10:23:45 [auth]    req_id=abc123 User validated
10:23:45 [order]   req_id=abc123 Order created
10:23:45 [payment] req_id=abc123 Payment failed   ← All same request!
10:23:45 [auth]    req_id=xyz789 User validated   ← Different request
```

### Request ID Flow

```
┌────────┐      ┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│ Client │ ──── │ API Gateway │ ──── │ Order Svc   │ ──── │ Payment Svc │
└────────┘      └─────────────┘      └─────────────┘      └─────────────┘
                      │                     │                    │
                 Generate ID:          Pass header:         Pass header:
                 X-Request-ID          X-Request-ID         X-Request-ID
                 = abc-123             = abc-123            = abc-123
```

### Request ID vs Trace ID

| Aspect | Request ID | Trace ID |
|--------|------------|----------|
| Purpose | Link logs together | Link logs + timing + hierarchy |
| What you get | "These logs are related" | "Service A called B, which took 200ms" |
| Structure | Just a string | Trace ID + Span IDs + Parent IDs |
| Tools needed | grep | Jaeger, Zipkin, Datadog |

### Understanding Spans

```
Trace ID: abc-123

├── Span 1 [API Gateway] ─────────────────────────── 0-500ms
│   │
│   ├── Span 2 [Auth Service] ────── 50-80ms
│   │
│   ├── Span 3 [Product Service] ── 80-160ms
│   │
│   └── Span 4 [Order Service] ──────────────────── 160-400ms
│       │
│       └── Span 5 [Payment Service] ───────────── 200-380ms
│           │
│           └── Span 6 [DB Query] ──────────────── 250-330ms ← Bottleneck!
```

Each span reports: `{ trace_id, span_id, parent_id, service, start_time, end_time }`

---

## 4. Log Aggregation Architecture

```
┌─────────┐ ┌─────────┐ ┌─────────┐
│ Server 1│ │ Server 2│ │ Server 3│    Multiple sources
└────┬────┘ └────┬────┘ └────┬────┘
     │           │           │
     └───────────┼───────────┘
                 ▼
          ┌─────────────┐
          │   Kafka     │              Buffer (handle spikes)
          └──────┬──────┘
                 ▼
          ┌─────────────┐
          │  Processor  │              Parse, enrich, filter
          └──────┬──────┘
                 ▼
          ┌─────────────┐
          │   Storage   │              Elasticsearch / CloudWatch
          └──────┬──────┘
                 ▼
          ┌─────────────┐
          │  Dashboard  │              Kibana / Grafana
          └─────────────┘
```

---

## 5. Cloud Logging Benefits

| Capability | What It Does |
|------------|--------------|
| Search at Scale | Query terabytes in seconds |
| Dashboards | Visualize error rates, latency |
| Alerts | Notify when thresholds crossed |
| Correlation | Link logs + metrics + traces |
| Compliance | Archive for GDPR, HIPAA, SOC2 |
| Security | IAM controls, encryption |

---

## 6. Cost Optimization

### The Problem
```
10,000 transactions/min × 5 logs each = 50,000 logs/min
= 72 million logs/day
= $1,000+/month just for logging!
```

### Solution: Log Sampling

```python
# Log ALL errors (100%) - every error matters
if payment_failed:
    logger.error(f"Payment failed: {transaction_id}")

# Log only 10% of successes - enough to spot patterns
elif random.random() < 0.1:
    logger.info(f"Payment success: {transaction_id}")
```

### Other Strategies
- **Shorter retention**: 7 days hot, archive older to S3
- **Filter at source**: Drop health check logs (`GET /health`)
- **Compress**: JSON logs compress 5-10x with gzip

---

## 7. Tracing Standards

**Why standards?** If Service A uses `X-Request-ID` and Service B uses `X-Trace-ID`, they can't communicate trace context.

| Standard | Header Format |
|----------|---------------|
| W3C Trace Context | `traceparent: 00-abc123-def456-01` |
| B3 (Zipkin) | `X-B3-TraceId`, `X-B3-SpanId` |
| OpenTelemetry | Uses W3C, unified logs+metrics+traces |

---

## Quick Reference

```python
import logging

# Basic setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s %(message)s'
)
logger = logging.getLogger(__name__)

# Usage
logger.debug("Detailed info for debugging")
logger.info("Normal operation")
logger.warning("Something unexpected")
logger.error("Something failed")
logger.critical("System is down")
```

### Django Logging Config
```python
# settings.py
LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}
```
