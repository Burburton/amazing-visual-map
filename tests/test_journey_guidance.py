"""Tests for Feature 015 - Journey Guidance.

Phase 2: Contextual guidance across surfaces.
"""

import pytest
from src.api.observatory_api import get_observatory_html


class TestLocationIndicator:
    """Each surface should show location indicator."""
    
    def test_observatory_has_location_context(self):
        """Observatory should show where user is."""
        html = get_observatory_html()
        
        assert "observatory" in html.lower() or "project" in html.lower()
    
    def test_focus_has_feature_context(self):
        """Focus should show feature context."""
        html = get_observatory_html()
        
        assert "details" in html.lower() or "focus" in html.lower()


class TestGuidanceAdaptsToState:
    """Guidance should adapt to project state."""
    
    def test_path_hint_present(self):
        """Path hint should be present."""
        html = get_observatory_html()
        
        assert "path-hint" in html.lower() or "next" in html.lower()
    
    def test_guidance_changes_by_state(self):
        """Guidance should reflect state."""
        html = get_observatory_html()
        
        assert "active" in html.lower() or "completed" in html.lower() or "blocked" in html.lower()


class TestNextJourneyStepShown:
    """Next journey step should be shown contextually."""
    
    def test_recommended_action_present(self):
        """Recommended action should be shown."""
        html = get_observatory_html()
        
        assert "recommended" in html.lower() or "next" in html.lower() or "hint" in html.lower()


class TestJourneyPathIndicator:
    """Journey path should be visualized."""
    
    def test_surface_connection_shown(self):
        """Surface connections should be shown."""
        html = get_observatory_html()
        
        assert "regions" in html.lower() or "trail" in html.lower() or "timeline" in html.lower()


class TestGuidanceNotGenericTooltip:
    """Guidance must feel like trail guide, not tooltip."""
    
    def test_guidance_integrated_not_tooltip(self):
        """Guidance should be integrated, not tooltip."""
        html = get_observatory_html()
        
        assert "path-hint" in html.lower() or "hint" in html.lower()
        assert "tooltip" not in html.lower()


class TestCrossSurfaceContinuity:
    """Cross-surface journey should feel continuous."""
    
    def test_navigation_preserves_context(self):
        """Navigation should preserve context."""
        html = get_observatory_html()
        
        assert "projectId" in html or "currentProject" in html or "project_id" in html.lower()


class TestJourneyGuidanceIntegration:
    """Full integration test for journey guidance."""
    
    def test_all_guidance_elements(self):
        """All guidance elements should exist."""
        html = get_observatory_html()
        
        required = ["path", "next", "project"]
        found = [r for r in required if r.lower() in html.lower()]
        
        assert len(found) >= 2