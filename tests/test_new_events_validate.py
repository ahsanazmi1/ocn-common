"""
Tests for validating Phase 2 CloudEvents against their schemas.

This module tests the new Phase 2 event types:
- orion.explanation.v1
- okra.bnpl_quote.v1
- onyx.kyb_verified.v1
"""

import json
from pathlib import Path
from typing import Dict, Any

import pytest

from ocn_common.contracts import validate_cloudevent, ContractValidationError


class TestPhase2EventsValidation:
    """Test validation of Phase 2 CloudEvents."""

    def load_example_event(self, filename: str) -> Dict[str, Any]:
        """Load an example CloudEvent from the examples directory."""
        examples_dir = Path(__file__).parent.parent / "examples" / "events"
        with open(examples_dir / filename, "r") as f:
            return json.load(f)

    def test_orion_explanation_event_valid(self) -> None:
        """Test that valid Orion explanation events pass validation."""
        event = self.load_example_event("orion_explanation_example.json")

        # Validate against the schema
        assert validate_cloudevent(event, "ocn.orion.explanation.v1") is True

    def test_orion_explanation_event_invalid_type(self) -> None:
        """Test that Orion explanation events with invalid type fail validation."""
        event = self.load_example_event("orion_explanation_example.json")
        event["type"] = "ocn.orion.explanation.v2"  # Invalid type

        with pytest.raises(ContractValidationError):
            validate_cloudevent(event, "ocn.orion.explanation.v1")

    def test_orion_explanation_event_missing_required_field(self) -> None:
        """Test that Orion explanation events missing required fields fail validation."""
        event = self.load_example_event("orion_explanation_example.json")
        del event["data"]["verification_result"]["best_rail"]  # Remove required field

        with pytest.raises(ContractValidationError):
            validate_cloudevent(event, "ocn.orion.explanation.v1")

    def test_okra_bnpl_quote_event_valid(self) -> None:
        """Test that valid Okra BNPL quote events pass validation."""
        event = self.load_example_event("okra_bnpl_quote_example.json")

        # Validate against the schema
        assert validate_cloudevent(event, "ocn.okra.bnpl_quote.v1") is True

    def test_okra_bnpl_quote_event_invalid_source(self) -> None:
        """Test that Okra BNPL quote events with invalid source fail validation."""
        event = self.load_example_event("okra_bnpl_quote_example.json")
        event["source"] = "invalid_source"  # Invalid source

        with pytest.raises(ContractValidationError):
            validate_cloudevent(event, "ocn.okra.bnpl_quote.v1")

    def test_okra_bnpl_quote_event_invalid_score_range(self) -> None:
        """Test that Okra BNPL quote events with invalid score range fail validation."""
        event = self.load_example_event("okra_bnpl_quote_example.json")
        event["data"]["quote_result"]["score"] = 1.5  # Invalid score > 1.0

        with pytest.raises(ContractValidationError):
            validate_cloudevent(event, "ocn.okra.bnpl_quote.v1")

    def test_onyx_kyb_verified_event_valid(self) -> None:
        """Test that valid Onyx KYB verified events pass validation."""
        event = self.load_example_event("onyx_kyb_verified_example.json")

        # Validate against the schema
        assert validate_cloudevent(event, "ocn.onyx.kyb_verified.v1") is True

    def test_onyx_kyb_verified_event_invalid_status(self) -> None:
        """Test that Onyx KYB verified events with invalid status fail validation."""
        event = self.load_example_event("onyx_kyb_verified_example.json")
        event["data"]["verification_result"]["status"] = "invalid_status"  # Invalid status

        with pytest.raises(ContractValidationError):
            validate_cloudevent(event, "ocn.onyx.kyb_verified.v1")

    def test_onyx_kyb_verified_event_invalid_check_status(self) -> None:
        """Test that Onyx KYB verified events with invalid check status fail validation."""
        event = self.load_example_event("onyx_kyb_verified_example.json")
        event["data"]["verification_result"]["checks"][0][
            "status"
        ] = "invalid_check_status"  # Invalid check status

        with pytest.raises(ContractValidationError):
            validate_cloudevent(event, "ocn.onyx.kyb_verified.v1")

    def test_all_phase2_event_types_registered(self) -> None:
        """Test that all Phase 2 event types are properly registered in contracts.py."""
        # Test that we can validate all Phase 2 event types
        phase2_types = [
            "ocn.orion.explanation.v1",
            "ocn.okra.bnpl_quote.v1",
            "ocn.onyx.kyb_verified.v1",
        ]

        for event_type in phase2_types:
            # Load corresponding example
            if "orion" in event_type:
                event = self.load_example_event("orion_explanation_example.json")
            elif "okra" in event_type:
                event = self.load_example_event("okra_bnpl_quote_example.json")
            elif "onyx" in event_type:
                event = self.load_example_event("onyx_kyb_verified_example.json")

            # Should validate successfully
            assert validate_cloudevent(event, event_type) is True

    def test_unknown_event_type_raises_error(self) -> None:
        """Test that unknown event types raise appropriate errors."""
        event = self.load_example_event("orion_explanation_example.json")

        with pytest.raises(ContractValidationError, match="Unknown CloudEvent type"):
            validate_cloudevent(event, "ocn.unknown.event.v1")

    def test_malformed_json_raises_error(self) -> None:
        """Test that malformed JSON raises appropriate errors."""
        malformed_json = '{"specversion": "1.0", "id": "test", "type": "ocn.orion.explanation.v1"'

        with pytest.raises(ContractValidationError, match="Invalid JSON payload"):
            validate_cloudevent(malformed_json, "ocn.orion.explanation.v1")

    def test_cloud_event_required_attributes(self) -> None:
        """Test that CloudEvents have all required attributes."""
        required_attrs = ["specversion", "id", "source", "type", "subject", "time", "data"]

        # Test each Phase 2 event type
        events = [
            ("orion_explanation_example.json", "ocn.orion.explanation.v1"),
            ("okra_bnpl_quote_example.json", "ocn.okra.bnpl_quote.v1"),
            ("onyx_kyb_verified_example.json", "ocn.onyx.kyb_verified.v1"),
        ]

        for filename, event_type in events:
            event = self.load_example_event(filename)

            # Check all required attributes are present
            for attr in required_attrs:
                assert attr in event, f"Missing required attribute '{attr}' in {event_type}"

            # Validate the complete event
            assert validate_cloudevent(event, event_type) is True

    def test_cloud_event_specversion_validation(self) -> None:
        """Test that CloudEvents specversion is properly validated."""
        event = self.load_example_event("orion_explanation_example.json")

        # Test valid specversion
        event["specversion"] = "1.0"
        assert validate_cloudevent(event, "ocn.orion.explanation.v1") is True

        # Test invalid specversion
        event["specversion"] = "2.0"
        with pytest.raises(ContractValidationError):
            validate_cloudevent(event, "ocn.orion.explanation.v1")

    def test_cloud_event_datacontenttype_validation(self) -> None:
        """Test that CloudEvents datacontenttype is properly validated."""
        event = self.load_example_event("okra_bnpl_quote_example.json")

        # Test valid datacontenttype
        event["datacontenttype"] = "application/json"
        assert validate_cloudevent(event, "ocn.okra.bnpl_quote.v1") is True

        # Test invalid datacontenttype
        event["datacontenttype"] = "application/xml"
        with pytest.raises(ContractValidationError):
            validate_cloudevent(event, "ocn.okra.bnpl_quote.v1")
