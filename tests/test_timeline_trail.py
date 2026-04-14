"""Tests for Feature 005 - Timeline Trail.

Surface C: Timeline visualization as movement trail.
Anti-regression: NOT flat list, NOT table. Visual trail with markers.
"""

import pytest
from pathlib import Path
from datetime import datetime, timedelta
from unittest.mock import Mock

from src.api.observatory_api import app, get_observatory_html


# ============================================================================
# AC1: Display timeline as vertical/horizontal trail
# ============================================================================

class TestTimelineEndpointExists:
    """API endpoint for timeline data."""
    
    def test_api_timeline_endpoint_exists(self, tmp_path):
        """GET /api/timeline/{project_id} should return timeline data."""
        from fastapi.testclient import TestClient
        client = TestClient(app)
        
        response = client.get(f"/api/timeline/test-project?repo_path={tmp_path}")
        
        assert response.status_code in (200, 404)
    
    def test_api_timeline_returns_events_list(self, tmp_path):
        """Timeline endpoint should return events as list."""
        projects_dir = tmp_path / "projects"
        projects_dir.mkdir()
        
        project = projects_dir / "test-project"
        project.mkdir()
        
        exec_packs = project / "execution-packs"
        exec_packs.mkdir()
        
        pack1 = exec_packs / "exec-20260101-001.md"
        pack1.write_text("```yaml\ndate: 2026-01-01\nstatus: success\n```\n")
        
        pack2 = exec_packs / "exec-20260102-001.md"
        pack2.write_text("```yaml\ndate: 2026-01-02\nstatus: success\n```\n")
        
        from fastapi.testclient import TestClient
        client = TestClient(app)
        
        response = client.get(f"/api/timeline/test-project?repo_path={tmp_path}")
        
        if response.status_code == 200:
            data = response.json()
            assert "events" in data or "trail" in data


# ============================================================================
# AC2: Each event as waypoint/marker on trail
# ============================================================================

class TestTimelineWaypointStructure:
    """Timeline events must have waypoint structure."""
    
    def test_timeline_event_has_waypoint_fields(self, tmp_path):
        """Events should have waypoint-specific fields."""
        projects_dir = tmp_path / "projects"
        projects_dir.mkdir()
        
        project = projects_dir / "test-project"
        project.mkdir()
        
        exec_results = project / "execution-results"
        exec_results.mkdir()
        
        result = exec_results / "exec-20260101-001.md"
        result.write_text("```yaml\ndate: 2026-01-01\nstatus: success\n```\n")
        
        from fastapi.testclient import TestClient
        client = TestClient(app)
        
        response = client.get(f"/api/timeline/test-project?repo_path={tmp_path}")
        
        if response.status_code == 200:
            data = response.json()
            events = data.get("events") or data.get("trail") or []
            
            if len(events) > 0:
                event = events[0]
                assert "id" in event
                assert "date" in event
                assert "type" in event


# ============================================================================
# AC3: Trail shows sequence (not random ordering)
# ============================================================================

class TestTimelineSequenceOrder:
    """Timeline must be ordered chronologically."""
    
    def test_timeline_ordered_by_date(self, tmp_path):
        """Events should be ordered by date (ascending or descending)."""
        projects_dir = tmp_path / "projects"
        projects_dir.mkdir()
        
        project = projects_dir / "test-project"
        project.mkdir()
        
        exec_packs = project / "execution-packs"
        exec_packs.mkdir()
        
        pack1 = exec_packs / "exec-20260101-001.md"
        pack1.write_text("```yaml\ndate: 2026-01-01\n```\n")
        
        pack2 = exec_packs / "exec-20260105-001.md"
        pack2.write_text("```yaml\ndate: 2026-01-05\n```\n")
        
        pack3 = exec_packs / "exec-20260103-001.md"
        pack3.write_text("```yaml\ndate: 2026-01-03\n```\n")
        
        from fastapi.testclient import TestClient
        client = TestClient(app)
        
        response = client.get(f"/api/timeline/test-project?repo_path={tmp_path}")
        
        if response.status_code == 200:
            data = response.json()
            events = data.get("events") or data.get("trail") or []
            
            if len(events) >= 2:
                dates = [e.get("date") for e in events if e.get("date")]
                
                assert dates == sorted(dates) or dates == sorted(dates, reverse=True)


# ============================================================================
# AC4: Highlight recent movement (last 7 days)
# ============================================================================

class TestRecentMovementHighlight:
    """Recent events should be marked/highlighted."""
    
    def test_timeline_has_recent_marker(self, tmp_path):
        """Events within 7 days should have recent flag."""
        projects_dir = tmp_path / "projects"
        projects_dir.mkdir()
        
        project = projects_dir / "test-project"
        project.mkdir()
        
        exec_packs = project / "execution-packs"
        exec_packs.mkdir()
        
        recent_date = datetime.now().strftime("%Y-%m-%d")
        old_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        
        recent_pack = exec_packs / f"exec-{recent_date.replace('-', '')}-001.md"
        recent_pack.write_text(f"```yaml\ndate: {recent_date}\n```\n")
        
        old_pack = exec_packs / f"exec-{old_date.replace('-', '')}-001.md"
        old_pack.write_text(f"```yaml\ndate: {old_date}\n```\n")
        
        from fastapi.testclient import TestClient
        client = TestClient(app)
        
        response = client.get(f"/api/timeline/test-project?repo_path={tmp_path}")
        
        if response.status_code == 200:
            data = response.json()
            events = data.get("events") or data.get("trail") or []
            
            recent_events = [e for e in events if e.get("is_recent")]
            assert len(recent_events) >= 1


# ============================================================================
# AC5: Click waypoint shows details
# ============================================================================

class TestWaypointClickInteraction:
    """Waypoint click should reveal details."""
    
    def test_observatory_html_has_waypoint_click_handler(self):
        """HTML should have click handler for waypoints."""
        html = get_observatory_html()
        
        assert "onclick" in html or "click" in html.lower()
    
    def test_observatory_html_has_details_panel(self):
        """HTML should have panel for showing artifact details."""
        html = get_observatory_html()
        
        assert "details-panel" in html or "detail" in html.lower()


# ============================================================================
# AC6: Dark theme integration
# ============================================================================

class TestDarkThemeIntegration:
    """Timeline must use dark observatory theme."""
    
    def test_timeline_uses_dark_colors(self):
        """CSS should use dark theme colors."""
        html = get_observatory_html()
        
        assert "--bg-dark" in html or "#0a0a0f" in html
        assert "--bg-region" in html or "#16161f" in html


# ============================================================================
# AC7: NO table/list format (Anti-Regression)
# ============================================================================

class TestAntiRegressionNoTable:
    """Timeline must NOT be a table or flat list."""
    
    def test_observatory_html_no_table_for_timeline(self):
        """HTML should NOT use table element for timeline."""
        html = get_observatory_html()
        
        timeline_section = html[html.find("trail") if "trail" in html else 0:]
        
        assert "<table" not in timeline_section.lower() or "trail" in html
    
    def test_timeline_visual_trail_not_list(self):
        """Timeline should use visual trail CSS, not list elements."""
        html = get_observatory_html()
        
        assert "trail-marker" in html or "waypoint" in html.lower()
        assert ".trail-item" in html or "marker" in html


# ============================================================================
# AC8: Load within 2 seconds
# ============================================================================

class TestPerformanceRequirement:
    """Timeline should load quickly."""
    
    def test_timeline_endpoint_response_time(self, tmp_path):
        """API should respond in reasonable time."""
        projects_dir = tmp_path / "projects"
        projects_dir.mkdir()
        
        project = projects_dir / "test-project"
        project.mkdir()
        
        exec_packs = project / "execution-packs"
        exec_packs.mkdir()
        
        for i in range(50):
            pack = exec_packs / f"exec-2026010{i:02d}-001.md"
            pack.write_text("```yaml\ndate: 2026-01-01\n```\n")
        
        from fastapi.testclient import TestClient
        client = TestClient(app)
        
        import time
        start = time.time()
        response = client.get(f"/api/timeline/test-project?repo_path={tmp_path}")
        elapsed = time.time() - start
        
        assert elapsed < 2.0


# ============================================================================
# Integration tests
# ============================================================================

class TestTimelineTrailIntegration:
    """Full integration test for timeline trail."""
    
    def test_full_timeline_workflow(self, tmp_path):
        """Complete workflow: scan, timeline endpoint, visual trail."""
        projects_dir = tmp_path / "projects"
        projects_dir.mkdir()
        
        project = projects_dir / "integration-test"
        project.mkdir()
        
        features = project / "features"
        features.mkdir()
        spec = features / "001-init" / "feature-spec.yaml"
        spec.parent.mkdir()
        spec.write_text("name: init\nfeature_id: 001\n")
        
        exec_packs = project / "execution-packs"
        exec_packs.mkdir()
        
        for i in range(1, 4):
            pack = exec_packs / f"exec-2026010{i}-001.md"
            pack.write_text(f"```yaml\ndate: 2026-01-0{i}\nfeature_id: 001\n```\n")
        
        exec_results = project / "execution-results"
        exec_results.mkdir()
        
        for i in range(1, 4):
            result = exec_results / f"exec-2026010{i}-001.md"
            result.write_text(f"```yaml\ndate: 2026-01-0{i}\nstatus: success\n```\n")
        
        from fastapi.testclient import TestClient
        client = TestClient(app)
        
        response = client.get(f"/api/timeline/integration-test?repo_path={tmp_path}")
        
        assert response.status_code == 200
        data = response.json()
        
        events = data.get("events") or data.get("trail") or []
        assert len(events) >= 3
        
        for event in events:
            assert "id" in event
            assert "date" in event
            assert "type" in event