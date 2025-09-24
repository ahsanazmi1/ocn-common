# Pull Request

## Overview

Brief description of the changes and their purpose.

## Type of Change

- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update
- [ ] Phase 2 explainability work

## Phase 2 — Explainability Checklist

If this PR includes Phase 2 explainability work, please ensure:

### Tests
- [ ] All tests pass (`make test`)
- [ ] New tests added for explainability features
- [ ] Test coverage maintained or improved
- [ ] Edge cases and error conditions tested

### Contracts & Schemas
- [ ] CloudEvents schemas validated (`make validate-contracts`)
- [ ] JSON schema validation working
- [ ] Contract examples updated
- [ ] Schema versioning handled correctly

### CloudEvents Validation
- [ ] CloudEvents structure validated
- [ ] Event types properly defined
- [ ] Payload schemas validated
- [ ] Trace ID propagation working

### Documentation
- [ ] README.md updated if needed
- [ ] API documentation updated
- [ ] Schema documentation updated
- [ ] Examples provided

### Code Quality
- [ ] Code follows project style guidelines
- [ ] Linting passes (`make lint`)
- [ ] Type checking passes (`make type-check`)
- [ ] Security scan passes (`make security`)

## Testing

### Manual Testing
- [ ] Tested locally with `make test`
- [ ] Tested contract validation
- [ ] Tested CloudEvents emission
- [ ] Tested schema validation

### Automated Testing
- [ ] CI pipeline passes
- [ ] All existing tests continue to pass
- [ ] New functionality has test coverage

## Breaking Changes

- [ ] No breaking changes
- [ ] Breaking changes documented
- [ ] Migration guide provided (if applicable)

## Dependencies

- [ ] No new dependencies added
- [ ] New dependencies documented and justified
- [ ] Dependency versions pinned

## Security Considerations

- [ ] No security vulnerabilities introduced
- [ ] Sensitive data handling reviewed
- [ ] Input validation implemented
- [ ] Security scan passes

## Performance Impact

- [ ] No performance impact
- [ ] Performance impact measured and documented
- [ ] Optimization opportunities identified

## Checklist

- [ ] My code follows the project's style guidelines
- [ ] I have performed a self-review of my own code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes
- [ ] Any dependent changes have been merged and published

## Additional Notes

Any additional information, context, or considerations for reviewers.
