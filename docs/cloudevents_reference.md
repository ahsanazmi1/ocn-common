# CloudEvents Reference for OCN

## Overview

The Open Checkout Network (OCN) uses CloudEvents (CE) as the standard event format for inter-service communication. This document defines the CE attributes, event types, and sample envelopes used across the OCN ecosystem.

## CloudEvents Specification

OCN implements CloudEvents specification version 1.0.2 with extensions for OCN-specific requirements.

## Core Attributes

### Required Attributes

| Attribute | Type | Description | Example |
|-----------|------|-------------|---------|
| `specversion` | String | CloudEvents specification version | `"1.0.2"` |
| `type` | String | OCN event type identifier | `"ocn.orca.decision.v1"` |
| `source` | URI | Service that generated the event | `"https://api.ocn.orca.com"` |
| `id` | String | Unique event identifier | `"evt_550e8400-e29b-41d4-a716-446655440000"` |
| `time` | Timestamp | ISO 8601 event timestamp | `"2024-01-21T12:00:00.000Z"` |
| `datacontenttype` | String | Content type of the data payload | `"application/json"` |

### Optional Attributes

| Attribute | Type | Description | Example |
|-----------|------|-------------|---------|
| `subject` | String | Event subject identifier | `"user_12345"` |
| `dataschema` | URI | JSON Schema for data validation | `"https://schemas.ocn.com/decision/v1"` |
| `traceid` | String | Distributed tracing identifier | `"550e8400-e29b-41d4-a716-446655440000"` |
| `spanid` | String | Span identifier for tracing | `"span_abc123"` |

### OCN Extensions

| Extension | Type | Description | Example |
|-----------|------|-------------|---------|
| `ocnservice` | String | OCN service identifier | `"orca"` |
| `ocnversion` | String | Service version | `"1.0.0"` |
| `ocnenvironment` | String | Deployment environment | `"production"` |
| `ocnregion` | String | AWS region | `"us-east-1"` |
| `ocncorrelationid` | String | Business correlation ID | `"txn_abc123"` |

## Event Types

### Decision Events

#### ocn.orca.decision.v1

Decision result from Orca decision engine.

```json
{
  "specversion": "1.0.2",
  "type": "ocn.orca.decision.v1",
  "source": "https://api.ocn.orca.com",
  "id": "evt_decision_550e8400-e29b-41d4-a716-446655440000",
  "time": "2024-01-21T12:00:00.000Z",
  "datacontenttype": "application/json",
  "subject": "user_12345",
  "dataschema": "https://schemas.ocn.com/decision/v1",
  "traceid": "550e8400-e29b-41d4-a716-446655440000",
  "ocnservice": "orca",
  "ocnversion": "1.0.0",
  "ocnenvironment": "production",
  "ocnregion": "us-east-1",
  "ocncorrelationid": "txn_abc123",
  "data": {
    "decision_id": "dec_550e8400-e29b-41d4-a716-446655440000",
    "result": "APPROVE",
    "confidence": 0.95,
    "risk_score": 0.15,
    "processing_time_ms": 45,
    "rules_triggered": [
      "velocity_check",
      "mcc_validation",
      "ml_risk_assessment"
    ],
    "transaction": {
      "amount": 99.99,
      "currency": "USD",
      "merchant_id": "merchant_abc123",
      "mcc": "5411"
    },
    "user": {
      "id": "user_12345",
      "risk_profile": "standard"
    },
    "metadata": {
      "model_version": "1.2.0",
      "feature_vector": ["f1", "f2", "f3"],
      "explanation_available": true
    }
  }
}
```

#### ocn.orca.explanation.v1

AI-generated explanation for a decision.

```json
{
  "specversion": "1.0.2",
  "type": "ocn.orca.explanation.v1",
  "source": "https://api.ocn.orca.com",
  "id": "evt_explanation_550e8400-e29b-41d4-a716-446655440000",
  "time": "2024-01-21T12:00:05.000Z",
  "datacontenttype": "application/json",
  "subject": "user_12345",
  "dataschema": "https://schemas.ocn.com/explanation/v1",
  "traceid": "550e8400-e29b-41d4-a716-446655440000",
  "ocnservice": "orca",
  "ocnversion": "1.0.0",
  "ocnenvironment": "production",
  "ocnregion": "us-east-1",
  "ocncorrelationid": "txn_abc123",
  "data": {
    "explanation_id": "exp_550e8400-e29b-41d4-a716-446655440000",
    "decision_id": "dec_550e8400-e29b-41d4-a716-446655440000",
    "explanation_type": "natural_language",
    "language": "en",
    "content": "Your transaction was approved based on your consistent spending patterns and low risk profile. The amount is within your typical range for this merchant category.",
    "confidence": 0.88,
    "generation_time_ms": 1200,
    "model": {
      "name": "orca-explainer-v2",
      "version": "2.1.0"
    },
    "factors": [
      {
        "factor": "spending_pattern",
        "impact": "positive",
        "weight": 0.4,
        "description": "Transaction amount consistent with historical patterns"
      },
      {
        "factor": "merchant_trust",
        "impact": "positive",
        "weight": 0.3,
        "description": "Merchant has good reputation and low fraud rate"
      },
      {
        "factor": "time_pattern",
        "impact": "neutral",
        "weight": 0.2,
        "description": "Transaction time within normal hours"
      }
    ],
    "metadata": {
      "llm_provider": "azure_openai",
      "prompt_version": "v1.2",
      "temperature": 0.7
    }
  }
}
```

### Receipt Events

#### ocn.weave.receipt.v1

Receipt storage confirmation from Weave.

```json
{
  "specversion": "1.0.2",
  "type": "ocn.weave.receipt.v1",
  "source": "https://api.ocn.weave.com",
  "id": "evt_receipt_550e8400-e29b-41d4-a716-446655440000",
  "time": "2024-01-21T12:00:02.000Z",
  "datacontenttype": "application/json",
  "subject": "user_12345",
  "dataschema": "https://schemas.ocn.com/receipt/v1",
  "traceid": "550e8400-e29b-41d4-a716-446655440000",
  "ocnservice": "weave",
  "ocnversion": "1.0.0",
  "ocnenvironment": "production",
  "ocnregion": "us-east-1",
  "ocncorrelationid": "txn_abc123",
  "data": {
    "receipt_id": "rec_550e8400-e29b-41d4-a716-446655440000",
    "receipt_type": "decision",
    "provider_id": "ocn-orca-v1",
    "content_hash": "sha256:abc123def456...",
    "storage_location": "s3://ocn-receipts/production/2024/01/21/rec_550e8400...",
    "storage_time_ms": 12,
    "content": {
      "decision_id": "dec_550e8400-e29b-41d4-a716-446655440000",
      "result": "APPROVE",
      "timestamp": "2024-01-21T12:00:00.000Z",
      "transaction": {
        "amount": 99.99,
        "currency": "USD",
        "merchant_id": "merchant_abc123"
      }
    },
    "metadata": {
      "compression": "gzip",
      "encryption": "aes-256-gcm",
      "retention_days": 2555
    }
  }
}
```

### Audit Events

#### ocn.weave.audit.v1

Audit trail event for compliance and monitoring.

```json
{
  "specversion": "1.0.2",
  "type": "ocn.weave.audit.v1",
  "source": "https://api.ocn.weave.com",
  "id": "evt_audit_550e8400-e29b-41d4-a716-446655440000",
  "time": "2024-01-21T12:00:01.000Z",
  "datacontenttype": "application/json",
  "subject": "user_12345",
  "dataschema": "https://schemas.ocn.com/audit/v1",
  "traceid": "550e8400-e29b-41d4-a716-446655440000",
  "ocnservice": "weave",
  "ocnversion": "1.0.0",
  "ocnenvironment": "production",
  "ocnregion": "us-east-1",
  "ocncorrelationid": "txn_abc123",
  "data": {
    "audit_id": "audit_550e8400-e29b-41d4-a716-446655440000",
    "event_type": "receipt_stored",
    "action": "CREATE",
    "resource_type": "receipt",
    "resource_id": "rec_550e8400-e29b-41d4-a716-446655440000",
    "actor": {
      "type": "service",
      "id": "weave-receipt-service",
      "version": "1.0.0"
    },
    "target": {
      "type": "user",
      "id": "user_12345"
    },
    "result": "SUCCESS",
    "details": {
      "storage_location": "s3://ocn-receipts/production/2024/01/21/",
      "content_size_bytes": 1024,
      "processing_time_ms": 12
    },
    "compliance": {
      "pci_dss": true,
      "gdpr": true,
      "sox": true
    },
    "metadata": {
      "request_id": "req_abc123",
      "client_ip": "203.0.113.1",
      "user_agent": "OCN-Client/1.0.0"
    }
  }
}
```

### Credit Events

#### ocn.okra.quote.v1

Credit quote from Okra credit agent.

```json
{
  "specversion": "1.0.2",
  "type": "ocn.okra.quote.v1",
  "source": "https://api.ocn.okra.com",
  "id": "evt_quote_550e8400-e29b-41d4-a716-446655440000",
  "time": "2024-01-21T12:00:03.000Z",
  "datacontenttype": "application/json",
  "subject": "user_12345",
  "dataschema": "https://schemas.ocn.com/quote/v1",
  "traceid": "550e8400-e29b-41d4-a716-446655440000",
  "ocnservice": "okra",
  "ocnversion": "1.0.0",
  "ocnenvironment": "production",
  "ocnregion": "us-east-1",
  "ocncorrelationid": "credit_req_abc123",
  "data": {
    "quote_id": "quote_550e8400-e29b-41d4-a716-446655440000",
    "credit_decision": "APPROVE",
    "approved_amount": 5000.00,
    "interest_rate": 12.5,
    "term_months": 36,
    "monthly_payment": 167.50,
    "credit_score": 720,
    "dti_ratio": 0.35,
    "processing_time_ms": 23,
    "user": {
      "id": "user_12345",
      "income": 75000.00,
      "employment_status": "employed"
    },
    "metadata": {
      "model_version": "credit-v1.3",
      "risk_tier": "standard",
      "offer_expires_at": "2024-01-28T12:00:00.000Z"
    }
  }
}
```

### Wallet Events

#### ocn.opal.selection.v1

Wallet selection decision from Opal wallet agent.

```json
{
  "specversion": "1.0.2",
  "type": "ocn.opal.selection.v1",
  "source": "https://api.ocn.opal.com",
  "id": "evt_selection_550e8400-e29b-41d4-a716-446655440000",
  "time": "2024-01-21T12:00:04.000Z",
  "datacontenttype": "application/json",
  "subject": "user_12345",
  "dataschema": "https://schemas.ocn.com/selection/v1",
  "traceid": "550e8400-e29b-41d4-a716-446655440000",
  "ocnservice": "opal",
  "ocnversion": "1.0.0",
  "ocnenvironment": "production",
  "ocnregion": "us-east-1",
  "ocncorrelationid": "wallet_req_abc123",
  "data": {
    "selection_id": "sel_550e8400-e29b-41d4-a716-446655440000",
    "result": "ALLOWED",
    "selected_wallet": "wallet_primary",
    "transaction_amount": 99.99,
    "mcc_code": "5411",
    "channel": "pos",
    "processing_time_ms": 8,
    "controls_checked": [
      "daily_limit",
      "merchant_restriction",
      "balance_check"
    ],
    "user": {
      "id": "user_12345",
      "wallet_balance": 2500.00,
      "daily_spent": 45.67
    },
    "metadata": {
      "rule_engine_version": "opal-v1.1",
      "control_version": "controls-v2.0"
    }
  }
}
```

## Event Routing

### Routing Rules

Events are routed based on the `type` attribute using the following patterns:

- `ocn.{service}.{operation}.v{major}` - Service-specific events
- `ocn.common.{operation}.v{major}` - Common/shared events
- `ocn.system.{operation}.v{major}` - System/infrastructure events

### Subscription Examples

```json
{
  "subscription_id": "sub_orca_decisions",
  "event_types": ["ocn.orca.decision.v1"],
  "endpoint": "https://api.ocn.weave.com/events/decision",
  "filters": {
    "ocnservice": "orca",
    "ocnenvironment": "production"
  }
}
```

## Event Validation

### Schema Validation

All events must validate against their respective JSON schemas:

```bash
# Validate decision event
curl -X POST https://schemas.ocn.com/validate \
  -H "Content-Type: application/json" \
  -d @decision_event.json
```

### Required Validations

1. **Attribute Validation**: All required CE attributes present
2. **Type Validation**: Event type matches expected format
3. **Schema Validation**: Data payload validates against schema
4. **Extension Validation**: OCN extensions are valid
5. **Timestamp Validation**: Time attribute is valid ISO 8601

## Error Events

### ocn.common.error.v1

Standard error event format.

```json
{
  "specversion": "1.0.2",
  "type": "ocn.common.error.v1",
  "source": "https://api.ocn.orca.com",
  "id": "evt_error_550e8400-e29b-41d4-a716-446655440000",
  "time": "2024-01-21T12:00:00.000Z",
  "datacontenttype": "application/json",
  "traceid": "550e8400-e29b-41d4-a716-446655440000",
  "ocnservice": "orca",
  "ocncorrelationid": "txn_abc123",
  "data": {
    "error_id": "err_550e8400-e29b-41d4-a716-446655440000",
    "error_code": "VALIDATION_FAILED",
    "error_message": "Invalid payment mandate signature",
    "error_details": {
      "field": "signature",
      "reason": "Invalid ECDSA signature"
    },
    "original_request": {
      "type": "PaymentMandate",
      "id": "payment_abc123"
    }
  }
}
```

## Implementation Guidelines

### Event Publishing

```python
from cloudevents.http import CloudEvent, to_structured

# Create decision event
event = CloudEvent(
    type="ocn.orca.decision.v1",
    source="https://api.ocn.orca.com",
    data={
        "decision_id": "dec_123",
        "result": "APPROVE",
        "confidence": 0.95
    }
)

# Add OCN extensions
event["ocnservice"] = "orca"
event["ocnversion"] = "1.0.0"
event["traceid"] = "550e8400-e29b-41d4-a716-446655440000"

# Convert to structured format
headers, body = to_structured(event)
```

### Event Consumption

```python
from cloudevents.http import from_http

# Parse incoming event
event = from_http(headers, body)

# Validate event type
if event["type"] == "ocn.orca.decision.v1":
    process_decision(event.data)
elif event["type"] == "ocn.orca.explanation.v1":
    process_explanation(event.data)
```

This CloudEvents reference provides the foundation for event-driven communication across the OCN ecosystem.
