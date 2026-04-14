"""Tests for Feature 004 - Project Grouping.

TDD approach: Tests define behavior before implementation.
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch

from src.scanner.repo_scanner import (
    DiscoveredArtifact,
    scan_repo,
    scan_project,
    detect_project_structure,
)
from src.model.artifact_model import (
    ProjectArtifact,
    normalize_artifact,
    group_artifacts_by_project,
    get_project_summary,
)
from src.api.observatory_api import app


# ============================================================================
# AC1: Group artifacts by project_id
# ============================================================================

class TestArtifactHasProjectId:
    """AC1: Each artifact must have project_id field."""
    
    def test_discovered_artifact_has_project_id_field(self):
        """DiscoveredArtifact should have project_id field."""
        artifact = DiscoveredArtifact(
            artifact_type="exec-pack",
            artifact_id="exec-001",
            file_path=Path("test.md"),
            parse_status="success",
            project_id="demo-product",
        )
        assert artifact.project_id == "demo-product"
    
    def test_project_artifact_has_project_id_field(self):
        """ProjectArtifact should preserve project_id."""
        discovered = DiscoveredArtifact(
            artifact_type="exec-pack",
            artifact_id="exec-001",
            file_path=Path("test.md"),
            parse_status="success",
            project_id="demo-product",
        )
        normalized = normalize_artifact(discovered)
        assert normalized.project_id == "demo-product"


class TestScannerTracksProjectId:
    """Scanner must track project_id for each artifact."""
    
    def test_scan_project_returns_artifacts_with_project_id(self, tmp_path):
        """scan_project should populate project_id field."""
        # Create minimal project structure
        project_dir = tmp_path / "projects" / "test-project"
        project_dir.mkdir(parents=True)
        
        features_dir = project_dir / "features"
        features_dir.mkdir()
        feature_spec = features_dir / "001-test-feature" / "feature-spec.yaml"
        feature_spec.parent.mkdir()
        feature_spec.write_text("name: test-feature\ngoal: test\n")
        
        artifacts = scan_project(project_dir)
        
        assert len(artifacts) > 0
        for artifact in artifacts:
            assert artifact.project_id == "test-project"
    
    def test_scan_repo_returns_artifacts_with_project_id(self, tmp_path):
        """scan_repo should populate project_id from project path."""
        # Create multi-project structure
        projects_dir = tmp_path / "projects"
        projects_dir.mkdir()
        
        # Project A
        project_a = projects_dir / "project-a"
        project_a.mkdir()
        features_a = project_a / "features"
        features_a.mkdir()
        feature_a = features_a / "001-feature" / "feature-spec.yaml"
        feature_a.parent.mkdir()
        feature_a.write_text("name: feature-a\n")
        
        # Project B
        project_b = projects_dir / "project-b"
        project_b.mkdir()
        runstate_b = project_b / "runstate.md"
        runstate_b.write_text("```yaml\nproduct_id: project-b\n```\n")
        
        artifacts = scan_repo(tmp_path)
        
        # Artifacts should have correct project_id
        project_ids = [a.project_id for a in artifacts]
        assert "project-a" in project_ids
        assert "project-b" in project_ids


class TestGroupArtifactsByProject:
    """group_artifacts_by_project function behavior."""
    
    def test_group_by_project_id(self):
        """Should group artifacts by project_id."""
        artifacts = [
            ProjectArtifact(
                artifact_type="exec-pack",
                artifact_id="exec-001",
                title="Pack 1",
                summary="Test",
                source_path=Path("a.md"),
                parse_status="success",
                project_id="project-a",
            ),
            ProjectArtifact(
                artifact_type="exec-pack",
                artifact_id="exec-002",
                title="Pack 2",
                summary="Test",
                source_path=Path("b.md"),
                parse_status="success",
                project_id="project-b",
            ),
            ProjectArtifact(
                artifact_type="exec-result",
                artifact_id="exec-001",
                title="Result 1",
                summary="Test",
                source_path=Path("c.md"),
                parse_status="success",
                project_id="project-a",
            ),
        ]
        
        grouped = group_artifacts_by_project(artifacts)
        
        assert "project-a" in grouped
        assert "project-b" in grouped
        assert len(grouped["project-a"]) == 2
        assert len(grouped["project-b"]) == 1
    
    def test_empty_artifacts_returns_empty_dict(self):
        """Empty list should return empty dict."""
        grouped = group_artifacts_by_project([])
        assert grouped == {}


# ============================================================================
# AC2: Provide project list for navigation
# ============================================================================

class TestGetProjectSummary:
    """get_project_summary returns project list with counts."""
    
    def test_get_project_summary(self):
        """Should return list of projects with artifact counts."""
        artifacts = [
            ProjectArtifact(
                artifact_type="exec-pack",
                artifact_id="exec-001",
                title="Pack 1",
                summary="Test",
                source_path=Path("a.md"),
                parse_status="success",
                project_id="project-a",
            ),
            ProjectArtifact(
                artifact_type="exec-pack",
                artifact_id="exec-002",
                title="Pack 2",
                summary="Test",
                source_path=Path("b.md"),
                parse_status="success",
                project_id="project-b",
            ),
            ProjectArtifact(
                artifact_type="exec-result",
                artifact_id="exec-001",
                title="Result 1",
                summary="Test",
                source_path=Path("c.md"),
                parse_status="success",
                project_id="project-a",
            ),
        ]
        
        summary = get_project_summary(artifacts)
        
        assert len(summary) == 2
        project_a = next(p for p in summary if p["project_id"] == "project-a")
        project_b = next(p for p in summary if p["project_id"] == "project-b")
        
        assert project_a["count"] == 2
        assert project_b["count"] == 1
    
    def test_empty_artifacts_returns_empty_list(self):
        """Empty list should return empty summary."""
        summary = get_project_summary([])
        assert summary == []


class TestProjectsEndpoint:
    """API endpoint for project list."""
    
    def test_api_projects_endpoint_exists(self, tmp_path):
        """GET /api/projects should return project list."""
        # Setup test repo structure
        projects_dir = tmp_path / "projects"
        projects_dir.mkdir()
        
        project_a = projects_dir / "project-a"
        project_a.mkdir()
        runstate_a = project_a / "runstate.md"
        runstate_a.write_text("```yaml\nproduct_id: project-a\n```\n")
        
        from fastapi.testclient import TestClient
        client = TestClient(app)
        
        response = client.get(f"/api/projects?repo_path={tmp_path}")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert any(p["project_id"] == "project-a" for p in data)


# ============================================================================
# AC3: Filter artifacts by selected project
# ============================================================================

class TestProjectFiltering:
    """API should support project filtering."""
    
    def test_get_project_state_with_project_filter(self, tmp_path):
        """GET /api/project/{project_id} should filter by project."""
        # Setup multi-project repo
        projects_dir = tmp_path / "projects"
        projects_dir.mkdir()
        
        project_a = projects_dir / "project-a"
        project_a.mkdir()
        features_a = project_a / "features"
        features_a.mkdir()
        feature_a = features_a / "001-feature" / "feature-spec.yaml"
        feature_a.parent.mkdir()
        feature_a.write_text("name: feature-a\nfeature_id: 001\n")
        
        project_b = projects_dir / "project-b"
        project_b.mkdir()
        features_b = project_b / "features"
        features_b.mkdir()
        feature_b = features_b / "002-feature" / "feature-spec.yaml"
        feature_b.parent.mkdir()
        feature_b.write_text("name: feature-b\nfeature_id: 002\n")
        
        from fastapi.testclient import TestClient
        client = TestClient(app)
        
        response_a = client.get(f"/api/project/project-a?repo_path={tmp_path}")
        response_b = client.get(f"/api/project/project-b?repo_path={tmp_path}")
        
        assert response_a.status_code == 200
        data_a = response_a.json()
        assert data_a["project_id"] == "project-a"
        
        assert response_b.status_code == 200
        data_b = response_b.json()
        assert data_b["project_id"] == "project-b"


# ============================================================================
# AC4: Show project count in observatory header
# ============================================================================

class TestProjectCountInHeader:
    """Observatory should show project count."""
    
    def test_api_returns_project_count(self, tmp_path):
        """API should return total project count."""
        projects_dir = tmp_path / "projects"
        projects_dir.mkdir()
        
        for i in range(3):
            project = projects_dir / f"project-{i}"
            project.mkdir()
            runstate = project / "runstate.md"
            runstate.write_text(f"```yaml\nproduct_id: project-{i}\n```\n")
        
        from fastapi.testclient import TestClient
        client = TestClient(app)
        
        response = client.get(f"/api/projects?repo_path={tmp_path}")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
    
    def test_observatory_html_has_project_count_element(self):
        """HTML should have element for project count."""
        from src.api.observatory_api import get_observatory_html
        html = get_observatory_html()
        
        # Should have project count display element
        assert "project-count" in html or "Projects" in html


# ============================================================================
# AC5: Project selection UI
# ============================================================================

class TestProjectSelectorUI:
    """Observatory should have project selector UI."""
    
    def test_observatory_html_has_project_selector(self):
        """HTML should include project selector element."""
        from src.api.observatory_api import get_observatory_html
        html = get_observatory_html()
        
        # Should have project selector (dropdown or buttons)
        assert "project-selector" in html or "project-select" in html
    
    def test_observatory_html_loads_project_list(self):
        """JavaScript should fetch project list."""
        from src.api.observatory_api import get_observatory_html
        html = get_observatory_html()
        
        # Should have JS to load projects
        assert "/api/projects" in html


# ============================================================================
# Integration tests
# ============================================================================

class TestProjectGroupingIntegration:
    """Full integration test for project grouping."""
    
    def test_full_workflow(self, tmp_path):
        """Complete workflow: detect projects, group artifacts, filter."""
        # Create multi-project repo
        projects_dir = tmp_path / "projects"
        projects_dir.mkdir()
        
        # Project alpha
        alpha = projects_dir / "alpha"
        alpha.mkdir()
        features_alpha = alpha / "features"
        features_alpha.mkdir()
        spec_alpha = features_alpha / "001-init" / "feature-spec.yaml"
        spec_alpha.parent.mkdir()
        spec_alpha.write_text("name: init\nfeature_id: 001\n")
        
        exec_packs_alpha = alpha / "execution-packs"
        exec_packs_alpha.mkdir()
        pack_alpha = exec_packs_alpha / "exec-20260101-001.md"
        pack_alpha.write_text("```yaml\ndate: 2026-01-01\nfeature_id: 001\n```\n")
        
        # Project beta
        beta = projects_dir / "beta"
        beta.mkdir()
        features_beta = beta / "features"
        features_beta.mkdir()
        spec_beta = features_beta / "002-main" / "feature-spec.yaml"
        spec_beta.parent.mkdir()
        spec_beta.write_text("name: main\nfeature_id: 002\n")
        
        # Scan
        artifacts = scan_repo(tmp_path)
        
        # Group
        grouped = group_artifacts_by_project(
            [normalize_artifact(a) for a in artifacts]
        )
        
        # Verify
        assert "alpha" in grouped
        assert "beta" in grouped
        
        alpha_artifacts = grouped["alpha"]
        beta_artifacts = grouped["beta"]
        
        assert len(alpha_artifacts) >= 2  # spec + pack
        assert len(beta_artifacts) >= 1   # spec
        
        # Verify project_id
        for a in alpha_artifacts:
            assert a.project_id == "alpha"
        for a in beta_artifacts:
            assert a.project_id == "beta"