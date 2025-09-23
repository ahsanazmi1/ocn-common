# OCN Common — Shared Libraries for the Open Checkout Network

[![Contracts Validation](https://github.com/ocn-ai/ocn-common/actions/workflows/contracts.yml/badge.svg)](https://github.com/ocn-ai/ocn-common/actions/workflows/contracts.yml)
[![Security Validation](https://github.com/ocn-ai/ocn-common/actions/workflows/security.yml/badge.svg)](https://github.com/ocn-ai/ocn-common/actions/workflows/security.yml)
[![CI](https://github.com/ocn-ai/ocn-common/actions/workflows/ci.yml/badge.svg)](https://github.com/ocn-ai/ocn-common/actions/workflows/ci.yml)

**OCN Common** provides shared libraries, schemas, and utilities for the [Open Checkout Network (OCN)](https://github.com/ocn-ai/ocn-common) ecosystem.

## Purpose

OCN Common serves as the foundation for all OCN agents and services, providing:

- **Event Schemas** - Standardized CloudEvents schemas for OCN agents
- **Contract Validation** - JSON schema validation utilities
- **Trace Utilities** - Distributed tracing and observability tools
- **Shared Types** - Common data types and structures

## Quickstart (≤ 60s)

```bash
# Clone and setup
git clone https://github.com/ocn-ai/ocn-common.git
cd ocn-common

# Setup development environment
make setup

# Run tests
make test

# See usage examples
make run
```

### Available Make Commands

- `make setup` - Create venv, install deps + dev extras, install pre-commit hooks
- `make lint` - Run ruff and black checks
- `make fmt` - Format code with black
- `make test` - Run pytest with coverage (≥80%)
- `make run` - Show usage examples and available demos
- `make clean` - Remove virtual environment and cache files
- `make validate-schemas` - Validate all JSON schemas
- `make test-contracts` - Run contract validation tests

## OCN Ecosystem

OCN Common is part of the broader Open Checkout Network ecosystem:

- **[OCN Common](https://github.com/ocn-ai/ocn-common)** - Shared libraries and schemas (this repo)
- **[Orca](https://github.com/ocn-ai/orca)** - Risk decision engine
- **[Weave](https://github.com/ocn-ai/weave)** - Receipt ledger
- **[Opal](https://github.com/ocn-ai/opal)** - Payment orchestration
- **[Onyx](https://github.com/ocn-ai/onyx)** - Trust registry
- **[Olive](https://github.com/ocn-ai/olive)** - Incentive management
- **[Oasis](https://github.com/ocn-ai/oasis)** - Treasury management
- **[Orion](https://github.com/ocn-ai/orion)** - Payout processing

## Event Schemas

OCN Common defines standardized event schemas for inter-agent communication:

### Decision Events
- `orca.decision.v1` - Risk decision outcomes
- `orca.explanation.v1` - Decision explanations

### Audit Events
- `weave.audit.v1` - Receipt audit trails

### Mandate Schemas
- Actor profiles and agent presence
- Payment and cart mandates
- Intent and modality definitions

## Contract Validation

```python
from ocn_common.contracts import validate_event

# Validate a CloudEvent against OCN schemas
is_valid = validate_event(event_data, schema_version="v1")
```

## Trace Utilities

```python
from ocn_common.trace import ensure_trace_id, trace_middleware

# Ensure trace context across OCN services
trace_id = ensure_trace_id()
```

## Development

### Prerequisites
- Python 3.12+
- Git

### Setup
```bash
pip install -e .[dev]
pre-commit install  # if available
```

### Testing
```bash
pytest -q
```

### Code Quality
```bash
ruff check .
black --check .
mypy src/
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed contribution guidelines.

## License

MIT License - see [LICENSE](LICENSE) for details.

## Links

- **Documentation**: [OCN Architecture](https://github.com/ocn-ai/ocn-common/docs)
- **Issues**: [GitHub Issues](https://github.com/ocn-ai/ocn-common/issues)
- **Discussions**: [GitHub Discussions](https://github.com/ocn-ai/ocn-common/discussions)
