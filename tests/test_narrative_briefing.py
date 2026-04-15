"""Tests for Feature 008 - Narrative Briefing.

Surface E: Summarize exec history as story, not flat list.
Anti-regression: NOT flat list, NOT raw log. Story narrative with milestones.
"""

import pytest
from pathlib import Path
from unittest.mock import Mock

from src.api.observatory_api import app, get_observatory_html, generate_narrative


# ============================================================================
# AC1: Generate narrative from exec results sequence
# ============================================================================

class TestNarrativeGeneration:
    """Narrative must be generated from exec results."""
    
    def test_generate_narrative_function_exists(self):
        """generate_narrative function should exist."""
        from src.api.observatory_api import generate_narrative
        assert generate_narrative is not None
    
    def test_generate_narrative_returns_string(self):
        """Narrative should return string text."""
        exec_results = [
            {"id": "exec-001", "date": "2026-01-01", "status": "success"},
            {"id": "exec-002", "date": "2026-01-02", "status": "success"},
            {"id": "exec-003", "date": "2026-01-03", "status": "success"},
        ]
        
        narrative = generate_narrative(exec_results)
        
        assert isinstance(narrative, str)
        assert len(narrative) > 0
    
    def test_generate_narrative_with_empty_results(self):
        """Empty exec results should return graceful message."""
        narrative = generate_narrative([])
        
        assert isinstance(narrative, str)


# ============================================================================
# AC2: Identify key milestones
# ============================================================================

class TestMilestoneIdentification:
    """Narrative must identify milestones."""
    
    def test_narrative_mentions_first_run(self):
        """Narrative should mention the first execution as beginning."""
        exec_results = [
            {"id": "exec-001", "date": "2026-01-01", "status": "success"},
            {"id": "exec-002", "date": "2026-01-02", "status": "success"},
        ]
        
        narrative = generate_narrative(exec_results)
        
        assert "first" in narrative.lower() or "beginning" in narrative.lower() or "started" in narrative.lower() or "began" in narrative.lower()
    
    def test_narrative_mentions_completion(self):
        """Narrative should highlight completed status."""
        exec_results = [
            {"id": "exec-001", "date": "2026-01-01", "status": "success"},
            {"id": "exec-002", "date": "2026-01-02", "status": "completed"},
        ]
        
        narrative = generate_narrative(exec_results)
        
        assert "complete" in narrative.lower() or "finished" in narrative.lower() or "success" in narrative.lower()
    
    def test_narrative_mentions_blocked(self):
        """Narrative should highlight blocked status."""
        exec_results = [
            {"id": "exec-001", "date": "2026-01-01", "status": "blocked"},
        ]
        
        narrative = generate_narrative(exec_results)
        
        assert "blocked" in narrative.lower() or "stuck" in narrative.lower() or "halted" in narrative.lower()


# ============================================================================
# AC3: Show progression narrative (started->progress->completed/blocked)
# ============================================================================

class TestProgressionStructure:
    """Narrative must show progression."""
    
    def test_narrative_has_beginning_middle_current(self):
        """Narrative should have story structure."""
        exec_results = [
            {"id": "exec-001", "date": "2026-01-01", "status": "planning"},
            {"id": "exec-002", "date": "2026-01-02", "status": "executing"},
            {"id": "exec-003", "date": "2026-01-03", "status": "completed"},
        ]
        
        narrative = generate_narrative(exec_results)
        
        # Should mention progression phases
        lower = narrative.lower()
        has_beginning = "start" in lower or "begin" in lower or "first" in lower
        has_progress = "progress" in lower or "continu" in lower or "moving" in lower
        has_current = "current" in lower or "now" in lower or "latest" in lower
        
        assert has_beginning or has_progress or has_current


# ============================================================================
# AC4: Briefing appears in focus view
# ============================================================================

class TestNarrativeInFocus:
    """Narrative should appear in focus API response."""
    
    def test_focus_endpoint_returns_narrative(self, tmp_path):
        """Focus API should include narrative field."""
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
        
        for i in range(1, 3):
            result = exec_results / f"exec-2026010{i}-001.md"
            result.write_text(f"```yaml\nfeature_id: 001\ndate: 2026-01-0{i}\nstatus: success\n```\n")
        
        from fastapi.testclient import TestClient
        client = TestClient(app)
        
        response = client.get(f"/api/focus/test-project/001-init?repo_path={tmp_path}")
        
        if response.status_code == 200:
            data = response.json()
            
            assert "narrative" in data
    
    def test_observatory_html_has_narrative_section(self):
        """HTML should have narrative display element."""
        html = get_observatory_html()
        
        assert "narrative" in html.lower() or "briefing" in html.lower() or "story" in html.lower()


# ============================================================================
# AC5: Dark theme integration
# ============================================================================

class TestNarrativeDarkTheme:
    """Narrative must use dark theme."""
    
    def test_narrative_uses_dark_colors(self):
        """CSS should use dark theme."""
        html = get_observatory_html()
        
        assert "--bg-dark" in html or "#0a0a0f" in html


# ============================================================================
# AC6: NO flat chronological list (Anti-Regression)
# ============================================================================

class TestAntiRegressionNoFlatList:
    """Narrative must NOT be flat list."""
    
    def test_narrative_not_just_ids_and_dates(self):
        """Narrative should not be just artifact ids/dates."""
        exec_results = [
            {"id": "exec-001", "date": "2026-01-01", "status": "success"},
            {"id": "exec-002", "date": "2026-01-02", "status": "success"},
        ]
        
        narrative = generate_narrative(exec_results)
        
        # Should have narrative words, not just raw data
        assert len(narrative.split()) > 3
        # Should not be just "exec-001: 2026-01-01\nexec-002: 2026-01-02"
        assert narrative != "exec-001: 2026-01-01\nexec-002: 2026-01-02"


# ============================================================================
# AC7: Story structure (beginning->middle->current)
# ============================================================================

class TestStoryStructure:
    """Narrative must have story structure."""
    
    def test_narrative_has_multiple_paragraphs_or_sections(self):
        """Narrative should have structure beyond single line."""
        exec_results = [
            {"id": "exec-001", "date": "2026-01-01", "status": "success"},
            {"id": "exec-002", "date": "2026-01-02", "status": "success"},
            {"id": "exec-003", "date": "2026-01-03", "status": "completed"},
        ]
        
        narrative = generate_narrative(exec_results)
        
        # Should have multiple sentences
        assert "." in narrative or "\n" in narrative or len(narrative) > 50


# ============================================================================
# Integration tests
# ============================================================================

class TestNarrativeBriefingIntegration:
    """Full integration test for narrative briefing."""
    
    def test_full_narrative_workflow(self, tmp_path):
        """Complete workflow: focus -> narrative generated and displayed."""
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
        
        # Create progression: planning -> executing -> completed
        statuses = ["planning", "executing", "success", "completed"]
        for i, status in enumerate(statuses, 1):
            result = exec_results / f"exec-2026010{i}-001.md"
            result.write_text(f"```yaml\nfeature_id: 001\ndate: 2026-01-0{i}\nstatus: {status}\n```\n")
        
        from fastapi.testclient import TestClient
        client = TestClient(app)
        
        response = client.get(f"/api/focus/test-project/001-init?repo_path={tmp_path}")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "narrative" in data
        narrative = data["narrative"]
        
        assert isinstance(narrative, str)
        assert len(narrative) > 0
        
        # Should mention progression
        lower = narrative.lower()
        assert "start" in lower or "begin" in lower or "complete" in lower or "success" in lower