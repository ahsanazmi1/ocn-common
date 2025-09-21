"""
Tests for trace utility functionality.
"""

import uuid
from unittest.mock import MagicMock, patch

from ocn_common.trace import (
    TRACE_HEADER,
    clear_current_trace_id,
    create_trace_context,
    ensure_trace_id,
    format_trace_log,
    get_current_trace_id,
    inject_trace_id_ce,
    new_trace_id,
    set_current_trace_id,
    trace_middleware,
)


class TestTraceIDGeneration:
    """Test trace ID generation functionality."""

    def test_new_trace_id_format(self):
        """Test that new_trace_id returns a valid UUID4 format."""
        trace_id = new_trace_id()

        # Should be a valid UUID4 string
        assert isinstance(trace_id, str)
        assert len(trace_id) == 36  # UUID4 format
        assert trace_id.count("-") == 4  # UUID4 has 4 hyphens

        # Should be parseable as UUID
        parsed_uuid = uuid.UUID(trace_id)
        assert parsed_uuid.version == 4  # UUID4

    def test_new_trace_id_uniqueness(self):
        """Test that new_trace_id generates unique IDs."""
        trace_ids = [new_trace_id() for _ in range(100)]

        # All should be unique
        assert len(set(trace_ids)) == 100

    def test_trace_id_format_consistency(self):
        """Test that trace IDs have consistent format."""
        for _ in range(10):
            trace_id = new_trace_id()
            # Should match UUID4 pattern
            assert len(trace_id) == 36
            assert trace_id[8] == "-"
            assert trace_id[13] == "-"
            assert trace_id[18] == "-"
            assert trace_id[23] == "-"


class TestEnsureTraceID:
    """Test ensure_trace_id functionality."""

    def test_ensure_trace_id_new_context(self):
        """Test ensure_trace_id with new context."""
        ctx = {"user_id": "123"}
        trace_id = ensure_trace_id(ctx)

        # Should generate new trace ID
        assert isinstance(trace_id, str)
        assert len(trace_id) == 36
        assert ctx["trace_id"] == trace_id

    def test_ensure_trace_id_existing_trace_id(self):
        """Test ensure_trace_id with existing trace ID."""
        existing_trace = "550e8400-e29b-41d4-a716-446655440000"  # Valid UUID4
        ctx = {"trace_id": existing_trace, "user_id": "123"}
        trace_id = ensure_trace_id(ctx)

        # Should return existing trace ID
        assert trace_id == existing_trace
        assert ctx["trace_id"] == existing_trace

    def test_ensure_trace_id_empty_trace_id(self):
        """Test ensure_trace_id with empty trace ID."""
        ctx = {"trace_id": "", "user_id": "123"}
        trace_id = ensure_trace_id(ctx)

        # Should generate new trace ID
        assert isinstance(trace_id, str)
        assert len(trace_id) == 36
        assert ctx["trace_id"] == trace_id

    def test_ensure_trace_id_none_context(self):
        """Test ensure_trace_id with None context."""
        trace_id = ensure_trace_id(None)

        # Should generate new trace ID
        assert isinstance(trace_id, str)
        assert len(trace_id) == 36

    def test_ensure_trace_id_none_trace_id(self):
        """Test ensure_trace_id with None trace ID."""
        ctx = {"trace_id": None, "user_id": "123"}
        trace_id = ensure_trace_id(ctx)

        # Should generate new trace ID
        assert isinstance(trace_id, str)
        assert len(trace_id) == 36
        assert ctx["trace_id"] == trace_id


class TestInjectTraceIDCE:
    """Test CloudEvent trace ID injection functionality."""

    def test_inject_trace_id_ce_basic(self):
        """Test basic trace ID injection into CloudEvent."""
        envelope = {
            "specversion": "1.0",
            "id": "event-123",
            "source": "https://example.com",
            "type": "ocn.orca.decision.v1",
        }
        trace_id = "trace-456"

        result = inject_trace_id_ce(envelope, trace_id)

        # Should add subject field
        assert result["subject"] == trace_id
        # Should preserve other fields
        assert result["id"] == "event-123"
        assert result["specversion"] == "1.0"
        assert result["source"] == "https://example.com"
        assert result["type"] == "ocn.orca.decision.v1"

    def test_inject_trace_id_ce_existing_subject(self):
        """Test trace ID injection overwrites existing subject."""
        envelope = {
            "specversion": "1.0",
            "id": "event-123",
            "subject": "old-subject",
            "type": "ocn.orca.decision.v1",
        }
        trace_id = "trace-456"

        result = inject_trace_id_ce(envelope, trace_id)

        # Should overwrite existing subject
        assert result["subject"] == trace_id
        assert result["subject"] != "old-subject"

    def test_inject_trace_id_ce_preserves_original(self):
        """Test that original envelope is not modified."""
        envelope = {"specversion": "1.0", "id": "event-123", "type": "ocn.orca.decision.v1"}
        original_envelope = envelope.copy()
        trace_id = "trace-456"

        result = inject_trace_id_ce(envelope, trace_id)

        # Original should be unchanged
        assert envelope == original_envelope
        assert envelope is not result  # Should be different objects

    def test_inject_trace_id_ce_complete_envelope(self):
        """Test trace ID injection with complete CloudEvent envelope."""
        envelope = {
            "specversion": "1.0",
            "id": "event-123",
            "source": "https://example.com",
            "type": "ocn.orca.decision.v1",
            "time": "2024-01-01T12:00:00Z",
            "datacontenttype": "application/json",
            "data": {"decision": "APPROVE"},
        }
        trace_id = "trace-456"

        result = inject_trace_id_ce(envelope, trace_id)

        # Should add subject
        assert result["subject"] == trace_id
        # Should preserve all other fields
        assert result["specversion"] == envelope["specversion"]
        assert result["id"] == envelope["id"]
        assert result["source"] == envelope["source"]
        assert result["type"] == envelope["type"]
        assert result["time"] == envelope["time"]
        assert result["datacontenttype"] == envelope["datacontenttype"]
        assert result["data"] == envelope["data"]


class TestContextManagement:
    """Test trace context variable management."""

    def test_get_current_trace_id_initial(self):
        """Test get_current_trace_id when no trace ID is set."""
        # Clear any existing trace ID
        clear_current_trace_id()

        trace_id = get_current_trace_id()
        assert trace_id is None

    def test_set_get_current_trace_id(self):
        """Test setting and getting current trace ID."""
        test_trace_id = "test-trace-123"

        set_current_trace_id(test_trace_id)
        trace_id = get_current_trace_id()

        assert trace_id == test_trace_id

    def test_clear_current_trace_id(self):
        """Test clearing current trace ID."""
        test_trace_id = "test-trace-123"

        set_current_trace_id(test_trace_id)
        assert get_current_trace_id() == test_trace_id

        clear_current_trace_id()
        assert get_current_trace_id() is None

    def test_context_isolation(self):
        """Test that context variables are properly isolated."""
        # Set trace ID in one context
        set_current_trace_id("trace-1")
        assert get_current_trace_id() == "trace-1"

        # In a real async context, this would be isolated
        # For testing, we simulate by clearing and setting again
        clear_current_trace_id()
        set_current_trace_id("trace-2")
        assert get_current_trace_id() == "trace-2"


class TestTraceMiddleware:
    """Test FastAPI middleware functionality."""

    def test_trace_middleware_adds_middleware(self):
        """Test that trace_middleware adds middleware to FastAPI app."""
        # Mock FastAPI app
        mock_app = MagicMock()
        mock_app.user_middleware = []

        # Add trace middleware
        result = trace_middleware(mock_app)

        # Should have added one middleware
        assert mock_app.add_middleware.call_count == 1
        assert result is mock_app

    def test_trace_middleware_returns_app(self):
        """Test that trace_middleware returns the app for chaining."""
        # Mock FastAPI app
        mock_app = MagicMock()
        mock_app.user_middleware = []

        result = trace_middleware(mock_app)

        # Should return the same app instance
        assert result is mock_app


class TestTraceContextCreation:
    """Test trace context creation functionality."""

    def test_create_trace_context_no_trace_id(self):
        """Test create_trace_context without providing trace ID."""
        ctx = create_trace_context()

        assert "trace_id" in ctx
        assert isinstance(ctx["trace_id"], str)
        assert len(ctx["trace_id"]) == 36  # UUID4 format
        assert ctx["service"] == "ocn-common"
        assert ctx["version"] == "1.0.0"

    def test_create_trace_context_with_trace_id(self):
        """Test create_trace_context with provided trace ID."""
        custom_trace_id = "custom-trace-123"
        ctx = create_trace_context(custom_trace_id)

        assert ctx["trace_id"] == custom_trace_id
        assert ctx["service"] == "ocn-common"
        assert ctx["version"] == "1.0.0"

    def test_create_trace_context_structure(self):
        """Test create_trace_context returns proper structure."""
        ctx = create_trace_context()

        # Should have all required fields
        required_fields = ["trace_id", "service", "version"]
        for field in required_fields:
            assert field in ctx
            assert isinstance(ctx[field], str)
            assert len(ctx[field]) > 0


class TestTraceLogFormatting:
    """Test trace log formatting functionality."""

    def test_format_trace_log_basic(self):
        """Test basic trace log formatting."""
        trace_id = "trace-123"
        message = "Processing request"

        log = format_trace_log(trace_id, message)

        assert f"[trace_id={trace_id}]" in log
        assert message in log

    def test_format_trace_log_with_context(self):
        """Test trace log formatting with additional context."""
        trace_id = "trace-123"
        message = "Processing request"
        context = {"user_id": "456", "action": "login"}

        log = format_trace_log(trace_id, message, **context)

        assert f"[trace_id={trace_id}]" in log
        assert message in log
        assert "user_id=456" in log
        assert "action=login" in log

    def test_format_trace_log_empty_context(self):
        """Test trace log formatting with empty context."""
        trace_id = "trace-123"
        message = "Simple message"

        log = format_trace_log(trace_id, message)

        assert f"[trace_id={trace_id}]" in log
        assert message in log
        # Should not have extra spaces or context
        assert log == f"[trace_id={trace_id}] {message}"

    def test_format_trace_log_multiple_context(self):
        """Test trace log formatting with multiple context items."""
        trace_id = "trace-123"
        message = "Complex operation"
        context = {
            "user_id": "456",
            "session_id": "sess-789",
            "duration_ms": 150,
            "status": "success",
        }

        log = format_trace_log(trace_id, message, **context)

        assert f"[trace_id={trace_id}]" in log
        assert message in log
        # All context items should be present
        for key, value in context.items():
            assert f"{key}={value}" in log


class TestIntegration:
    """Integration tests for trace utilities."""

    def test_full_trace_workflow(self):
        """Test complete trace workflow from generation to CloudEvent injection."""
        # Generate new trace ID
        trace_id = new_trace_id()
        assert isinstance(trace_id, str)
        assert len(trace_id) == 36

        # Ensure trace ID in context
        ctx = {"user_id": "123"}
        ensured_trace_id = ensure_trace_id(ctx)
        assert ensured_trace_id == ctx["trace_id"]

        # Set in context variable
        set_current_trace_id(trace_id)
        assert get_current_trace_id() == trace_id

        # Create CloudEvent envelope
        envelope = {"specversion": "1.0", "id": "event-123", "type": "ocn.orca.decision.v1"}

        # Inject trace ID
        modified_envelope = inject_trace_id_ce(envelope, trace_id)
        assert modified_envelope["subject"] == trace_id

        # Format log message
        log = format_trace_log(trace_id, "Request processed", user_id="123")
        assert f"[trace_id={trace_id}]" in log
        assert "user_id=123" in log

        # Clean up
        clear_current_trace_id()
        assert get_current_trace_id() is None

    def test_trace_header_constant(self):
        """Test that TRACE_HEADER constant is properly defined."""
        assert TRACE_HEADER == "x-ocn-trace-id"
        assert isinstance(TRACE_HEADER, str)
        assert len(TRACE_HEADER) > 0


class TestEdgeCases:
    """Test edge cases and error conditions."""

    def test_ensure_trace_id_malformed_trace_id(self):
        """Test ensure_trace_id with malformed existing trace ID."""
        # Test with various malformed trace IDs
        malformed_ids = ["", " ", "invalid-uuid", "too-short", "x" * 100]

        for malformed_id in malformed_ids:
            ctx = {"trace_id": malformed_id}
            trace_id = ensure_trace_id(ctx)

            # Should generate a new valid trace ID
            assert isinstance(trace_id, str)
            assert len(trace_id) == 36
            assert ctx["trace_id"] == trace_id

    def test_inject_trace_id_ce_empty_envelope(self):
        """Test inject_trace_id_ce with empty envelope."""
        envelope = {}
        trace_id = "trace-123"

        result = inject_trace_id_ce(envelope, trace_id)

        assert result["subject"] == trace_id
        assert len(result) == 1  # Only subject field

    def test_format_trace_log_special_characters(self):
        """Test format_trace_log with special characters."""
        trace_id = "trace-123"
        message = "Message with special chars: !@#$%^&*()"
        context = {"key with spaces": "value with spaces", "unicode": "测试"}

        log = format_trace_log(trace_id, message, **context)

        assert f"[trace_id={trace_id}]" in log
        assert message in log
        assert "key with spaces=value with spaces" in log
        assert "unicode=测试" in log
