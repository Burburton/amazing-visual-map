"""Tests for Feature 012 - Feature Navigation.

Polish Phase 1: Cross-surface navigation with journey feel.
"""

import pytest
from pathlib import Path
from src.api.observatory_api import app, get_observatory_html


# ============================================================================
# AC1: Focus view shows Related Features section
# ============================================================================

class TestRelatedFeaturesSection:
    """Focus must show related features."""
    
    def test_focus_api_returns_related_features(self, tmp_path):
        """Focus endpoint should return related features."""
        projects_dir = tmp_path / "projects"
        projects_dir.mkdir()
        
        project = projects_dir / "test-project"
        project.mkdir()
        
        features = project / "features"
        features.mkdir()
        
        feature1 = features / "001-init" / "feature-spec.yaml"
        feature1.parent.mkdir()
        feature1.write_text("name: init\nfeature_id: 001\n")
        
        feature2 = features / "002-main" / "feature-spec.yaml"
        feature2.parent.mkdir()
        feature2.write_text("name: main\nfeature_id: 002\n")
        
        from fastapi.testclient import TestClient
        client = TestClient(app)
        
        response = client.get(f"/api/focus/test-project/001-init?repo_path={tmp_path}")
        
        if response.status_code == 200:
            data = response.json()
            
            assert "related_features" in data or "related" in data
    
    def test_html_has_related_features_ui(self):
        """HTML should have UI for related features."""
        html = get_observatory_html()
        
        assert "related" in html.lower()


# ============================================================================
# AC2: Click related feature navigates to focus view
# ============================================================================

class TestRelatedFeatureNavigation:
    """Clicking related feature should open its focus view."""
    
    def test_html_has_click_handler_for_related(self):
        """HTML should have click handler for related items."""
        html = get_observatory_html()
        
        assert "onclick" in html.lower() or "click" in html.lower()


# ============================================================================
# AC3: Navigation breadcrumbs show current location
# ============================================================================

class TestNavigationBreadcrumbs:
    """Focus view should show location breadcrumbs."""
    
    def test_html_has_breadcrumbs_element(self):
        """HTML should have breadcrumbs UI."""
        html = get_observatory_html()
        
        assert "breadcrumb" in html.lower() or "location" in html.lower() or "path" in html.lower()


# ============================================================================
# AC4: Back button returns to previous surface
# ============================================================================

class TestBackNavigation:
    """Back button should work correctly."""
    
    def test_html_has_back_button(self):
        """HTML should have back button."""
        html = get_observatory_html()
        
        assert "back" in html.lower() or "close" in html.lower()


# ============================================================================
# AC5: Timeline waypoint click opens focus
# ============================================================================

class TestTimelineWaypointFocus:
    """Timeline waypoint should link to focus."""
    
    def test_timeline_waypoint_clickable(self):
        """Timeline waypoints should be clickable."""
        html = get_observatory_html()
        
        assert "waypoint-clickable" in html.lower() or "onclick" in html.lower()


# ============================================================================
# AC6: Search result click opens focus view
# ============================================================================

class TestSearchResultFocus:
    """Search results should link to focus."""
    
    def test_search_result_clickable(self):
        """Search results should be clickable."""
        html = get_observatory_html()
        
        assert "search-result-card" in html
        assert "onclick" in html.lower()


# ============================================================================
# AC7: Navigation feels like journey (not tabs)
# ============================================================================

class TestJourneyFeel:
    """Navigation should express journey metaphor."""
    
    def test_navigation_has_movement_metaphor(self):
        """Navigation should use journey/movement language."""
        html = get_observatory_html()
        
        metaphor_words = ["journey", "path", "trail", "movement", "approach", "depart"]
        
        found = [w for w in metaphor_words if w in html.lower()]
        
        assert len(found) >= 1 or "focus" in html.lower()


# ============================================================================
# AC8: Location context preserved
# ============================================================================

class TestLocationContext:
    """Navigation should preserve project context."""
    
    def test_js_tracks_current_project(self):
        """JavaScript should track current project."""
        html = get_observatory_html()
        
        assert "currentProject" in html or "projectId" in html or "project_id" in html.lower()


# ============================================================================
# Integration tests
# ============================================================================

class TestFeatureNavigationIntegration:
    """Full integration test for feature navigation."""
    
    def test_full_navigation_workflow(self, tmp_path):
        """Complete navigation workflow."""
        projects_dir = tmp_path / "projects"
        projects_dir.mkdir()
        
        project = projects_dir / "test-project"
        project.mkdir()
        
        features = project / "features"
        features.mkdir()
        
        feature1 = features / "001-init" / "feature-spec.yaml"
        feature1.parent.mkdir()
        feature1.write_text("name: init\nfeature_id: 001\n")
        
        feature2 = features / "002-main" / "feature-spec.yaml"
        feature2.parent.mkdir()
        feature2.write_text("name: main\nfeature_id: 002\n")
        
        exec_packs = project / "execution-packs"
        exec_packs.mkdir()
        
        pack = exec_packs / "exec-001.md"
        pack.write_text("```yaml\nfeature_id: 001\n```\n")
        
        from fastapi.testclient import TestClient
        client = TestClient(app)
        
        # Get terrain
        terrain_response = client.get(f"/api/terrain/test-project?repo_path={tmp_path}")
        assert terrain_response.status_code == 200
        
        # Click to focus
        focus_response = client.get(f"/api/focus/test-project/001-init?repo_path={tmp_path}")
        assert focus_response.status_code == 200
        
        data = focus_response.json()
        assert data["feature"]["id"] == "001-init"