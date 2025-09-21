# CloudEvents Reference

This document provides a comprehensive reference for CloudEvents used in the OCN ecosystem.

## Overview

CloudEvents is a specification for describing event data in a common way. The OCN ecosystem uses CloudEvents v1.0 to ensure consistent event structure across all services.

## Standard CloudEvent Structure

All CloudEvents in the OCN ecosystem follow this base structure:

```json
{
  "specversion": "1.0",
  "id": "unique-event-id",
  "source": "https://service.ocn.ai/v1",
  "type": "ocn.service.event.v1",
  "subject": "trace-id-or-correlation-id",
  "time": "2024-01-01T12:00:00Z",
  "datacontenttype": "application/json",
  "dataschema": "https://schemas.ocn.ai/events/service/event/v1",
  "data": {
    // Event-specific payload
  }
}
```

### Required Fields

- **specversion**: Always "1.0" for OCN events
- **id**: Unique identifier for this event instance
- **source**: URI identifying the event producer
- **type**: Event type following OCN naming convention
- **subject**: Trace ID or correlation identifier (see Trace section below)
- **time**: ISO 8601 timestamp when the event occurred

### Optional Fields

- **datacontenttype**: MIME type of the data payload (default: "application/json")
- **dataschema**: URI reference to the event's schema
- **data**: The actual event payload

## OCN Event Types

### Decision Events

**Type**: `ocn.orca.decision.v1`

Emitted by the Orca decision engine when processing transactions.

```json
{
  "specversion": "1.0",
  "id": "decision-123",
  "source": "https://orca.ocn.ai/v1",
  "type": "ocn.orca.decision.v1",
  "subject": "txn_trace_456",
  "time": "2024-01-01T12:00:00Z",
  "datacontenttype": "application/json",
  "dataschema": "https://schemas.ocn.ai/events/orca/decision/v1",
  "data": {
    "decision": "APPROVE",
    "amount": 100.00,
    "currency": "USD",
    "risk_score": 0.15,
    "reasons": ["Low risk profile", "Within limits"],
    "trace_id": "txn_trace_456"
  }
}
```

### Explanation Events

**Type**: `ocn.orca.explanation.v1`

Emitted by the Orca decision engine to provide AI-generated explanations.

```json
{
  "specversion": "1.0",
  "id": "explanation-123",
  "source": "https://orca.ocn.ai/v1",
  "type": "ocn.orca.explanation.v1",
  "subject": "txn_trace_456",
  "time": "2024-01-01T12:00:01Z",
  "datacontenttype": "application/json",
  "dataschema": "https://schemas.ocn.ai/events/orca/explanation/v1",
  "data": {
    "decision_id": "decision-123",
    "reason": "Transaction approved due to low risk indicators",
    "key_signals": ["amount within limits", "merchant reputation good"],
    "mitigation": "Standard fraud monitoring applied",
    "confidence": 0.85,
    "trace_id": "txn_trace_456"
  }
}
```

### Audit Events

**Type**: `ocn.weave.audit.v1`

Emitted by the Weave receipt store for audit trail purposes.

```json
{
  "specversion": "1.0",
  "id": "audit-123",
  "source": "https://weave.ocn.ai/v1",
  "type": "ocn.weave.audit.v1",
  "subject": "txn_trace_456",
  "time": "2024-01-01T12:00:02Z",
  "datacontenttype": "application/json",
  "dataschema": "https://schemas.ocn.ai/events/weave/audit/v1",
  "data": {
    "receipt_id": "receipt-789",
    "event_hash": "sha256:abc123...",
    "provider_id": "ocn-orca-v1",
    "trust_verified": true,
    "trace_id": "txn_trace_456"
  }
}
```

## Trace

### Trace ID Propagation

The OCN ecosystem uses trace IDs for request correlation and observability. Trace IDs are propagated through the `subject` field of CloudEvents.

#### Trace ID Format

Trace IDs follow UUID4 format for uniqueness and consistency:

```
550e8400-e29b-41d4-a716-446655440000
```

#### Trace ID Usage in CloudEvents

The `subject` field of every CloudEvent should contain the trace ID for the request chain:

```json
{
  "specversion": "1.0",
  "id": "event-123",
  "source": "https://service.ocn.ai/v1",
  "type": "ocn.service.event.v1",
  "subject": "550e8400-e29b-41d4-a716-446655440000",
  "time": "2024-01-01T12:00:00Z",
  "data": {
    "trace_id": "550e8400-e29b-41d4-a716-446655440000"
  }
}
```

#### Trace ID Generation

Use the `ocn_common.trace` module for trace ID management:

```python
from ocn_common.trace import new_trace_id, inject_trace_id_ce

# Generate new trace ID
trace_id = new_trace_id()

# Inject into CloudEvent envelope
envelope = {
    "specversion": "1.0",
    "id": "event-123",
    "type": "ocn.service.event.v1"
}
envelope_with_trace = inject_trace_id_ce(envelope, trace_id)
# envelope_with_trace["subject"] == trace_id
```

#### HTTP Header Propagation

Trace IDs are propagated via the `x-ocn-trace-id` HTTP header:

```http
POST /events HTTP/1.1
Host: weave.ocn.ai
Content-Type: application/json
x-ocn-trace-id: 550e8400-e29b-41d4-a716-446655440000

{
  "specversion": "1.0",
  "id": "event-123",
  "type": "ocn.orca.decision.v1",
  "subject": "550e8400-e29b-41d4-a716-446655440000",
  "data": {...}
}
```

#### FastAPI Middleware Integration

Use the trace middleware for automatic trace ID management:

```python
from fastapi import FastAPI
from ocn_common.trace import trace_middleware

app = FastAPI()
app = trace_middleware(app)

# Now all requests automatically have trace ID management
@app.post("/events")
async def handle_event(event: CloudEvent):
    # Current trace ID available via get_current_trace_id()
    pass
```

#### Trace ID Context

The trace ID is maintained in a context variable for the duration of the request:

```python
from ocn_common.trace import get_current_trace_id, set_current_trace_id

# Get current trace ID
trace_id = get_current_trace_id()

# Set trace ID (usually done by middleware)
set_current_trace_id("custom-trace-id")
```

#### Logging with Trace IDs

Use the trace log formatter for consistent logging:

```python
from ocn_common.trace import format_trace_log

trace_id = get_current_trace_id()
log_message = format_trace_log(
    trace_id,
    "Processing request",
    user_id="123",
    action="login"
)
# Result: "[trace_id=550e8400-e29b-41d4-a716-446655440000] Processing request user_id=123 action=login"
```

### Trace ID Best Practices

1. **Always include trace ID in CloudEvent subject**: Ensures end-to-end correlation
2. **Propagate via HTTP headers**: Use `x-ocn-trace-id` for service-to-service calls
3. **Include in logs**: Use structured logging with trace ID for debugging
4. **Generate early**: Create trace ID at the start of request processing
5. **Maintain context**: Use context variables to keep trace ID available throughout request lifecycle

## Event Schemas

All CloudEvents in the OCN ecosystem have corresponding JSON schemas for validation:

- Decision events: `common/events/v1/orca.decision.v1.schema.json`
- Explanation events: `common/events/v1/orca.explanation.v1.schema.json`
- Audit events: `common/events/v1/weave.audit.v1.schema.json`

## Validation

Use the `ocn_common.contracts` module for CloudEvent validation:

```python
from ocn_common.contracts import validate_cloudevent

# Validate CloudEvent against schema
try:
    validate_cloudevent(event_data, "orca.decision.v1")
    print("Valid CloudEvent")
except ValidationError as e:
    print(f"Invalid CloudEvent: {e}")
```

## Examples

See the `examples/events/` directory for complete CloudEvent examples:

- `decision_approve.json` - Approved decision event
- `explanation_approve.json` - Decision explanation event
- `audit_approve.json` - Receipt audit event

## Migration Guide

When upgrading CloudEvent schemas:

1. Check schema version compatibility
2. Update event type versions (e.g., v1 → v2)
3. Validate all event producers and consumers
4. Update documentation and examples

See `docs/migration_guide_ap2.md` for detailed migration instructions.
