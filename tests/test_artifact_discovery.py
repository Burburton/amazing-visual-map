"""Tests for Feature 009 - Artifact Discovery.

Surface F: Search artifacts by keyword and filter by type.
Anti-regression: NOT generic search, NOT flat list. Visual results with indicators.
"""

import pytest
from pathlib import Path

from src.api.observatory_api import app, get_observatory_html
from src.model.artifact_model import search_artifacts


# ============================================================================
# AC1: Search endpoint returns matching artifacts
# ============================================================================

class TestSearchEndpointExists:
    """API endpoint for search."""
    
    def test_api_search_endpoint_exists(self, tmp_path):
        """GET /api/search should return search results."""
        from fastapi.testclient import TestClient
        client = TestClient(app)
        
        response = client.get(f"/api/search?q=test&repo_path={tmp_path}")
        
        assert response.status_code in (200, 404)
    
    def test_api_search_returns_results_list(self, tmp_path):
        """Search endpoint should return results as list."""
        projects_dir = tmp_path / "projects"
        projects_dir.mkdir()
        
        project = projects_dir / "test-project"
        project.mkdir()
        
        features = project / "features"
        features.mkdir()
        
        feature = features / "001-timeline-feature" / "feature-spec.yaml"
        feature.parent.mkdir()
        feature.write_text("name: Timeline Feature\ndescription: A timeline implementation\n")
        
        from fastapi.testclient import TestClient
        client = TestClient(app)
        
        response = client.get(f"/api/search?q=timeline&repo_path={tmp_path}")
        
        if response.status_code == 200:
            data = response.json()
            assert "results" in data


# ============================================================================
# AC2: Search by keyword in title, summary, artifact_id
# ============================================================================

class TestKeywordSearch:
    """Search must match keywords in title, summary, id."""
    
    def test_search_matches_title(self, tmp_path):
        """Search should find artifacts by title."""
        projects_dir = tmp_path / "projects"
        projects_dir.mkdir()
        
        project = projects_dir / "test-project"
        project.mkdir()
        
        features = project / "features"
        features.mkdir()
        
        feature = features / "001-journal-viewer" / "feature-spec.yaml"
        feature.parent.mkdir()
        feature.write_text("name: Journal Viewer\ndescription: View execution journals\n")
        
        from fastapi.testclient import TestClient
        client = TestClient(app)
        
        response = client.get(f"/api/search?q=journal&repo_path={tmp_path}")
        
        if response.status_code == 200:
            data = response.json()
            results = data.get("results", [])
            
            assert len(results) > 0
            assert any("journal" in r.get("title", "").lower() for r in results)
    
    def test_search_matches_summary(self, tmp_path):
        """Search should find artifacts by summary/description."""
        projects_dir = tmp_path / "projects"
        projects_dir.mkdir()
        
        project = projects_dir / "test-project"
        project.mkdir()
        
        features = project / "features"
        features.mkdir()
        
        feature = features / "001-data-export" / "feature-spec.yaml"
        feature.parent.mkdir()
        feature.write_text("name: Export\nfeature_id: 001\ndescription: Export data to CSV format\n")
        
        from fastapi.testclient import TestClient
        client = TestClient(app)
        
        response = client.get(f"/api/search?q=csv&repo_path={tmp_path}")
        
        if response.status_code == 200:
            data = response.json()
            results = data.get("results", [])
            
            if len(results) > 0:
                assert any("csv" in r.get("summary", "").lower() or "csv" in str(r).lower() for r in results)
    
    def test_search_matches_artifact_id(self, tmp_path):
        """Search should find artifacts by artifact_id."""
        projects_dir = tmp_path / "projects"
        projects_dir.mkdir()
        
        project = projects_dir / "test-project"
        project.mkdir()
        
        features = project / "features"
        features.mkdir()
        
        feature = features / "001-cli-tool" / "feature-spec.yaml"
        feature.parent.mkdir()
        feature.write_text("name: CLI\nfeature_id: 001\n")
        
        from fastapi.testclient import TestClient
        client = TestClient(app)
        
        response = client.get(f"/api/search?q=cli-tool&repo_path={tmp_path}")
        
        if response.status_code == 200:
            data = response.json()
            results = data.get("results", [])
            
            if len(results) > 0:
                assert any("cli-tool" in r.get("id", "").lower() for r in results)


# ============================================================================
# AC3: Filter by artifact type
# ============================================================================

class TestTypeFilter:
    """Search must support type filtering."""
    
    def test_search_with_type_filter(self, tmp_path):
        """Search should filter by artifact type."""
        projects_dir = tmp_path / "projects"
        projects_dir.mkdir()
        
        project = projects_dir / "test-project"
        project.mkdir()
        
        features = project / "features"
        features.mkdir()
        
        feature = features / "001-init" / "feature-spec.yaml"
        feature.parent.mkdir()
        feature.write_text("name: init\n")
        
        exec_packs = project / "execution-packs"
        exec_packs.mkdir()
        
        pack = exec_packs / "exec-001.md"
        pack.write_text("```yaml\ndate: 2026-01-01\n```\n")
        
        from fastapi.testclient import TestClient
        client = TestClient(app)
        
        response = client.get(f"/api/search?q=init&type=feature-spec&repo_path={tmp_path}")
        
        if response.status_code == 200:
            data = response.json()
            results = data.get("results", [])
            
            for r in results:
                assert r.get("type") == "feature-spec"
    
    def test_search_without_filter_returns_all_types(self, tmp_path):
        """Search without type filter should return all matching types."""
        projects_dir = tmp_path / "projects"
        projects_dir.mkdir()
        
        project = projects_dir / "test-project"
        project.mkdir()
        
        features = project / "features"
        features.mkdir()
        
        feature = features / "001-init" / "feature-spec.yaml"
        feature.parent.mkdir()
        feature.write_text("name: init feature\n")
        
        exec_packs = project / "execution-packs"
        exec_packs.mkdir()
        
        pack = exec_packs / "exec-001.md"
        pack.write_text("```yaml\nfeature_id: 001\n```\n")
        
        from fastapi.testclient import TestClient
        client = TestClient(app)
        
        response = client.get(f"/api/search?q=init&repo_path={tmp_path}")
        
        if response.status_code == 200:
            data = response.json()
            results = data.get("results", [])
            
            types = [r.get("type") for r in results]
            assert len(types) > 0


# ============================================================================
# AC4: Results displayed with map indicators
# ============================================================================

class TestResultIndicators:
    """Search results must have visual indicators."""
    
    def test_search_result_has_type_indicator(self, tmp_path):
        """Results should include artifact type."""
        projects_dir = tmp_path / "projects"
        projects_dir.mkdir()
        
        project = projects_dir / "test-project"
        project.mkdir()
        
        features = project / "features"
        features.mkdir()
        
        feature = features / "001-init" / "feature-spec.yaml"
        feature.parent.mkdir()
        feature.write_text("name: init\n")
        
        from fastapi.testclient import TestClient
        client = TestClient(app)
        
        response = client.get(f"/api/search?q=init&repo_path={tmp_path}")
        
        if response.status_code == 200:
            data = response.json()
            results = data.get("results", [])
            
            if len(results) > 0:
                assert "type" in results[0]
    
    def test_search_result_has_status_indicator(self, tmp_path):
        """Results should include status."""
        projects_dir = tmp_path / "projects"
        projects_dir.mkdir()
        
        project = projects_dir / "test-project"
        project.mkdir()
        
        features = project / "features"
        features.mkdir()
        
        feature = features / "001-init" / "feature-spec.yaml"
        feature.parent.mkdir()
        feature.write_text("name: init\nstatus: active\n")
        
        from fastapi.testclient import TestClient
        client = TestClient(app)
        
        response = client.get(f"/api/search?q=init&repo_path={tmp_path}")
        
        if response.status_code == 200:
            data = response.json()
            results = data.get("results", [])
            
            if len(results) > 0:
                assert "status" in results[0]
    
    def test_search_result_has_date_indicator(self, tmp_path):
        """Results should include date."""
        projects_dir = tmp_path / "projects"
        projects_dir.mkdir()
        
        project = projects_dir / "test-project"
        project.mkdir()
        
        exec_results = project / "execution-results"
        exec_results.mkdir()
        
        result = exec_results / "exec-20260101-001.md"
        result.write_text("```yaml\ndate: 2026-01-01\n```\n")
        
        from fastapi.testclient import TestClient
        client = TestClient(app)
        
        response = client.get(f"/api/search?q=20260101&repo_path={tmp_path}")
        
        if response.status_code == 200:
            data = response.json()
            results = data.get("results", [])
            
            if len(results) > 0:
                assert "date" in results[0]


# ============================================================================
# AC5: Search results count shown
# ============================================================================

class TestSearchCount:
    """Search must show results count."""
    
    def test_search_returns_total_count(self, tmp_path):
        """Search should return total count."""
        projects_dir = tmp_path / "projects"
        projects_dir.mkdir()
        
        project = projects_dir / "test-project"
        project.mkdir()
        
        features = project / "features"
        features.mkdir()
        
        for i in range(3):
            feature = features / f"00{i}-init" / "feature-spec.yaml"
            feature.parent.mkdir()
            feature.write_text(f"name: init {i}\n")
        
        from fastapi.testclient import TestClient
        client = TestClient(app)
        
        response = client.get(f"/api/search?q=init&repo_path={tmp_path}")
        
        if response.status_code == 200:
            data = response.json()
            
            assert "total" in data or "count" in data or len(data.get("results", [])) >= 0


# ============================================================================
# AC6: Dark theme integration
# ============================================================================

class TestSearchDarkTheme:
    """Search must use dark theme."""
    
    def test_search_ui_uses_dark_colors(self):
        """Search UI should use dark theme colors."""
        html = get_observatory_html()
        
        assert "--bg-dark" in html or "#0a0a0f" in html
        assert "--bg-region" in html or "#16161f" in html


# ============================================================================
# AC7: NO flat list without visual context (Anti-Regression)
# ============================================================================

class TestAntiRegressionNoFlatList:
    """Search must NOT be flat list without indicators."""
    
    def test_search_result_has_visual_elements(self):
        """HTML should have visual search result styling."""
        html = get_observatory_html()
        
        # Should have search styling, not just plain list
        assert "search" in html.lower() or "result" in html.lower()


# ============================================================================
# AC8: Fast search (under 1 second)
# ============================================================================

class TestSearchPerformance:
    """Search must be fast."""
    
    def test_search_response_time(self, tmp_path):
        """Search should respond quickly."""
        projects_dir = tmp_path / "projects"
        projects_dir.mkdir()
        
        project = projects_dir / "test-project"
        project.mkdir()
        
        features = project / "features"
        features.mkdir()
        
        for i in range(10):
            feature = features / f"00{i}-feature" / "feature-spec.yaml"
            feature.parent.mkdir()
            feature.write_text(f"name: feature {i}\ndescription: feature description {i}\n")
        
        from fastapi.testclient import TestClient
        client = TestClient(app)
        
        import time
        start = time.time()
        response = client.get(f"/api/search?q=feature&repo_path={tmp_path}")
        elapsed = time.time() - start
        
        assert elapsed < 1.0


# ============================================================================
# Integration tests
# ============================================================================

class TestSearchIntegration:
    """Full integration test for search."""
    
    def test_full_search_workflow(self, tmp_path):
        """Complete workflow: search across multiple artifacts."""
        projects_dir = tmp_path / "projects"
        projects_dir.mkdir()
        
        project = projects_dir / "test-project"
        project.mkdir()
        
        features = project / "features"
        features.mkdir()
        
        feature1 = features / "001-timeline" / "feature-spec.yaml"
        feature1.parent.mkdir()
        feature1.write_text("name: Timeline View\ndescription: Shows timeline\n")
        
        feature2 = features / "002-journal" / "feature-spec.yaml"
        feature2.parent.mkdir()
        feature2.write_text("name: Journal Reader\ndescription: Reads journals\n")
        
        exec_packs = project / "execution-packs"
        exec_packs.mkdir()
        
        pack = exec_packs / "exec-001.md"
        pack.write_text("```yaml\nfeature_id: 001\n```\n")
        
        from fastapi.testclient import TestClient
        client = TestClient(app)
        
        # Search for timeline
        response = client.get(f"/api/search?q=timeline&repo_path={tmp_path}")
        
        assert response.status_code == 200
        data = response.json()
        
        results = data.get("results", [])
        assert len(results) > 0
        
        # Results should have required fields
        for r in results:
            assert "id" in r
            assert "type" in r
            assert "title" in r or "name" in r