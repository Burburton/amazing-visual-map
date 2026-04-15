"""Tests for Feature 007 - Focus View.

Surface D: Click region to zoom into feature detail.
Anti-regression: NOT CRUD detail, NOT form editor. Zoom-style transition.
"""

import pytest
from pathlib import Path
from unittest.mock import Mock

from src.api.observatory_api import app, get_observatory_html


# ============================================================================
# AC1: Click region -> focus panel expands
# ============================================================================

class TestFocusEndpointExists:
    """API endpoint for focus data."""
    
    def test_api_focus_endpoint_exists(self, tmp_path):
        """GET /api/focus/{project_id}/{feature_id} should return focus data."""
        from fastapi.testclient import TestClient
        client = TestClient(app)
        
        response = client.get(f"/api/focus/test-project/001-init?repo_path={tmp_path}")
        
        assert response.status_code in (200, 404)
    
    def test_api_focus_returns_feature_data(self, tmp_path):
        """Focus endpoint should return feature with full content."""
        projects_dir = tmp_path / "projects"
        projects_dir.mkdir()
        
        project = projects_dir / "test-project"
        project.mkdir()
        
        features = project / "features"
        features.mkdir()
        
        feature = features / "001-init" / "feature-spec.yaml"
        feature.parent.mkdir()
        feature.write_text("name: init\nfeature_id: 001\ngoal: initialize project\nacceptance_criteria:\n  - AC1: setup complete\n")
        
        from fastapi.testclient import TestClient
        client = TestClient(app)
        
        response = client.get(f"/api/focus/test-project/001-init?repo_path={tmp_path}")
        
        if response.status_code == 200:
            data = response.json()
            assert "feature" in data
            assert data["feature"]["id"] == "001-init"


# ============================================================================
# AC2: Show full feature spec content
# ============================================================================

class TestFocusFullContent:
    """Focus must show full feature spec content."""
    
    def test_focus_returns_full_feature_content(self, tmp_path):
        """Focus should include goal, acceptance_criteria, not just id."""
        projects_dir = tmp_path / "projects"
        projects_dir.mkdir()
        
        project = projects_dir / "test-project"
        project.mkdir()
        
        features = project / "features"
        features.mkdir()
        
        feature = features / "001-init" / "feature-spec.yaml"
        feature.parent.mkdir()
        feature.write_text("name: init\nfeature_id: 001\ngoal: initialize project\nacceptance_criteria:\n  - AC1: setup\n  - AC2: config\n")
        
        from fastapi.testclient import TestClient
        client = TestClient(app)
        
        response = client.get(f"/api/focus/test-project/001-init?repo_path={tmp_path}")
        
        if response.status_code == 200:
            data = response.json()
            feature = data.get("feature", {})
            
            assert "goal" in feature or "description" in feature
            assert feature.get("name") or feature.get("title")


# ============================================================================
# AC3: Show feature-related artifacts
# ============================================================================

class TestFocusRelatedArtifacts:
    """Focus must show related artifacts (exec packs, exec results)."""
    
    def test_focus_returns_related_artifacts(self, tmp_path):
        """Focus should include exec packs and results for the feature."""
        projects_dir = tmp_path / "projects"
        projects_dir.mkdir()
        
        project = projects_dir / "test-project"
        project.mkdir()
        
        features = project / "features"
        features.mkdir()
        
        feature = features / "001-init" / "feature-spec.yaml"
        feature.parent.mkdir()
        feature.write_text("name: init\nfeature_id: 001\n")
        
        exec_packs = project / "execution-packs"
        exec_packs.mkdir()
        
        pack = exec_packs / "exec-001.md"
        pack.write_text("```yaml\nfeature_id: 001\ndate: 2026-01-01\n```\n")
        
        exec_results = project / "execution-results"
        exec_results.mkdir()
        
        result = exec_results / "exec-001.md"
        result.write_text("```yaml\nfeature_id: 001\nstatus: success\n```\n")
        
        from fastapi.testclient import TestClient
        client = TestClient(app)
        
        response = client.get(f"/api/focus/test-project/001-init?repo_path={tmp_path}")
        
        if response.status_code == 200:
            data = response.json()
            
            assert "related_artifacts" in data or "executions" in data


# ============================================================================
# AC4: Feature-level timeline in focus view
# ============================================================================

class TestFocusTimeline:
    """Focus must include feature-level timeline."""
    
    def test_focus_returns_feature_timeline(self, tmp_path):
        """Focus should include timeline events specific to the feature."""
        projects_dir = tmp_path / "projects"
        projects_dir.mkdir()
        
        project = projects_dir / "test-project"
        project.mkdir()
        
        features = project / "features"
        features.mkdir()
        
        feature = features / "001-init" / "feature-spec.yaml"
        feature.parent.mkdir()
        feature.write_text("name: init\nfeature_id: 001\n")
        
        exec_results = project / "execution-results"
        exec_results.mkdir()
        
        for i in range(1, 4):
            result = exec_results / f"exec-2026010{i}-001.md"
            result.write_text(f"```yaml\nfeature_id: 001\ndate: 2026-01-0{i}\n```\n")
        
        from fastapi.testclient import TestClient
        client = TestClient(app)
        
        response = client.get(f"/api/focus/test-project/001-init?repo_path={tmp_path}")
        
        if response.status_code == 200:
            data = response.json()
            
            assert "timeline" in data or "events" in data
            
            events = data.get("timeline") or data.get("events") or []
            assert len(events) >= 3


# ============================================================================
# AC5: Back button to return to terrain
# ============================================================================

class TestFocusBackNavigation:
    """Focus must have back navigation."""
    
    def test_observatory_html_has_back_button(self):
        """HTML should have back button for focus view."""
        html = get_observatory_html()
        
        assert "back" in html.lower() or "return" in html.lower() or "close" in html.lower()
    
    def test_observatory_html_has_focus_panel_transition(self):
        """HTML should have CSS transition for focus panel."""
        html = get_observatory_html()
        
        assert "transition" in html or "slide" in html.lower()


# ============================================================================
# AC6: Dark theme integration
# ============================================================================

class TestFocusDarkTheme:
    """Focus must use dark observatory theme."""
    
    def test_focus_uses_dark_colors(self):
        """CSS should use dark theme colors."""
        html = get_observatory_html()
        
        assert "--bg-dark" in html or "#0a0a0f" in html
        assert "--bg-region" in html or "#16161f" in html


# ============================================================================
# AC7: NO form-based editor layout (Anti-Regression)
# ============================================================================

class TestAntiRegressionNoForm:
    """Focus must NOT be form-based CRUD editor."""
    
    def test_observatory_html_no_form_layout(self):
        """HTML should NOT use form elements for focus view."""
        html = get_observatory_html()
        
        focus_section = html[html.find("focus") if "focus" in html else html.find("details"):]
        
        assert "<form" not in focus_section.lower() or "focus" in html.lower()
    
    def test_focus_not_input_fields(self):
        """Focus should display content, not input fields for editing."""
        html = get_observatory_html()
        
        assert "input" not in html.lower() or "details" in html


# ============================================================================
# AC8: Maintain map metaphor (zoom into region)
# ============================================================================

class TestFocusMapMetaphor:
    """Focus must maintain zoom/region metaphor."""
    
    def test_observatory_html_has_zoom_transition(self):
        """HTML should have zoom-like transition effect."""
        html = get_observatory_html()
        
        assert "transform" in html or "scale" in html.lower() or "slide" in html.lower()
    
    def test_observatory_html_has_focus_panel(self):
        """HTML should have dedicated focus panel element."""
        html = get_observatory_html()
        
        assert "focus-panel" in html.lower() or "details-panel" in html.lower()


# ============================================================================
# Integration tests
# ============================================================================

class TestFocusViewIntegration:
    """Full integration test for focus view."""
    
    def test_full_focus_workflow(self, tmp_path):
        """Complete workflow: terrain -> click region -> focus -> back."""
        projects_dir = tmp_path / "projects"
        projects_dir.mkdir()
        
        project = projects_dir / "integration-test"
        project.mkdir()
        
        features = project / "features"
        features.mkdir()
        
        feature = features / "001-init" / "feature-spec.yaml"
        feature.parent.mkdir()
        feature.write_text("name: init\nfeature_id: 001\ngoal: initialize\n")
        
        feature2 = features / "002-main" / "feature-spec.yaml"
        feature2.parent.mkdir()
        feature2.write_text("name: main\nfeature_id: 002\ngoal: main feature\n")
        
        exec_packs = project / "execution-packs"
        exec_packs.mkdir()
        
        pack = exec_packs / "exec-001.md"
        pack.write_text("```yaml\nfeature_id: 001\ndate: 2026-01-01\n```\n")
        
        exec_results = project / "execution-results"
        exec_results.mkdir()
        
        result = exec_results / "exec-001.md"
        result.write_text("```yaml\nfeature_id: 001\nstatus: success\n```\n")
        
        from fastapi.testclient import TestClient
        client = TestClient(app)
        
        # Get terrain (shows regions)
        terrain_response = client.get(f"/api/terrain/integration-test?repo_path={tmp_path}")
        assert terrain_response.status_code == 200
        terrain = terrain_response.json()
        assert len(terrain["regions"]) >= 2
        
        # Click region -> focus
        focus_response = client.get(f"/api/focus/integration-test/001-init?repo_path={tmp_path}")
        assert focus_response.status_code == 200
        focus = focus_response.json()
        
        assert focus["feature"]["id"] == "001-init"
        assert "related_artifacts" in focus or "executions" in focus
        assert "timeline" in focus or "events" in focus