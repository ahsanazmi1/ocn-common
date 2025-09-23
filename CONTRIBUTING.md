# Contributing to OCN Common

Thank you for your interest in contributing to the Open Checkout Network (OCN) Common library! This document provides guidelines and information for contributors.

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

## Getting Started

### Prerequisites

- Python 3.12 or higher
- Git
- Basic understanding of the Open Checkout Network (OCN)

### Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/ocn-ai/ocn-common.git
   cd ocn-common
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -U pip
   pip install -e .[dev]
   ```

4. **Install pre-commit hooks** (if available)
   ```bash
   pre-commit install
   ```

5. **Run tests**
   ```bash
   pytest -q
   ```

## Contribution Guidelines

### Branch Strategy

- **`main`** - Production-ready code
- **`phase-1-foundations`** - Development branch for foundational features
- **Feature branches** - Create from `phase-1-foundations` for new features

### Commit Messages

Follow conventional commit format:
- `feat:` - New features
- `fix:` - Bug fixes
- `docs:` - Documentation changes
- `style:` - Code style changes
- `refactor:` - Code refactoring
- `test:` - Test additions or changes
- `chore:` - Maintenance tasks

### Code Style

- Follow PEP 8
- Use `black` for code formatting
- Use `ruff` for linting
- Type hints are encouraged where appropriate

### Testing

- Write tests for new functionality
- Ensure all tests pass: `pytest -q`
- Maintain test coverage
- Include integration tests for schema validation

### Schema Development

When adding or modifying event schemas:

1. **Location**: Place schemas in `common/events/v1/` or appropriate subdirectory
2. **Naming**: Use descriptive names following the pattern `agent.event.v1.schema.json`
3. **Validation**: Ensure schemas are valid JSON Schema
4. **Examples**: Add example events in `examples/events/`
5. **Documentation**: Update relevant documentation

### Documentation

- Update README.md for significant changes
- Document new APIs and utilities
- Include examples for new features
- Update CHANGELOG.md for releases

## Pull Request Process

1. **Create a feature branch** from `phase-1-foundations`
2. **Make your changes** following the guidelines above
3. **Write tests** for your changes
4. **Run the test suite** and ensure it passes
5. **Update documentation** as needed
6. **Submit a pull request** to `phase-1-foundations`

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] New tests added for new functionality
- [ ] Schema validation tests pass

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] CHANGELOG.md updated (if applicable)
```

## Issue Reporting

When reporting issues:

1. **Check existing issues** first
2. **Use the issue template** provided
3. **Include reproduction steps** for bugs
4. **Provide environment details** (Python version, OS, etc.)
5. **Include relevant logs** or error messages

## Release Process

Releases are managed by the maintainers:

1. **Version bump** in `pyproject.toml`
2. **Update CHANGELOG.md** with release notes
3. **Create git tag** for the release
4. **Publish to PyPI** (if applicable)

## Questions?

- **GitHub Issues** - For bugs and feature requests
- **GitHub Discussions** - For questions and general discussion
- **OCN Documentation** - For architecture and design questions

## License

By contributing to OCN Common, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to the Open Checkout Network! 🚀
