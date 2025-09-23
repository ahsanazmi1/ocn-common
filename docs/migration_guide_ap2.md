# AP2 Migration Guide

## Overview

This guide provides step-by-step instructions for migrating from pre-AP2 input formats to AP2 mandate structures. It includes field mapping tables, transformation examples, and validation requirements.

## Migration Principles

### 1. Backward Compatibility
- Support both pre-AP2 and AP2 formats during transition period
- Provide automatic format detection and conversion
- Maintain data integrity throughout migration process

### 2. Data Transformation
- Map pre-AP2 fields to AP2 mandate structures
- Preserve all original data while adding AP2 enhancements
- Handle missing or optional fields gracefully

### 3. Validation and Testing
- Validate all migrated mandates against AP2 schemas
- Test migration with production-like data
- Implement rollback capabilities for failed migrations

## Field Mapping Tables

### Payment Request → PaymentMandate

| Pre-AP2 Field | AP2 Field | Type | Required | Notes |
|---------------|-----------|------|----------|-------|
| `payment_method` | `payment.method` | String | Yes | Direct mapping |
| `card_number` | `payment.instrument.vc_id` | String | Yes | Convert to VC reference |
| `card_type` | `payment.instrument.stub.brand` | String | Yes | Map to standard brands |
| `expiry_month` | `payment.instrument.stub.exp_month` | Integer | Yes | Direct mapping |
| `expiry_year` | `payment.instrument.stub.exp_year` | Integer | Yes | Direct mapping |
| `cvv` | `payment.instrument.stub.cvv_hash` | String | No | Hash CVV, don't store raw |
| `holder_name` | `payment.instrument.stub.holder_name` | String | Yes | Direct mapping |
| `amount` | `payment.amount` | Decimal | Yes | Direct mapping |
| `currency` | `payment.currency` | String | Yes | Direct mapping |
| `merchant_id` | `payment.merchant_id` | String | Yes | Direct mapping |
| `capture` | `payment.processing_options.capture` | Boolean | No | Default to true |
| `three_d_secure` | `payment.processing_options.three_d_secure` | String | No | Map to standard values |

### Transaction Request → IntentMandate

| Pre-AP2 Field | AP2 Field | Type | Required | Notes |
|---------------|-----------|------|----------|-------|
| `transaction_type` | `intent.action` | String | Yes | Map to standard actions |
| `amount` | `intent.amount` | Decimal | Yes | Direct mapping |
| `currency` | `intent.currency` | String | Yes | Direct mapping |
| `merchant_id` | `intent.merchant_id` | String | Yes | Direct mapping |
| `description` | `intent.description` | String | No | Direct mapping |
| `mcc_code` | `intent.metadata.mcc` | String | No | Move to metadata |
| `channel` | `intent.metadata.channel` | String | No | Move to metadata |
| `location.lat` | `intent.metadata.location.latitude` | Decimal | No | Restructure location |
| `location.lng` | `intent.metadata.location.longitude` | Decimal | No | Restructure location |
| `user_id` | `user_id` | String | Yes | Move to top level |
| `session_id` | `intent.metadata.session_id` | String | No | Move to metadata |

### Shopping Cart → CartMandate

| Pre-AP2 Field | AP2 Field | Type | Required | Notes |
|---------------|-----------|------|----------|-------|
| `items[]` | `cart.items[]` | Array | Yes | Restructure item format |
| `items[].id` | `cart.items[].id` | String | Yes | Direct mapping |
| `items[].name` | `cart.items[].name` | String | Yes | Direct mapping |
| `items[].quantity` | `cart.items[].quantity` | Integer | Yes | Direct mapping |
| `items[].price` | `cart.items[].unit_price` | Decimal | Yes | Rename field |
| `items[].total` | `cart.items[].total_price` | Decimal | Yes | Rename field |
| `items[].category` | `cart.items[].category` | String | No | Direct mapping |
| `subtotal` | `cart.subtotal` | Decimal | Yes | Direct mapping |
| `tax_amount` | `cart.tax` | Decimal | No | Rename field |
| `total_amount` | `cart.total` | Decimal | Yes | Rename field |
| `currency` | `cart.currency` | String | Yes | Direct mapping |

## Migration Examples

### Example 1: Payment Request Migration

#### Pre-AP2 Format
```json
{
  "payment_request": {
    "id": "req_12345",
    "payment_method": "card",
    "card_number": "4111111111111111",
    "card_type": "visa",
    "expiry_month": 12,
    "expiry_year": 2025,
    "cvv": "123",
    "holder_name": "John Doe",
    "amount": 99.99,
    "currency": "USD",
    "merchant_id": "merchant_abc123",
    "capture": true,
    "three_d_secure": "challenge_if_available",
    "user_id": "user_12345",
    "timestamp": "2024-01-21T12:00:00.000Z"
  }
}
```

#### AP2 PaymentMandate
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
        "last_four": "1111",
        "brand": "visa",
        "exp_month": 12,
        "exp_year": 2025,
        "holder_name": "John Doe"
      }
    },
    "amount": 99.99,
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

### Example 2: Transaction Request Migration

#### Pre-AP2 Format
```json
{
  "transaction_request": {
    "id": "txn_67890",
    "transaction_type": "purchase",
    "amount": 25.99,
    "currency": "USD",
    "merchant_id": "merchant_xyz789",
    "description": "Coffee purchase",
    "mcc_code": "5814",
    "channel": "pos",
    "location": {
      "lat": 37.7749,
      "lng": -122.4194
    },
    "user_id": "user_12345",
    "session_id": "sess_abc123",
    "timestamp": "2024-01-21T12:00:00.000Z"
  }
}
```

#### AP2 IntentMandate
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
    "merchant_id": "merchant_xyz789",
    "amount": 25.99,
    "currency": "USD",
    "description": "Coffee purchase",
    "metadata": {
      "mcc": "5814",
      "channel": "pos",
      "session_id": "sess_abc123",
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

### Example 3: Shopping Cart Migration

#### Pre-AP2 Format
```json
{
  "shopping_cart": {
    "id": "cart_11111",
    "items": [
      {
        "id": "item_001",
        "name": "Coffee - Large",
        "quantity": 1,
        "price": 4.50,
        "total": 4.50,
        "category": "beverages"
      },
      {
        "id": "item_002",
        "name": "Croissant",
        "quantity": 2,
        "price": 3.25,
        "total": 6.50,
        "category": "food"
      }
    ],
    "subtotal": 11.00,
    "tax_amount": 0.88,
    "total_amount": 11.88,
    "currency": "USD",
    "merchant_id": "merchant_abc123",
    "user_id": "user_12345",
    "timestamp": "2024-01-21T12:00:00.000Z"
  }
}
```

#### AP2 CartMandate
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

## Migration Implementation

### Python Migration Service

```python
import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec

class AP2Migrator:
    def __init__(self, private_key_pem: str):
        """Initialize migrator with signing key."""
        self.private_key = serialization.load_pem_private_key(
            private_key_pem.encode(),
            password=None
        )

    def migrate_payment_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Migrate pre-AP2 payment request to PaymentMandate."""

        # Generate new mandate ID
        mandate_id = f"payment_{uuid.uuid4()}"

        # Create VC stub for payment instrument
        vc_stub = {
            "last_four": request["card_number"][-4:],
            "brand": self._map_card_type(request["card_type"]),
            "exp_month": request["expiry_month"],
            "exp_year": request["expiry_year"],
            "holder_name": request["holder_name"]
        }

        # Build payment mandate
        mandate = {
            "type": "PaymentMandate",
            "version": "2.0",
            "id": mandate_id,
            "timestamp": request["timestamp"],
            "expires_at": self._calculate_expiry(request["timestamp"]),
            "user_id": request["user_id"],
            "payment": {
                "method": request["payment_method"],
                "instrument": {
                    "type": "verifiable_credential",
                    "vc_id": f"vc_payment_{uuid.uuid4()}",
                    "stub": vc_stub
                },
                "amount": request["amount"],
                "currency": request["currency"],
                "merchant_id": request["merchant_id"],
                "processing_options": {
                    "capture": request.get("capture", True),
                    "three_d_secure": request.get("three_d_secure", "challenge_if_available"),
                    "risk_assessment": "standard"
                }
            }
        }

        # Sign mandate
        mandate["signature"] = self._sign_mandate(mandate)

        return mandate

    def migrate_transaction_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Migrate pre-AP2 transaction request to IntentMandate."""

        # Generate new mandate ID
        mandate_id = f"intent_{uuid.uuid4()}"

        # Build intent mandate
        mandate = {
            "type": "IntentMandate",
            "version": "2.0",
            "id": mandate_id,
            "timestamp": request["timestamp"],
            "expires_at": self._calculate_expiry(request["timestamp"]),
            "user_id": request["user_id"],
            "intent": {
                "action": self._map_transaction_type(request["transaction_type"]),
                "merchant_id": request["merchant_id"],
                "amount": request["amount"],
                "currency": request["currency"],
                "description": request.get("description", ""),
                "metadata": {
                    "mcc": request.get("mcc_code"),
                    "channel": request.get("channel"),
                    "session_id": request.get("session_id"),
                    "location": self._restructure_location(request.get("location"))
                }
            }
        }

        # Sign mandate
        mandate["signature"] = self._sign_mandate(mandate)

        return mandate

    def migrate_shopping_cart(self, cart: Dict[str, Any]) -> Dict[str, Any]:
        """Migrate pre-AP2 shopping cart to CartMandate."""

        # Generate new mandate ID
        mandate_id = f"cart_{uuid.uuid4()}"

        # Migrate cart items
        migrated_items = []
        for item in cart["items"]:
            migrated_item = {
                "id": item["id"],
                "name": item["name"],
                "quantity": item["quantity"],
                "unit_price": item["price"],
                "total_price": item["total"],
                "category": item.get("category"),
                "metadata": {
                    "sku": item.get("sku"),
                    "tax_category": item.get("tax_category", "standard")
                }
            }
            migrated_items.append(migrated_item)

        # Build cart mandate
        mandate = {
            "type": "CartMandate",
            "version": "2.0",
            "id": mandate_id,
            "timestamp": cart["timestamp"],
            "expires_at": self._calculate_expiry(cart["timestamp"]),
            "user_id": cart["user_id"],
            "cart": {
                "items": migrated_items,
                "subtotal": cart["subtotal"],
                "tax": cart.get("tax_amount", 0),
                "total": cart["total_amount"],
                "currency": cart["currency"],
                "merchant_id": cart["merchant_id"]
            }
        }

        # Sign mandate
        mandate["signature"] = self._sign_mandate(mandate)

        return mandate

    def _map_card_type(self, card_type: str) -> str:
        """Map card type to standard brand."""
        mapping = {
            "visa": "visa",
            "mastercard": "mastercard",
            "amex": "american_express",
            "discover": "discover"
        }
        return mapping.get(card_type.lower(), "unknown")

    def _map_transaction_type(self, transaction_type: str) -> str:
        """Map transaction type to standard action."""
        mapping = {
            "purchase": "purchase",
            "refund": "refund",
            "void": "void",
            "capture": "capture"
        }
        return mapping.get(transaction_type.lower(), "purchase")

    def _restructure_location(self, location: Optional[Dict]) -> Optional[Dict]:
        """Restructure location object."""
        if not location:
            return None

        return {
            "latitude": location.get("lat"),
            "longitude": location.get("lng")
        }

    def _calculate_expiry(self, timestamp: str) -> str:
        """Calculate mandate expiry (30 minutes from timestamp)."""
        dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        expiry = dt + timedelta(minutes=30)
        return expiry.isoformat().replace("+00:00", "Z")

    def _sign_mandate(self, mandate: Dict[str, Any]) -> Dict[str, str]:
        """Sign mandate with ECDSA."""
        # Create signature data (exclude signature field)
        signature_data = {k: v for k, v in mandate.items() if k != "signature"}
        message = json.dumps(signature_data, sort_keys=True).encode()

        # Sign message
        signature = self.private_key.sign(
            message,
            ec.ECDSA(hashes.SHA256())
        )

        # Get public key
        public_key = self.private_key.public_key()
        public_key_bytes = public_key.public_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        return {
            "algorithm": "ES256",
            "public_key": public_key_bytes.hex(),
            "signature": signature.hex()
        }

# Usage example
migrator = AP2Migrator(private_key_pem)

# Migrate payment request
payment_mandate = migrator.migrate_payment_request(payment_request)

# Migrate transaction request
intent_mandate = migrator.migrate_transaction_request(transaction_request)

# Migrate shopping cart
cart_mandate = migrator.migrate_shopping_cart(shopping_cart)
```

## Validation and Testing

### Schema Validation

```python
import jsonschema
from jsonschema import validate, ValidationError

def validate_ap2_mandate(mandate: Dict[str, Any], schema: Dict[str, Any]) -> bool:
    """Validate AP2 mandate against schema."""
    try:
        validate(instance=mandate, schema=schema)
        return True
    except ValidationError as e:
        print(f"Validation error: {e.message}")
        return False

# Load AP2 schemas
with open("schemas/payment_mandate_v2.json") as f:
    payment_schema = json.load(f)

with open("schemas/intent_mandate_v2.json") as f:
    intent_schema = json.load(f)

with open("schemas/cart_mandate_v2.json") as f:
    cart_schema = json.load(f)

# Validate migrated mandates
is_valid_payment = validate_ap2_mandate(payment_mandate, payment_schema)
is_valid_intent = validate_ap2_mandate(intent_mandate, intent_schema)
is_valid_cart = validate_ap2_mandate(cart_mandate, cart_schema)
```

### Migration Testing

```python
def test_migration_completeness(pre_ap2_data: Dict, ap2_mandate: Dict) -> bool:
    """Test that all pre-AP2 data is preserved in AP2 mandate."""

    # Test payment request migration
    if "payment_request" in pre_ap2_data:
        payment = pre_ap2_data["payment_request"]
        mandate = ap2_mandate["payment"]

        assert payment["amount"] == mandate["amount"]
        assert payment["currency"] == mandate["currency"]
        assert payment["merchant_id"] == mandate["merchant_id"]
        assert payment["card_number"][-4:] == mandate["instrument"]["stub"]["last_four"]
        assert payment["card_type"] == mandate["instrument"]["stub"]["brand"]
        assert payment["expiry_month"] == mandate["instrument"]["stub"]["exp_month"]
        assert payment["expiry_year"] == mandate["instrument"]["stub"]["exp_year"]
        assert payment["holder_name"] == mandate["instrument"]["stub"]["holder_name"]

    # Test transaction request migration
    if "transaction_request" in pre_ap2_data:
        transaction = pre_ap2_data["transaction_request"]
        mandate = ap2_mandate["intent"]

        assert transaction["amount"] == mandate["amount"]
        assert transaction["currency"] == mandate["currency"]
        assert transaction["merchant_id"] == mandate["merchant_id"]
        assert transaction["description"] == mandate["description"]
        assert transaction["mcc_code"] == mandate["metadata"]["mcc"]
        assert transaction["channel"] == mandate["metadata"]["channel"]

    # Test shopping cart migration
    if "shopping_cart" in pre_ap2_data:
        cart = pre_ap2_data["shopping_cart"]
        mandate = ap2_mandate["cart"]

        assert cart["subtotal"] == mandate["subtotal"]
        assert cart["total_amount"] == mandate["total"]
        assert cart["currency"] == mandate["currency"]
        assert len(cart["items"]) == len(mandate["items"])

        for i, item in enumerate(cart["items"]):
            migrated_item = mandate["items"][i]
            assert item["id"] == migrated_item["id"]
            assert item["name"] == migrated_item["name"]
            assert item["quantity"] == migrated_item["quantity"]
            assert item["price"] == migrated_item["unit_price"]
            assert item["total"] == migrated_item["total_price"]

    return True
```

## Rollback Strategy

### Rollback Implementation

```python
class AP2Rollback:
    def __init__(self, migration_log: str):
        """Initialize rollback with migration log."""
        self.migration_log = migration_log

    def rollback_mandate(self, ap2_mandate: Dict[str, Any]) -> Dict[str, Any]:
        """Rollback AP2 mandate to pre-AP2 format."""

        mandate_type = ap2_mandate["type"]

        if mandate_type == "PaymentMandate":
            return self._rollback_payment_mandate(ap2_mandate)
        elif mandate_type == "IntentMandate":
            return self._rollback_intent_mandate(ap2_mandate)
        elif mandate_type == "CartMandate":
            return self._rollback_cart_mandate(ap2_mandate)
        else:
            raise ValueError(f"Unknown mandate type: {mandate_type}")

    def _rollback_payment_mandate(self, mandate: Dict[str, Any]) -> Dict[str, Any]:
        """Rollback PaymentMandate to payment request format."""
        payment = mandate["payment"]
        instrument = payment["instrument"]
        stub = instrument["stub"]

        return {
            "payment_request": {
                "id": mandate["id"],
                "payment_method": payment["method"],
                "card_number": f"****{stub['last_four']}",  # Masked for security
                "card_type": stub["brand"],
                "expiry_month": stub["exp_month"],
                "expiry_year": stub["exp_year"],
                "holder_name": stub["holder_name"],
                "amount": payment["amount"],
                "currency": payment["currency"],
                "merchant_id": payment["merchant_id"],
                "capture": payment["processing_options"]["capture"],
                "three_d_secure": payment["processing_options"]["three_d_secure"],
                "user_id": mandate["user_id"],
                "timestamp": mandate["timestamp"]
            }
        }
```

## Migration Checklist

### Pre-Migration
- [ ] Backup all pre-AP2 data
- [ ] Validate AP2 schemas
- [ ] Test migration with sample data
- [ ] Implement rollback procedures
- [ ] Set up monitoring and alerting

### During Migration
- [ ] Enable dual-format support
- [ ] Migrate data in batches
- [ ] Validate each migrated mandate
- [ ] Monitor system performance
- [ ] Log all migration activities

### Post-Migration
- [ ] Verify data integrity
- [ ] Test AP2 mandate processing
- [ ] Monitor error rates
- [ ] Update documentation
- [ ] Plan deprecation of pre-AP2 support

This migration guide ensures smooth transition from pre-AP2 formats to AP2 mandates while maintaining data integrity and system reliability.

