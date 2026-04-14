"""Tests for Feature 002 — Artifact Model."""

import pytest
from pathlib import Path

from src.scanner.repo_scanner import DiscoveredArtifact
from src.model.artifact_model import (
    ProjectArtifact,
    normalize_artifact,
    normalize_artifacts,
    extract_relationships,
    calculate_state_summary,
)


class TestProjectArtifactDataclass:
    """AC1: Define ProjectArtifact dataclass with stable fields"""
    
    def test_dataclass_has_required_fields(self):
        artifact = ProjectArtifact(
            artifact_type="exec-pack",
            artifact_id="exec-001",
            title="Test",
            summary="Test summary",
            source_path=Path("/test"),
            parse_status="success",
        )
        
        assert artifact.artifact_type == "exec-pack"
        assert artifact.artifact_id == "exec-001"
        assert artifact.relationships == []
        assert artifact.metadata == {}

    def test_dataclass_accepts_metadata(self):
        artifact = ProjectArtifact(
            artifact_type="exec-pack",
            artifact_id="exec-001",
            title="Test",
            summary="",
            source_path=Path("/test"),
            parse_status="success",
            metadata={"key": "value"},
        )
        
        assert artifact.metadata == {"key": "value"}


class TestNormalizeFeatureSpec:
    """AC2: Normalize feature spec → ProjectArtifact"""
    
    def test_normalize_feature_spec(self):
        discovered = DiscoveredArtifact(
            artifact_type="feature-spec",
            artifact_id="001-test",
            file_path=Path("/test/feature-spec.yaml"),
            parse_status="success",
            title="Test Feature",
            summary="A test feature",
            metadata={"feature_id": "001-test"},
        )
        
        normalized = normalize_artifact(discovered)
        
        assert normalized.artifact_type == "feature-spec"
        assert normalized.artifact_id == "001-test"
        assert normalized.title == "Test Feature"


class TestNormalizeExecPack:
    """AC3: Normalize exec pack → ProjectArtifact"""
    
    def test_normalize_exec_pack(self):
        discovered = DiscoveredArtifact(
            artifact_type="exec-pack",
            artifact_id="exec-20260414-001",
            file_path=Path("/test/exec-pack.md"),
            parse_status="success",
            title="",
            summary="Execute test task",
            date="2026-04-14",
            feature_id="001-test",
            metadata={"execution_id": "exec-20260414-001", "feature_id": "001-test"},
        )
        
        normalized = normalize_artifact(discovered)
        
        assert normalized.artifact_type == "exec-pack"
        assert normalized.date == "2026-04-14"
        assert normalized.feature_id == "001-test"
        assert "exec-result:exec-20260414-001" in normalized.relationships
        assert "feature:001-test" in normalized.relationships


class TestNormalizeExecResult:
    """AC4: Normalize exec result → ProjectArtifact"""
    
    def test_normalize_exec_result(self):
        discovered = DiscoveredArtifact(
            artifact_type="exec-result",
            artifact_id="exec-20260414-001",
            file_path=Path("/test/exec-result.md"),
            parse_status="success",
            status="success",
            feature_id="001-test",
            metadata={"execution_id": "exec-20260414-001", "status": "success"},
        )
        
        normalized = normalize_artifact(discovered)
        
        assert normalized.status == "success"
        assert "exec-pack:exec-20260414-001" in normalized.relationships


class TestNormalizeReview:
    """AC5: Normalize review → ProjectArtifact"""
    
    def test_normalize_review(self):
        discovered = DiscoveredArtifact(
            artifact_type="review",
            artifact_id="review-2026-04-14",
            file_path=Path("/test/review.md"),
            parse_status="success",
            date="2026-04-14",
            summary="Today's goal achieved",
            feature_id="001-test",
            metadata={"date": "2026-04-14", "feature_id": "001-test"},
        )
        
        normalized = normalize_artifact(discovered)
        
        assert normalized.date == "2026-04-14"
        assert "feature:001-test" in normalized.relationships


class TestNormalizeRunstate:
    """AC6: Normalize runstate → ProjectArtifact"""
    
    def test_normalize_runstate(self):
        discovered = DiscoveredArtifact(
            artifact_type="runstate",
            artifact_id="runstate",
            file_path=Path("/test/runstate.md"),
            parse_status="success",
            status="executing",
            metadata={"current_phase": "executing"},
        )
        
        normalized = normalize_artifact(discovered)
        
        assert normalized.status == "executing"


class TestExtractRelationships:
    """AC7: Extract relationships (feature ↔ exec-pack ↔ exec-result)"""
    
    def test_exec_pack_to_exec_result_link(self):
        discovered = DiscoveredArtifact(
            artifact_type="exec-pack",
            artifact_id="exec-001",
            file_path=Path("/test"),
            parse_status="success",
            metadata={"execution_id": "exec-001"},
        )
        
        relationships = extract_relationships(discovered)
        
        assert "exec-result:exec-001" in relationships
    
    def test_exec_pack_to_feature_link(self):
        discovered = DiscoveredArtifact(
            artifact_type="exec-pack",
            artifact_id="exec-001",
            file_path=Path("/test"),
            parse_status="success",
            feature_id="001-test",
            metadata={"feature_id": "001-test"},
        )
        
        relationships = extract_relationships(discovered)
        
        assert "feature:001-test" in relationships
    
    def test_exec_result_to_exec_pack_link(self):
        discovered = DiscoveredArtifact(
            artifact_type="exec-result",
            artifact_id="exec-001",
            file_path=Path("/test"),
            parse_status="success",
            metadata={},
        )
        
        relationships = extract_relationships(discovered)
        
        assert "exec-pack:exec-001" in relationships


class TestCalculateStateSummary:
    """AC8: Calculate minimal state summary"""
    
    def test_counts_active_states(self):
        artifacts = [
            ProjectArtifact(artifact_type="runstate", artifact_id="r1", title="", summary="", source_path=Path("/t"), parse_status="success", status="executing"),
            ProjectArtifact(artifact_type="runstate", artifact_id="r2", title="", summary="", source_path=Path("/t"), parse_status="success", status="planning"),
        ]
        
        summary = calculate_state_summary(artifacts)
        
        assert summary["active"] == 2
        assert summary["completed"] == 0
        assert summary["blocked"] == 0
    
    def test_counts_completed_states(self):
        artifacts = [
            ProjectArtifact(artifact_type="exec-result", artifact_id="r1", title="", summary="", source_path=Path("/t"), parse_status="success", status="success"),
            ProjectArtifact(artifact_type="exec-result", artifact_id="r2", title="", summary="", source_path=Path("/t"), parse_status="success", status="completed"),
        ]
        
        summary = calculate_state_summary(artifacts)
        
        assert summary["completed"] == 2
    
    def test_counts_blocked_states(self):
        artifacts = [
            ProjectArtifact(artifact_type="runstate", artifact_id="r1", title="", summary="", source_path=Path("/t"), parse_status="success", status="blocked"),
        ]
        
        summary = calculate_state_summary(artifacts)
        
        assert summary["blocked"] == 1
    
    def test_empty_artifacts_returns_zeros(self):
        summary = calculate_state_summary([])
        
        assert summary["active"] == 0
        assert summary["completed"] == 0
        assert summary["blocked"] == 0


class TestNormalizeArtifacts:
    def test_normalize_list(self):
        discovered_list = [
            DiscoveredArtifact(artifact_type="exec-pack", artifact_id="e1", file_path=Path("/t"), parse_status="success", metadata={}),
            DiscoveredArtifact(artifact_type="exec-result", artifact_id="e2", file_path=Path("/t"), parse_status="success", metadata={}),
        ]
        
        normalized = normalize_artifacts(discovered_list)
        
        assert len(normalized) == 2
        assert all(isinstance(a, ProjectArtifact) for a in normalized)