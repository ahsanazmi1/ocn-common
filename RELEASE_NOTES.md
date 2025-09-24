# Release Notes - OCN Common v0.2.0

**Release Date**: January 24, 2025
**Version**: 0.2.0
**Previous Version**: 0.1.0

## 🎯 Overview

OCN Common v0.2.0 introduces comprehensive support for Phase 2 explainability features across the Open Checkout Network ecosystem. This release extends the contract validation system with new CloudEvent schemas for Orion, Okra, and Onyx agents, enabling standardized explainability event handling and validation.

## 🚀 New Capabilities

### Phase 2 Explainability CloudEvents

This release adds complete CloudEvent schema definitions for three new OCN agents:

#### **Orion - Payout Optimization**
- **Schema**: `orion.explanation.v1`
- **Purpose**: Payout optimization explanations with rail scoring and selection reasoning
- **Features**:
  - Rail scoring and ranking (ACH, Wire, RTP, V-Card)
  - Cost, speed, and limits analysis
  - Explanation with signals, mitigation strategies, and confidence scores
  - Context-aware optimization decisions

#### **Okra - BNPL Scoring**
- **Schema**: `okra.bnpl_quote.v1`
- **Purpose**: Buy Now, Pay Later scoring and quote generation
- **Features**:
  - Deterministic scoring with key signals (amount, tenor, payment history, utilization)
  - Quote generation (credit limit, APR, term, monthly payment)
  - Customer credit profile integration
  - Risk assessment and scoring transparency

#### **Onyx - KYB Verification**
- **Schema**: `onyx.kyb_verified.v1`
- **Purpose**: Know Your Business verification results
- **Features**:
  - Multi-check verification system (jurisdiction, age, sanctions, business validation)
  - Detailed check results with individual status and reasoning
  - Comprehensive verification metadata
  - Compliance and audit trail support

### Enhanced Contract Validation

- **New Event Types**: Added validation support for all Phase 2 event types
- **Schema Registration**: Automatic registration in contract validation system
- **Error Handling**: Comprehensive validation error reporting
- **Type Safety**: Full type checking and enum validation

## 📋 Contract Validation Status

### ✅ Fully Validated Schemas
- `ocn.orion.explanation.v1` - Payout optimization explanations
- `ocn.okra.bnpl_quote.v1` - BNPL scoring and quotes
- `ocn.onyx.kyb_verified.v1` - KYB verification results

### ✅ CloudEvent Compliance
All new schemas include required CloudEvent v1.0 attributes:
- `specversion`, `id`, `source`, `type`, `subject`, `time`, `datacontenttype`
- Proper enum constraints and type validation
- Comprehensive data payload validation

### ✅ Example Validation
- Complete working examples for all Phase 2 event types
- All examples validate against their respective schemas
- Ready-to-use CloudEvent templates

## 🧪 Testing & Quality

### Test Coverage
- **67/67 tests passing** (92% coverage)
- **15 new test scenarios** for Phase 2 event validation
- Comprehensive validation of all event types and edge cases
- Error handling and malformed data testing

### Quality Assurance
- All linting and formatting checks pass
- Type checking with mypy
- Security scanning with bandit
- Pre-commit hooks enforced

## 📚 Documentation

### Updated Documentation
- **README.md**: Added Okra to OCN Ecosystem, organized event schemas by category
- **cloudevents_reference.md**: Complete Phase 2 event documentation with examples
- **CHANGELOG.md**: Comprehensive change tracking

### New Documentation Sections
- **Credit Events**: BNPL scoring and quotes
- **Payout Events**: Optimization explanations
- **Verification Events**: KYB verification results

## 🔧 Technical Details

### Schema Structure
Each Phase 2 schema includes:
- **Required Attributes**: Full CloudEvent v1.0 compliance
- **Data Validation**: Comprehensive payload validation
- **Type Safety**: Proper enum constraints and type checking
- **Extensibility**: Metadata fields for future enhancements

### Validation System
- **Automatic Registration**: New event types automatically available for validation
- **Error Reporting**: Detailed validation error messages
- **Schema Caching**: Optimized performance with schema caching
- **Type Mapping**: Clean mapping between CloudEvent types and schema files

## 🎯 Usage Examples

### Basic Validation
```python
from ocn_common.contracts import validate_cloudevent

# Validate Orion payout optimization explanation
is_valid = validate_cloudevent(event_data, "ocn.orion.explanation.v1")

# Validate Okra BNPL quote
is_valid = validate_cloudevent(event_data, "ocn.okra.bnpl_quote.v1")

# Validate Onyx KYB verification
is_valid = validate_cloudevent(event_data, "ocn.onyx.kyb_verified.v1")
```

### Schema Access
```python
from ocn_common.contracts import get_contract_validator

validator = get_contract_validator()
schema = validator.schema_loader.get_schema("orion.explanation.v1", "events")
```

## 🔄 Migration Guide

### For Existing Users
- **No Breaking Changes**: All existing functionality remains unchanged
- **Backward Compatible**: Previous event types continue to work
- **Enhanced Validation**: New Phase 2 event types available immediately

### For New Phase 2 Integrations
1. **Install**: `pip install ocn-common==0.2.0`
2. **Import**: Use existing validation functions
3. **Validate**: New event types automatically recognized
4. **Examples**: Reference example files in `examples/events/`

## 🏗️ Architecture Impact

### OCN Ecosystem Integration
- **Orion**: Payout optimization explanations now standardized
- **Okra**: BNPL scoring events fully documented and validated
- **Onyx**: KYB verification results with comprehensive schemas
- **Cross-Agent**: Consistent explainability event handling

### Contract System
- **Extensible**: Easy addition of future event types
- **Validated**: All schemas tested and verified
- **Documented**: Complete reference documentation
- **Maintained**: Ongoing schema evolution support

## 📈 Performance

- **Schema Caching**: Optimized validation performance
- **Minimal Overhead**: Efficient validation processing
- **Memory Efficient**: Smart schema loading and caching
- **Fast Validation**: Quick event validation with detailed error reporting

## 🔮 Future Roadmap

### Phase 3 Planning
- Additional agent event types
- Enhanced validation features
- Performance optimizations
- Extended documentation

### Community Contributions
- Schema contributions welcome
- Validation improvements
- Documentation enhancements
- Example additions

---

## 📞 Support

For questions, issues, or contributions:
- **GitHub Issues**: [ocn-ai/ocn-common](https://github.com/ocn-ai/ocn-common/issues)
- **Documentation**: [README.md](./README.md)
- **Examples**: [examples/events/](./examples/events/)

---

**OCN Common v0.2.0** - Enabling Phase 2 Explainability Across the Open Checkout Network
