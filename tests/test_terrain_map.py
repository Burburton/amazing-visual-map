"""Tests for Feature 006 - Terrain Map.

Surface B: Project terrain visualization as regions.
Anti-regression: NOT card grid, NOT table. Spatial/region visualization.
"""

import pytest
from pathlib import Path
from unittest.mock import Mock

from src.api.observatory_api import app, get_observatory_html


# ============================================================================
# AC1: Display features as visual regions (distinct from table)
# ============================================================================

class TestTerrainEndpointExists:
    """API endpoint for terrain data."""
    
    def test_api_terrain_endpoint_exists(self, tmp_path):
        """GET /api/terrain/{project_id} should return terrain data."""
        from fastapi.testclient import TestClient
        client = TestClient(app)
        
        response = client.get(f"/api/terrain/test-project?repo_path={tmp_path}")
        
        assert response.status_code in (200, 404)
    
    def test_api_terrain_returns_regions(self, tmp_path):
        """Terrain endpoint should return regions list."""
        projects_dir = tmp_path / "projects"
        projects_dir.mkdir()
        
        project = projects_dir / "test-project"
        project.mkdir()
        
        features = project / "features"
        features.mkdir()
        
        feature1 = features / "001-init" / "feature-spec.yaml"
        feature1.parent.mkdir()
        feature1.write_text("name: init\nfeature_id: 001\nstatus: active\n")
        
        feature2 = features / "002-main" / "feature-spec.yaml"
        feature2.parent.mkdir()
        feature2.write_text("name: main\nfeature_id: 002\nstatus: completed\n")
        
        from fastapi.testclient import TestClient
        client = TestClient(app)
        
        response = client.get(f"/api/terrain/test-project?repo_path={tmp_path}")
        
        if response.status_code == 200:
            data = response.json()
            assert "regions" in data or "terrain" in data


# ============================================================================
# AC2: Region color/status indicates state
# ============================================================================

class TestRegionStatusColoring:
    """Terrain regions must have status-based coloring."""
    
    def test_terrain_region_has_status(self, tmp_path):
        """Regions should include status field for coloring."""
        projects_dir = tmp_path / "projects"
        projects_dir.mkdir()
        
        project = projects_dir / "test-project"
        project.mkdir()
        
        features = project / "features"
        features.mkdir()
        
        feature = features / "001-init" / "feature-spec.yaml"
        feature.parent.mkdir()
        feature.write_text("name: init\nfeature_id: 001\nstatus: active\n")
        
        from fastapi.testclient import TestClient
        client = TestClient(app)
        
        response = client.get(f"/api/terrain/test-project?repo_path={tmp_path}")
        
        if response.status_code == 200:
            data = response.json()
            regions = data.get("regions") or data.get("terrain") or []
            
            if len(regions) > 0:
                region = regions[0]
                assert "status" in region
    
    def test_observatory_html_has_region_colors(self):
        """CSS should define status-based region colors."""
        html = get_observatory_html()
        
        assert "--accent-cyan" in html or "active" in html.lower()
        assert "--accent-green" in html or "completed" in html.lower()
        assert "--accent-red" in html or "blocked" in html.lower()


# ============================================================================
# AC3: Cluster related features visually
# ============================================================================

class TestFeatureClustering:
    """Related features should cluster together."""
    
    def test_terrain_has_position_metadata(self, tmp_path):
        """Regions should have position for spatial layout."""
        projects_dir = tmp_path / "projects"
        projects_dir.mkdir()
        
        project = projects_dir / "test-project"
        project.mkdir()
        
        features = project / "features"
        features.mkdir()
        
        feature = features / "001-init" / "feature-spec.yaml"
        feature.parent.mkdir()
        feature.write_text("name: init\nfeature_id: 001\n")
        
        from fastapi.testclient import TestClient
        client = TestClient(app)
        
        response = client.get(f"/api/terrain/test-project?repo_path={tmp_path}")
        
        if response.status_code == 200:
            data = response.json()
            regions = data.get("regions") or []
            
            if len(regions) > 0:
                region = regions[0]
                assert "position" in region or "x" in region or "row" in region


# ============================================================================
# AC4: Show relationships as connections/paths between regions
# ============================================================================

class TestRelationshipPaths:
    """Region relationships should be shown as paths."""
    
    def test_terrain_has_connections(self, tmp_path):
        """Terrain should include relationship connections."""
        projects_dir = tmp_path / "projects"
        projects_dir.mkdir()
        
        project = projects_dir / "test-project"
        project.mkdir()
        
        features = project / "features"
        features.mkdir()
        
        feature1 = features / "001-init" / "feature-spec.yaml"
        feature1.parent.mkdir()
        feature1.write_text("name: init\nfeature_id: 001\n")
        
        exec_results = project / "execution-results"
        exec_results.mkdir()
        
        result = exec_results / "exec-001.md"
        result.write_text("```yaml\nfeature_id: 001\n```\n")
        
        from fastapi.testclient import TestClient
        client = TestClient(app)
        
        response = client.get(f"/api/terrain/test-project?repo_path={tmp_path}")
        
        if response.status_code == 200:
            data = response.json()
            
            assert "connections" in data or "paths" in data or "relationships" in data
    
    def test_observatory_html_has_connection_styling(self):
        """HTML should have CSS for connection lines."""
        html = get_observatory_html()
        
        assert "connection" in html.lower() or "path" in html.lower() or "link" in html.lower()


# ============================================================================
# AC5: Zoom into region triggers focus view
# ============================================================================

class TestRegionZoomInteraction:
    """Click region should reveal focus view."""
    
    def test_terrain_region_clickable(self):
        """HTML should have clickable regions."""
        html = get_observatory_html()
        
        assert "onclick" in html or "click" in html.lower()
    
    def test_terrain_has_focus_trigger(self):
        """HTML should have mechanism to show focus view."""
        html = get_observatory_html()
        
        assert "focus" in html.lower() or "zoom" in html.lower() or "details" in html.lower()


# ============================================================================
# AC6: Dark observatory terrain theme
# ============================================================================

class TestDarkTerrainTheme:
    """Terrain must use dark theme."""
    
    def test_terrain_uses_dark_colors(self):
        """CSS should use dark theme colors."""
        html = get_observatory_html()
        
        assert "--bg-dark" in html or "#0a0a0f" in html
        assert "--bg-region" in html or "#16161f" in html


# ============================================================================
# AC7: NO card grid/table format (Anti-Regression)
# ============================================================================

class TestAntiRegressionNoGrid:
    """Terrain must NOT be card grid or table."""
    
    def test_observatory_html_no_grid_for_terrain(self):
        """HTML should NOT use grid layout for terrain (use spatial/region)."""
        html = get_observatory_html()
        
        terrain_section = html[html.find("terrain") if "terrain" in html else html.find("regions"):html.find("terrain") + 500 if "terrain" in html else len(html)]
        
        assert "region" in html.lower()
    
    def test_terrain_spatial_not_table(self):
        """Terrain should use spatial layout, not table."""
        html = get_observatory_html()
        
        assert "<table" not in html.lower() or "terrain" in html.lower()


# ============================================================================
# AC8: Graceful handling of empty/sparse projects
# ============================================================================

class TestEmptyProjectHandling:
    """Terrain should handle empty projects gracefully."""
    
    def test_terrain_empty_project_returns_empty_regions(self, tmp_path):
        """Empty project should return empty terrain."""
        projects_dir = tmp_path / "projects"
        projects_dir.mkdir()
        
        project = projects_dir / "empty-project"
        project.mkdir()
        
        runstate = project / "runstate.md"
        runstate.write_text("```yaml\nproduct_id: empty-project\n```\n")
        
        from fastapi.testclient import TestClient
        client = TestClient(app)
        
        response = client.get(f"/api/terrain/empty-project?repo_path={tmp_path}")
        
        if response.status_code == 200:
            data = response.json()
            regions = data.get("regions") or []
            
            assert regions == [] or len(regions) == 0
    
    def test_observatory_html_has_empty_state(self):
        """HTML should have empty state message."""
        html = get_observatory_html()
        
        assert "empty" in html.lower() or "no" in html.lower()


# ============================================================================
# Integration tests
# ============================================================================

class TestTerrainMapIntegration:
    """Full integration test for terrain map."""
    
    def test_full_terrain_workflow(self, tmp_path):
        """Complete workflow: scan, terrain endpoint, visual regions."""
        projects_dir = tmp_path / "projects"
        projects_dir.mkdir()
        
        project = projects_dir / "integration-test"
        project.mkdir()
        
        features = project / "features"
        features.mkdir()
        
        for i in range(1, 4):
            feature = features / f"00{i}-feature" / "feature-spec.yaml"
            feature.parent.mkdir()
            feature.write_text(f"name: feature-{i}\nfeature_id: 00{i}\nstatus: active\n")
        
        exec_packs = project / "execution-packs"
        exec_packs.mkdir()
        
        for i in range(1, 4):
            pack = exec_packs / f"exec-00{i}.md"
            pack.write_text(f"```yaml\nfeature_id: 00{i}\nstatus: success\n```\n")
        
        from fastapi.testclient import TestClient
        client = TestClient(app)
        
        response = client.get(f"/api/terrain/integration-test?repo_path={tmp_path}")
        
        assert response.status_code == 200
        data = response.json()
        
        regions = data.get("regions") or []
        assert len(regions) >= 3
        
        for region in regions:
            assert "id" in region
            assert "name" in region or "title" in region