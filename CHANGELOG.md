# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.0] - 2025-01-24

### Added
- **Phase 2 Explainability CloudEvents**: Complete schema definitions for Orion, Okra, and Onyx
  - `orion.explanation.v1` - Payout optimization explanations with rail scoring and selection reasoning
  - `okra.bnpl_quote.v1` - BNPL scoring and quote generation with deterministic outputs
  - `onyx.kyb_verified.v1` - KYB verification results with comprehensive check details
- **Example CloudEvents**: Complete working examples for all Phase 2 event types
- **Contract Validation**: Registration of Phase 2 event types in validation system
- **Comprehensive Test Suite**: 15 test scenarios covering all Phase 2 event validation
- **Documentation**: Complete Phase 2 event reference in CloudEvents documentation
- **README Updates**: Added Okra to OCN Ecosystem and organized event schemas by category

### Changed
- Enhanced contract validation system to support Phase 2 explainability events
- Reorganized event schema documentation by category (Decision, Credit, Payout, Verification, Audit)

### Deprecated
- None

### Removed
- None

### Fixed
- None

### Security
- None

## [Unreleased — Phase 2]

### Added
- Enhanced explainability schemas for OCN agents
- CloudEvents validation for explainability events
- Contract validation for Phase 2 explainability features
- Documentation scaffolding for Phase 2 development

### Changed
- None

### Deprecated
- None

### Removed
- None

### Fixed
- None

### Security
- None

## [Unreleased — Phase 1]

### Added
- Initial release of OCN Common library
- Event schemas for OCN agents (Orca, Weave, etc.)
- Contract validation utilities
- Trace and observability utilities
- JSON schema validation for CloudEvents

### Changed
- None

### Deprecated
- None

### Removed
- None

### Fixed
- None

### Security
- None

## [0.1.0] - 2025-01-23

### Added
- Initial release
- Core OCN event schemas
- Contract validation framework
- Trace middleware for distributed tracing
- CloudEvents integration
- JSON schema validation utilities

[Unreleased]: https://github.com/ocn-ai/ocn-common/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/ocn-ai/ocn-common/releases/tag/v0.1.0
