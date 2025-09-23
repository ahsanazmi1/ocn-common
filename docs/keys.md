# Key Handling Principles for OCN

## Overview

This document outlines the key handling principles, security requirements, and rotation policies for the Open Checkout Network (OCN). It covers cryptographic key management, verifiable credentials, and data protection strategies.

## Core Principles

### 1. No Raw PCI/PII Storage

**Principle**: Never store raw payment card data or personally identifiable information in plaintext.

**Implementation**:
- Use verifiable credentials (VCs) for sensitive data references
- Implement field-level encryption for any stored sensitive data
- Use tokenization for payment instruments
- Apply data minimization - only store what's necessary

**Examples**:
```json
// ❌ NEVER store raw card data
{
  "card_number": "4111111111111111",
  "cvv": "123",
  "expiry": "12/25"
}

// ✅ Use verifiable credential stubs
{
  "payment_instrument": {
    "type": "verifiable_credential",
    "vc_id": "vc_payment_abc123",
    "stub": {
      "last_four": "1111",
      "brand": "visa",
      "exp_month": 12,
      "exp_year": 2025,
      "holder_name": "John Doe"
    }
  }
}
```

### 2. Verifiable Credential Stubs

**Principle**: Use cryptographically verifiable credential stubs for sensitive data references.

**Components**:
- **VC ID**: Unique identifier for the verifiable credential
- **Stub Data**: Non-sensitive reference information
- **Proof**: Cryptographic proof of credential validity
- **Metadata**: Additional context without exposing sensitive data

**Example VC Stub**:
```json
{
  "verifiable_credential": {
    "id": "vc_payment_abc123",
    "type": "PaymentCredential",
    "issuer": "https://issuer.ocn.com",
    "issuance_date": "2024-01-15T10:00:00.000Z",
    "expiration_date": "2025-01-15T10:00:00.000Z",
    "stub": {
      "last_four": "1111",
      "brand": "visa",
      "exp_month": 12,
      "exp_year": 2025,
      "holder_name": "John Doe",
      "billing_address": {
        "city": "San Francisco",
        "state": "CA",
        "zip_code": "94105"
      }
    },
    "proof": {
      "type": "Ed25519Signature2020",
      "created": "2024-01-15T10:00:00.000Z",
      "verification_method": "did:ocn:issuer#key-1",
      "proof_purpose": "assertionMethod",
      "jws": "eyJhbGciOiJFZERTQSIsImI2NCI6ZmFsc2UsImNyaXQiOlsiYjY0Il19..."
    }
  }
}
```

### 3. Cryptographic Key Management

**Principle**: Implement robust cryptographic key management with proper rotation and access controls.

**Key Types**:
- **Signing Keys**: For digital signatures on mandates and credentials
- **Encryption Keys**: For data encryption at rest and in transit
- **HMAC Keys**: For message authentication and integrity
- **Derived Keys**: For specific use cases and data types

**Key Storage**:
```json
{
  "key_management": {
    "signing_keys": {
      "algorithm": "ES256",
      "key_id": "signing_key_v1",
      "public_key": "04a1b2c3d4e5f6...",
      "created": "2024-01-01T00:00:00.000Z",
      "expires": "2024-12-31T23:59:59.000Z",
      "status": "active",
      "usage": ["mandate_signing", "credential_signing"]
    },
    "encryption_keys": {
      "algorithm": "AES-256-GCM",
      "key_id": "encryption_key_v1",
      "created": "2024-01-01T00:00:00.000Z",
      "expires": "2024-12-31T23:59:59.000Z",
      "status": "active",
      "usage": ["data_encryption", "field_encryption"]
    }
  }
}
```

## Key Rotation Policy

### Rotation Schedule

| Key Type | Rotation Frequency | Grace Period | Notification |
|----------|-------------------|--------------|--------------|
| Signing Keys | Annual | 30 days | 90 days advance |
| Encryption Keys | Annual | 7 days | 30 days advance |
| HMAC Keys | Quarterly | 3 days | 14 days advance |
| API Keys | Monthly | 1 day | 7 days advance |

### Rotation Process

#### 1. Pre-Rotation Phase
```json
{
  "rotation_phase": "pre_rotation",
  "new_key": {
    "algorithm": "ES256",
    "key_id": "signing_key_v2",
    "public_key": "04b2c3d4e5f6a7...",
    "created": "2024-11-01T00:00:00.000Z",
    "expires": "2025-10-31T23:59:59.000Z",
    "status": "pending"
  },
  "old_key": {
    "key_id": "signing_key_v1",
    "status": "active",
    "rotation_date": "2024-12-01T00:00:00.000Z"
  }
}
```

#### 2. Active Rotation Phase
```json
{
  "rotation_phase": "active_rotation",
  "dual_keys": {
    "primary": "signing_key_v2",
    "secondary": "signing_key_v1",
    "start_date": "2024-12-01T00:00:00.000Z",
    "end_date": "2024-12-31T23:59:59.000Z"
  },
  "validation": {
    "new_key_tests": "passed",
    "old_key_compatibility": "verified",
    "rollback_capability": "confirmed"
  }
}
```

#### 3. Post-Rotation Phase
```json
{
  "rotation_phase": "post_rotation",
  "active_key": {
    "key_id": "signing_key_v2",
    "status": "active",
    "activated": "2024-12-01T00:00:00.000Z"
  },
  "retired_key": {
    "key_id": "signing_key_v1",
    "status": "retired",
    "retired": "2024-12-31T23:59:59.000Z",
    "retention_until": "2025-06-30T23:59:59.000Z"
  }
}
```

### Emergency Rotation

**Trigger Conditions**:
- Suspected key compromise
- Cryptographic vulnerability discovery
- Regulatory requirement
- Security incident

**Emergency Process**:
```json
{
  "emergency_rotation": {
    "trigger": "suspected_compromise",
    "incident_id": "SEC-2024-001",
    "affected_keys": ["signing_key_v1"],
    "new_key": {
      "key_id": "signing_key_emergency",
      "created": "2024-01-21T12:00:00.000Z",
      "status": "active"
    },
    "notification": {
      "sent_to": ["security@ocn.com", "ops@ocn.com"],
      "timestamp": "2024-01-21T12:05:00.000Z"
    }
  }
}
```

## Key Derivation

### Hierarchical Key Derivation

**Principle**: Derive specific keys from master keys using HKDF (HMAC-based Key Derivation Function).

```json
{
  "key_derivation": {
    "master_key": "mk_abc123",
    "derived_keys": {
      "user_encryption": {
        "key_id": "uk_user_12345",
        "derivation_info": "user_encryption_v1",
        "usage": "user_data_encryption"
      },
      "session_encryption": {
        "key_id": "sk_session_xyz789",
        "derivation_info": "session_encryption_v1",
        "usage": "session_data_encryption"
      },
      "audit_signing": {
        "key_id": "ak_audit_456",
        "derivation_info": "audit_signing_v1",
        "usage": "audit_log_signing"
      }
    }
  }
}
```

### Context-Based Derivation

```python
import hkdf
import hashlib

def derive_key(master_key: bytes, context: str, length: int = 32) -> bytes:
    """Derive a key for specific context using HKDF."""
    info = f"ocn_key_derivation_{context}_v1".encode()
    return hkdf.Hkdf(
        algorithm=hashlib.sha256,
        length=length,
        salt=None,
        info=info,
        master=master_key
    ).derive()

# Example usage
user_key = derive_key(master_key, "user_encryption", 32)
session_key = derive_key(master_key, "session_encryption", 32)
audit_key = derive_key(master_key, "audit_signing", 32)
```

## Access Control

### Key Access Policies

```json
{
  "access_policies": {
    "signing_keys": {
      "read": ["orchestrator", "validator"],
      "write": ["key_manager"],
      "admin": ["security_admin"]
    },
    "encryption_keys": {
      "read": ["orchestrator", "encryption_service"],
      "write": ["key_manager"],
      "admin": ["security_admin"]
    },
    "api_keys": {
      "read": ["service_owner"],
      "write": ["service_owner", "key_manager"],
      "admin": ["security_admin"]
    }
  }
}
```

### Role-Based Access

| Role | Signing Keys | Encryption Keys | API Keys | Audit Access |
|------|--------------|-----------------|----------|--------------|
| Security Admin | Full | Full | Full | Full |
| Key Manager | Rotate | Rotate | Rotate | Read |
| Service Owner | Read | Read | Manage | Read |
| Developer | None | None | Read | None |
| Auditor | Read | None | None | Full |

## Key Validation

### Signature Validation

```python
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.utils import decode_dss_signature
import base64

def validate_signature(public_key_pem: str, message: bytes, signature: str) -> bool:
    """Validate ECDSA signature."""
    try:
        # Load public key
        public_key = serialization.load_pem_public_key(public_key_pem.encode())

        # Decode signature
        signature_bytes = base64.b64decode(signature)
        r, s = decode_dss_signature(signature_bytes)

        # Verify signature
        public_key.verify(
            signature_bytes,
            message,
            ec.ECDSA(hashes.SHA256())
        )
        return True
    except Exception:
        return False
```

### Key Expiration Check

```python
from datetime import datetime, timezone

def is_key_expired(key_metadata: dict) -> bool:
    """Check if key is expired."""
    if key_metadata.get("status") != "active":
        return True

    expires_at = datetime.fromisoformat(
        key_metadata["expires"].replace("Z", "+00:00")
    )
    return datetime.now(timezone.utc) > expires_at
```

## Compliance Requirements

### PCI DSS Compliance

**Requirements**:
- No storage of card verification values (CVV)
- Encryption of stored cardholder data
- Secure key management
- Regular security testing

**Implementation**:
```json
{
  "pci_compliance": {
    "card_data_handling": {
      "storage": "prohibited",
      "transmission": "encrypted_tls_1_3",
      "processing": "memory_only",
      "logging": "tokenized_only"
    },
    "key_management": {
      "rotation": "annual",
      "encryption": "aes_256",
      "access": "role_based",
      "audit": "continuous"
    }
  }
}
```

### GDPR Compliance

**Requirements**:
- Data minimization
- Purpose limitation
- Storage limitation
- Right to erasure

**Implementation**:
```json
{
  "gdpr_compliance": {
    "data_minimization": {
      "principle": "collect_only_necessary",
      "implementation": "vc_stubs_only"
    },
    "storage_limitation": {
      "retention_period": "7_years",
      "automatic_deletion": true
    },
    "right_to_erasure": {
      "process": "automated",
      "timeframe": "30_days"
    }
  }
}
```

## Monitoring and Alerting

### Key Health Monitoring

```json
{
  "monitoring": {
    "key_expiration": {
      "alert_threshold": "30_days",
      "critical_threshold": "7_days",
      "notification_channels": ["email", "slack", "pagerduty"]
    },
    "key_usage": {
      "anomaly_detection": true,
      "rate_limiting": true,
      "geographic_monitoring": true
    },
    "key_rotation": {
      "success_rate": "99.9%",
      "rollback_capability": true,
      "audit_logging": true
    }
  }
}
```

### Audit Trail

```json
{
  "audit_trail": {
    "event_id": "audit_550e8400-e29b-41d4-a716-446655440000",
    "timestamp": "2024-01-21T12:00:00.000Z",
    "event_type": "key_rotation",
    "actor": {
      "type": "service",
      "id": "key_manager_service",
      "version": "1.0.0"
    },
    "target": {
      "type": "key",
      "id": "signing_key_v1"
    },
    "action": "rotate",
    "result": "success",
    "details": {
      "old_key_id": "signing_key_v1",
      "new_key_id": "signing_key_v2",
      "rotation_reason": "scheduled"
    },
    "compliance": {
      "pci_dss": true,
      "gdpr": true,
      "sox": true
    }
  }
}
```

## Implementation Guidelines

### Key Generation

```python
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
import secrets

def generate_ecdsa_keypair() -> tuple[str, str]:
    """Generate ECDSA P-256 keypair."""
    private_key = ec.generate_private_key(ec.SECP256R1())

    # Serialize private key
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    # Serialize public key
    public_key = private_key.public_key()
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    return private_pem.decode(), public_pem.decode()
```

### Key Storage

```python
import boto3
from cryptography.fernet import Fernet
import json

class KeyManager:
    def __init__(self, kms_client, s3_client):
        self.kms_client = kms_client
        self.s3_client = s3_client

    def store_key(self, key_id: str, key_data: bytes, metadata: dict):
        """Store encrypted key in S3 with KMS encryption."""
        # Encrypt key data with KMS
        response = self.kms_client.encrypt(
            KeyId='alias/ocn-key-encryption',
            Plaintext=key_data
        )

        # Store in S3
        self.s3_client.put_object(
            Bucket='ocn-keys',
            Key=f'keys/{key_id}',
            Body=response['CiphertextBlob'],
            Metadata=metadata
        )

    def retrieve_key(self, key_id: str) -> bytes:
        """Retrieve and decrypt key from S3."""
        # Get encrypted key from S3
        response = self.s3_client.get_object(
            Bucket='ocn-keys',
            Key=f'keys/{key_id}'
        )

        # Decrypt with KMS
        decrypt_response = self.kms_client.decrypt(
            CiphertextBlob=response['Body'].read()
        )

        return decrypt_response['Plaintext']
```

This key handling specification ensures secure, compliant, and auditable cryptographic operations across the OCN ecosystem.

