# Monitoring Fundamentals

> What metrics to track, why they matter, and how to use them effectively.

---

## Logs vs Metrics: What's the Difference?

| Aspect | Logs | Metrics |
|--------|------|---------|
| **What they are** | Discrete events with context | Numeric measurements over time |
| **Example** | "User X did Y at time Z" | "CPU at 80%", "500 req/sec" |
| **Data density** | High cardinality, detailed | Aggregated, compact |
| **Best for** | Debugging specific issues | Trends and alerting |
| **Cost at scale** | Expensive ($$$) | Cheap ($) |

### Rule of Thumb

- **Metrics** → "How many? How much?" questions
- **Logs** → "What exactly happened?" questions

---

## The Four Golden Signals

From [Google's SRE Book](https://sre.google/sre-book/monitoring-distributed-systems/) - the four metrics every service should monitor:

### 1. Latency ⏱️
How long requests take.

- Track **p50, p90, p99 percentiles**, not just average
- p99 = 500ms means 99% of requests are faster than 500ms
- Distinguish between latency of successful vs failed requests

### 2. Traffic 📈
How much demand is on your system.

- Requests per second
- Concurrent users
- Transactions per minute
- Network I/O

### 3. Errors ❌
Rate of failed requests.

- Explicit errors (HTTP 5xx)
- Implicit errors (wrong data returned, timeouts)
- Express as error rate: `errors / total requests`

### 4. Saturation 📊
How "full" your service is.

- CPU utilization
- Memory usage
- Disk I/O
- Connection pool usage
- Queue depth

---

## Why Percentiles Matter

```
LATENCY DISTRIBUTION (1000 requests)
════════════════════════════════════

    Number of requests
    ▲
100 │ ████
 80 │ ████████
 60 │ ████████████
 40 │ ████████████████
 20 │ ████████████████████████
    └────────────────────────────────▶ Latency (ms)
      50   100  200  500  1000 2000

p50 (median) = 100ms  → 50% of requests faster than this
p90 = 500ms           → 90% of requests faster than this
p99 = 1000ms          → 99% of requests faster than this
```

### Why not use averages?

If you have **1 million requests/day**:
- p99 = 1000ms means **10,000 requests** take >1 second
- Average hides outliers
- p99 catches the worst user experiences

---

## Types of Metrics

### Counter
**Only goes up** (or resets to 0 on restart)

```
0 → 5 → 12 → 50 → 100 → 250
        ↑ (never decreases)
```

**Use for:**
- Total requests served
- Error count
- Bytes sent/received
- Tasks completed

**Query pattern:** Rate of change (`rate(counter[5m])`)

---

### Gauge
**Goes up and down** - represents current state

```
80% → 45% → 92% → 60% → 75%
     ↑↓ (fluctuates)
```

**Use for:**
- CPU percentage
- Memory usage
- Queue size
- Active connections
- Temperature

**Query pattern:** Current value or average over time

---

### Histogram
**Distribution across buckets** - tracks how values are spread

```
Bucket     Count
<100ms:    ████████ 800
<500ms:    ██ 150
<1s:       █ 50
```

**Use for:**
- Request latency distribution
- Response sizes
- Any value where distribution matters

**Query pattern:** Percentiles (`histogram_quantile(0.99, ...)`)

---

### Summary
**Pre-calculated percentiles** on the client side

```
p50: 100ms
p90: 450ms
p99: 980ms
```

**Use for:**
- When you need exact percentiles
- When aggregation across instances isn't needed

---

## Metric Type Decision Tree

```
Is it a cumulative total that only increases?
├── YES → COUNTER (requests, errors, bytes)
└── NO
    └── Is it a current snapshot value?
        ├── YES → GAUGE (CPU%, memory, queue size)
        └── NO
            └── Do you need distribution/percentiles?
                ├── YES → HISTOGRAM (latency, sizes)
                └── NO → Probably a GAUGE
```

---

## The RED Method (For Services)

A simplified monitoring approach for request-driven services:

| Signal | What to Track | Example |
|--------|---------------|---------|
| **R** - Rate | Requests per second | `rate(http_requests_total[5m])` |
| **E** - Errors | Failed requests per second | `rate(http_errors_total[5m])` |
| **D** - Duration | Request latency (histogram) | `histogram_quantile(0.99, ...)` |

---

## The USE Method (For Resources)

For infrastructure components (CPU, memory, disk, network):

| Signal | What to Track | Example |
|--------|---------------|---------|
| **U** - Utilization | % of resource used | CPU at 75% |
| **S** - Saturation | Work queued/waiting | 10 processes in run queue |
| **E** - Errors | Error count | Disk read errors |

---

## What to Monitor

### Infrastructure Metrics

```
┌─────────────────────────────────────────────────────────────────┐
│ SERVER                                                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────┐    │
│  │   CPU    │  │  Memory  │  │   Disk   │  │   Network    │    │
│  │ • Usage %│  │ • Used % │  │ • Usage %│  │ • Bytes in/out│   │
│  │ • Load   │  │ • Free   │  │ • IOPS   │  │ • Errors     │    │
│  │ • Steal  │  │ • Swap   │  │ • Latency│  │ • Packets    │    │
│  └──────────┘  └──────────┘  └──────────┘  └──────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

### Application Metrics

| Metric | What It Tells You | Alert When |
|--------|-------------------|------------|
| Request Rate | Traffic volume, usage patterns | Sudden drop (outage?) or spike (attack?) |
| Error Rate | Service health, bugs | > 1% of requests failing |
| p50 Latency | Typical user experience | > 200ms for typical APIs |
| p99 Latency | Worst-case experience | > 1000ms (varies by service) |
| Availability | Uptime percentage | < 99.9% (depending on SLA) |

### Database Metrics

- **Query latency:** p50, p95, p99
- **Connection pool:** Active, idle, waiting
- **Replication lag:** How far behind replicas are
- **Lock waits:** Time spent waiting for locks
- **Cache hit ratio:** Buffer pool efficiency

---

## Prometheus Metric Examples

```python
from prometheus_client import Counter, Histogram, Gauge

# Counter: Total requests (only goes up)
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

# Histogram: Request duration with buckets
REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'Request latency in seconds',
    ['endpoint'],
    buckets=[0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0]
)

# Gauge: Current active connections (goes up and down)
ACTIVE_CONNECTIONS = Gauge(
    'active_connections',
    'Number of active connections'
)
```

### Prometheus Query Examples

```promql
# Request rate (requests per second over last 5 minutes)
rate(http_requests_total[5m])

# Error rate as percentage
rate(http_requests_total{status=~"5.."}[5m])
  / rate(http_requests_total[5m]) * 100

# 99th percentile latency
histogram_quantile(0.99,
  rate(http_request_duration_seconds_bucket[5m])
)

# Current memory usage
process_resident_memory_bytes / 1024 / 1024  # Convert to MB
```

---

## Alerting Best Practices

### Good Alerts

1. **Actionable** - Someone needs to do something
2. **Urgent** - Requires immediate attention
3. **Clear** - Includes context to diagnose
4. **Rare** - Not crying wolf

### Alert on Symptoms, Not Causes

```
❌ BAD:  Alert when CPU > 80%
         (CPU can be high and everything is fine)

✅ GOOD: Alert when p99 latency > 1s for 5 minutes
         (Users are actually affected)
```

### Example Alert Rules

```yaml
# High error rate
- alert: HighErrorRate
  expr: rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m]) > 0.01
  for: 5m
  labels:
    severity: critical
  annotations:
    summary: "Error rate > 1% for 5 minutes"

# High latency
- alert: HighLatency
  expr: histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m])) > 1
  for: 5m
  labels:
    severity: warning
  annotations:
    summary: "p99 latency > 1s for 5 minutes"
```

---

## Quick Reference

| I want to track... | Metric Type | Example |
|--------------------|-------------|---------|
| Total requests since start | Counter | `http_requests_total` |
| Current memory usage | Gauge | `memory_usage_bytes` |
| Request latency distribution | Histogram | `request_duration_seconds` |
| Active users right now | Gauge | `active_users` |
| Errors since start | Counter | `errors_total` |
| Queue depth | Gauge | `queue_size` |
| Response size distribution | Histogram | `response_size_bytes` |

---

## Summary

1. **Four Golden Signals:** Latency, Traffic, Errors, Saturation
2. **Use percentiles** (p50, p90, p99) not averages for latency
3. **Counter** for things that only go up (requests, errors)
4. **Gauge** for current state (CPU%, connections, queue size)
5. **Histogram** for distributions (latency, sizes)
6. **RED Method** for services: Rate, Errors, Duration
7. **USE Method** for resources: Utilization, Saturation, Errors
8. **Alert on symptoms** (user impact), not causes (high CPU)
