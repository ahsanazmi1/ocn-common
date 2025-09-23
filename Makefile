.PHONY: help setup lint fmt test run clean install-hooks

# Default target
help:
	@echo "Available targets:"
	@echo "  setup      - Create venv, install deps + dev extras, install pre-commit hooks"
	@echo "  lint       - Run ruff and black checks"
	@echo "  fmt        - Format code with black"
	@echo "  test       - Run pytest with coverage"
	@echo "  run        - Run demo or show usage examples (if available)"
	@echo "  clean      - Remove virtual environment and cache files"
	@echo "  install-hooks - Install pre-commit hooks"

# Setup development environment
setup:
	@echo "🔧 Setting up OCN Common development environment..."
	@python -m venv .venv
	@. .venv/bin/activate && pip install -U pip
	@. .venv/bin/activate && pip install -e '.[dev]'
	@. .venv/bin/activate && pre-commit install
	@echo "✅ Setup complete! Activate with: source .venv/bin/activate"

# Install pre-commit hooks
install-hooks:
	@echo "🔗 Installing pre-commit hooks..."
	@. .venv/bin/activate && pre-commit install
	@echo "✅ Pre-commit hooks installed!"

# Lint code
lint:
	@echo "🔍 Running linting checks..."
	@. .venv/bin/activate && ruff check .
	@. .venv/bin/activate && black --check .
	@echo "✅ Linting passed!"

# Format code
fmt:
	@echo "🎨 Formatting code..."
	@. .venv/bin/activate && black .
	@echo "✅ Code formatted!"

# Run tests with coverage
test:
	@echo "🧪 Running tests with coverage..."
	@. .venv/bin/activate && pip install pytest-cov
	@. .venv/bin/activate && pytest -q --cov=src --cov-report=term-missing --cov-fail-under=80
	@echo "✅ Tests passed!"

# Run demo or show usage (OCN Common is a library)
run:
	@echo "📚 OCN Common is a shared library for the Open Checkout Network"
	@echo ""
	@echo "Available demos and examples:"
	@if [ -f "examples/streamlit_demo.py" ]; then \
		echo "  📊 Streamlit demo: examples/streamlit_demo.py"; \
		echo "    Run with: streamlit run examples/streamlit_demo.py"; \
	fi
	@echo ""
	@echo "📖 Usage examples:"
	@echo "  # Import OCN Common utilities"
	@echo "  from ocn_common.contracts import validate_event, get_schema"
	@echo "  from ocn_common.trace import ensure_trace_id, trace_middleware"
	@echo ""
	@echo "  # Validate an event against OCN schemas"
	@echo "  is_valid = validate_event(event_data, schema_version=\"v1\")"
	@echo ""
	@echo "  # Ensure trace context across OCN services"
	@echo "  trace_id = ensure_trace_id()"
	@echo ""
	@echo "📁 Available schemas:"
	@if [ -d "common/events" ]; then \
		echo "  📋 Event schemas: common/events/v1/"; \
		find common/events/v1/ -name "*.json" 2>/dev/null | head -3 | sed 's/^/    /'; \
	fi
	@if [ -d "common/mandates" ]; then \
		echo "  📋 Mandate schemas: common/mandates/"; \
		find common/mandates/ -name "*.json" 2>/dev/null | head -3 | sed 's/^/    /'; \
	fi

# Clean up
clean:
	@echo "🧹 Cleaning up..."
	@rm -rf .venv
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@find . -type f -name "*.pyo" -delete 2>/dev/null || true
	@find . -type f -name ".coverage" -delete 2>/dev/null || true
	@find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	@echo "✅ Cleanup complete!"

# Quick development workflow
dev: fmt lint test
	@echo "✅ Development checks complete!"

# CI workflow (used by GitHub Actions)
ci: lint test
	@echo "✅ CI checks complete!"

# Validate schemas
validate-schemas:
	@echo "🔍 Validating JSON schemas..."
	@. .venv/bin/activate && find common/ -name "*.json" -print0 | while IFS= read -r -d $$'\0' file; do \
		python -m json.tool "$$file" > /dev/null || { echo "❌ Invalid JSON in $$file"; exit 1; }; \
		echo "✅ Valid JSON: $$file"; \
	done
	@echo "✅ Schema validation completed!"

# Run contract tests
test-contracts:
	@echo "🧪 Running contract validation tests..."
	@. .venv/bin/activate && python -m pytest tests/test_contracts.py -v
	@echo "✅ Contract tests completed!"
