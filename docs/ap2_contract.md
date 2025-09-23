# AP2 Contract Specification

## Overview

The AP2 (Agent Protocol v2) Contract defines the standardized data structures for agent communication within the Open Checkout Network (OCN). This specification covers mandates, actor profiles, and presence indicators that enable secure, interoperable agent interactions.

## Core Concepts

### Mandates

Mandates are digitally signed authorization structures that define what an agent is permitted to do on behalf of a user. They include cryptographic proofs and specific authorization scopes.

### Actor Profiles

Actor profiles describe the identity, capabilities, and metadata of agents operating within the OCN ecosystem.

### Agent Presence

Agent presence indicates the availability and modality of agents for processing requests.

## Contract Definitions

### IntentMandate

Defines the user's intent for a transaction or action.

```json
{
  "type": "IntentMandate",
  "version": "2.0",
  "id": "intent_550e8400-e29b-41d4-a716-446655440000",
  "timestamp": "2024-01-21T12:00:00.000Z",
  "expires_at": "2024-01-21T12:30:00.000Z",
  "user_id": "user_12345",
  "intent": {
    "action": "purchase",
    "merchant_id": "merchant_abc123",
    "amount": 99.99,
    "currency": "USD",
    "description": "Coffee purchase at Downtown Cafe",
    "metadata": {
      "mcc": "5814",
      "channel": "pos",
      "location": {
        "latitude": 37.7749,
        "longitude": -122.4194
      }
    }
  },
  "signature": {
    "algorithm": "ES256",
    "public_key": "04a1b2c3d4e5f6...",
    "signature": "3045022100a1b2c3d4e5f6..."
  }
}
```

**Required Fields:**
- `type`: Must be "IntentMandate"
- `version`: Contract version (e.g., "2.0")
- `id`: Unique mandate identifier
- `timestamp`: ISO 8601 timestamp of creation
- `expires_at`: ISO 8601 timestamp of expiration
- `user_id`: Identifier of the user authorizing the intent
- `intent`: Object containing the user's intent details
- `signature`: Digital signature for mandate validation

### CartMandate

Defines the shopping cart contents and transaction context.

```json
{
  "type": "CartMandate",
  "version": "2.0",
  "id": "cart_550e8400-e29b-41d4-a716-446655440000",
  "timestamp": "2024-01-21T12:00:00.000Z",
  "expires_at": "2024-01-21T12:30:00.000Z",
  "user_id": "user_12345",
  "cart": {
    "items": [
      {
        "id": "item_001",
        "name": "Coffee - Large",
        "quantity": 1,
        "unit_price": 4.50,
        "total_price": 4.50,
        "category": "beverages",
        "metadata": {
          "sku": "COFFEE_LG_001",
          "tax_category": "food"
        }
      },
      {
        "id": "item_002",
        "name": "Croissant",
        "quantity": 2,
        "unit_price": 3.25,
        "total_price": 6.50,
        "category": "food",
        "metadata": {
          "sku": "CROISSANT_001",
          "tax_category": "food"
        }
      }
    ],
    "subtotal": 11.00,
    "tax": 0.88,
    "total": 11.88,
    "currency": "USD",
    "merchant_id": "merchant_abc123"
  },
  "signature": {
    "algorithm": "ES256",
    "public_key": "04a1b2c3d4e5f6...",
    "signature": "3045022100a1b2c3d4e5f6..."
  }
}
```

**Required Fields:**
- `type`: Must be "CartMandate"
- `version`: Contract version
- `id`: Unique mandate identifier
- `timestamp`: ISO 8601 timestamp of creation
- `expires_at`: ISO 8601 timestamp of expiration
- `user_id`: Identifier of the user
- `cart`: Object containing cart items and totals
- `signature`: Digital signature for mandate validation

### PaymentMandate

Defines payment method authorization and processing parameters.

```json
{
  "type": "PaymentMandate",
  "version": "2.0",
  "id": "payment_550e8400-e29b-41d4-a716-446655440000",
  "timestamp": "2024-01-21T12:00:00.000Z",
  "expires_at": "2024-01-21T12:30:00.000Z",
  "user_id": "user_12345",
  "payment": {
    "method": "card",
    "instrument": {
      "type": "verifiable_credential",
      "vc_id": "vc_payment_abc123",
      "stub": {
        "last_four": "1234",
        "brand": "visa",
        "exp_month": 12,
        "exp_year": 2025,
        "holder_name": "John Doe"
      }
    },
    "amount": 11.88,
    "currency": "USD",
    "merchant_id": "merchant_abc123",
    "processing_options": {
      "capture": true,
      "three_d_secure": "challenge_if_available",
      "risk_assessment": "standard"
    }
  },
  "signature": {
    "algorithm": "ES256",
    "public_key": "04a1b2c3d4e5f6...",
    "signature": "3045022100a1b2c3d4e5f6..."
  }
}
```

**Required Fields:**
- `type`: Must be "PaymentMandate"
- `version`: Contract version
- `id`: Unique mandate identifier
- `timestamp`: ISO 8601 timestamp of creation
- `expires_at`: ISO 8601 timestamp of expiration
- `user_id`: Identifier of the user
- `payment`: Object containing payment method and processing details
- `signature`: Digital signature for mandate validation

### ActorProfile

Describes the identity and capabilities of an agent.

```json
{
  "type": "ActorProfile",
  "version": "2.0",
  "id": "actor_orca_decision_engine_v1",
  "timestamp": "2024-01-21T12:00:00.000Z",
  "actor": {
    "id": "orca_decision_engine_v1",
    "name": "Orca Decision Engine",
    "type": "decision_agent",
    "version": "1.0.0",
    "capabilities": [
      "payment_authorization",
      "risk_assessment",
      "fraud_detection",
      "ml_inference"
    ],
    "endpoints": {
      "api": "https://api.ocn.orca.com/v1",
      "health": "https://api.ocn.orca.com/health",
      "metrics": "https://api.ocn.orca.com/metrics"
    },
    "metadata": {
      "provider": "OCN",
      "environment": "production",
      "region": "us-east-1",
      "supported_currencies": ["USD", "EUR", "GBP"],
      "max_amount": 50000.00,
      "processing_time_ms": 200
    }
  },
  "signature": {
    "algorithm": "ES256",
    "public_key": "04a1b2c3d4e5f6...",
    "signature": "3045022100a1b2c3d4e5f6..."
  }
}
```

**Required Fields:**
- `type`: Must be "ActorProfile"
- `version`: Contract version
- `id`: Unique actor identifier
- `timestamp`: ISO 8601 timestamp of creation
- `actor`: Object containing actor identity and capabilities
- `signature`: Digital signature for profile validation

### Agent Presence

Indicates agent availability and processing modality.

```json
{
  "type": "AgentPresence",
  "version": "2.0",
  "id": "presence_orca_550e8400-e29b-41d4-a716-446655440000",
  "timestamp": "2024-01-21T12:00:00.000Z",
  "expires_at": "2024-01-21T13:00:00.000Z",
  "actor_id": "orca_decision_engine_v1",
  "presence": {
    "status": "available",
    "modality": "realtime",
    "capacity": {
      "current_load": 0.65,
      "max_concurrent": 1000,
      "estimated_wait_time_ms": 150
    },
    "capabilities": [
      "payment_authorization",
      "risk_assessment",
      "fraud_detection"
    ],
    "supported_mandates": [
      "IntentMandate",
      "PaymentMandate"
    ],
    "metadata": {
      "region": "us-east-1",
      "version": "1.0.0",
      "last_health_check": "2024-01-21T12:00:00.000Z"
    }
  },
  "signature": {
    "algorithm": "ES256",
    "public_key": "04a1b2c3d4e5f6...",
    "signature": "3045022100a1b2c3d4e5f6..."
  }
}
```

**Required Fields:**
- `type`: Must be "AgentPresence"
- `version`: Contract version
- `id`: Unique presence identifier
- `timestamp`: ISO 8601 timestamp of creation
- `expires_at`: ISO 8601 timestamp of expiration
- `actor_id`: Identifier of the actor
- `presence`: Object containing availability and capability information
- `signature`: Digital signature for presence validation

## Modality Types

### Realtime
- Immediate processing with sub-second response times
- Suitable for interactive transactions
- Requires low-latency infrastructure

### Near-realtime
- Processing within 1-5 seconds
- Suitable for most payment scenarios
- Balanced performance and cost

### Batch
- Processing within minutes to hours
- Suitable for non-urgent operations
- Cost-optimized processing

### Scheduled
- Processing at specific times
- Suitable for recurring operations
- Predictable resource usage

## Validation Rules

### Mandate Validation
1. **Signature Verification**: All mandates must have valid cryptographic signatures
2. **Expiration Check**: Mandates must not be expired
3. **Version Compatibility**: Mandates must use supported contract versions
4. **Required Fields**: All required fields must be present and non-empty
5. **Data Integrity**: Mandate data must be consistent and valid

### Actor Profile Validation
1. **Identity Verification**: Actor identity must be cryptographically verifiable
2. **Capability Declaration**: Capabilities must be accurately declared
3. **Endpoint Validation**: API endpoints must be accessible and valid
4. **Metadata Consistency**: Metadata must be consistent with capabilities

### Presence Validation
1. **Freshness Check**: Presence data must be recent and not stale
2. **Capacity Accuracy**: Capacity metrics must be accurate
3. **Capability Alignment**: Declared capabilities must match actor profile
4. **Health Status**: Health indicators must be current

## Security Considerations

### Digital Signatures
- All mandates and profiles must be digitally signed
- Use ES256 (ECDSA with P-256) for signature algorithms
- Public keys must be verifiable through a trusted PKI

### Data Privacy
- No raw PCI/PII data in mandates
- Use verifiable credentials for sensitive information
- Implement data minimization principles

### Access Control
- Mandates are non-transferable and user-specific
- Actor profiles must be registered and verified
- Presence data must be authenticated

## Implementation Guidelines

### Mandate Lifecycle
1. **Creation**: User creates mandate with digital signature
2. **Transmission**: Mandate transmitted securely to processing agent
3. **Validation**: Agent validates signature and expiration
4. **Processing**: Agent processes request according to mandate
5. **Expiration**: Mandate automatically expires after specified time

### Error Handling
- Invalid signatures result in immediate rejection
- Expired mandates are rejected with appropriate error codes
- Missing required fields trigger validation errors
- Malformed data is rejected with detailed error messages

### Performance Considerations
- Mandates should be as small as possible
- Use efficient serialization formats (JSON)
- Implement caching for frequently accessed actor profiles
- Monitor signature verification performance

## Examples

### Complete Transaction Flow
```json
{
  "intent_mandate": {
    "type": "IntentMandate",
    "id": "intent_001",
    "intent": {
      "action": "purchase",
      "amount": 25.99,
      "merchant_id": "merchant_123"
    }
  },
  "payment_mandate": {
    "type": "PaymentMandate",
    "id": "payment_001",
    "payment": {
      "method": "card",
      "amount": 25.99,
      "instrument": {
        "type": "verifiable_credential",
        "vc_id": "vc_abc123"
      }
    }
  },
  "actor_profile": {
    "type": "ActorProfile",
    "actor": {
      "id": "orca_v1",
      "capabilities": ["payment_authorization", "risk_assessment"]
    }
  }
}
```

This specification provides the foundation for secure, interoperable agent communication within the OCN ecosystem.

