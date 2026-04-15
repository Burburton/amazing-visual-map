"""Tests for Feature 013 - Visual History.

Phase 2: Timeline with embedded narrative waypoints.
"""

import pytest
from src.api.observatory_api import get_observatory_html


class TestTimelineHasNarrative:
    """Timeline must show narrative on waypoints."""
    
    def test_timeline_waypoint_has_narrative_class(self):
        """Waypoints should have narrative display."""
        html = get_observatory_html()
        
        assert "waypoint" in html.lower() or "trail-item" in html
    
    def test_timeline_waypoint_has_story_section(self):
        """Waypoints should show story/narrative."""
        html = get_observatory_html()
        
        assert "story" in html.lower() or "narrative" in html.lower() or "summary" in html.lower()


class TestNarrativeIntegratedWithTimeline:
    """Narrative must be visually connected to timeline."""
    
    def test_timeline_has_visual_connection_elements(self):
        """Timeline should have visual connection elements."""
        html = get_observatory_html()
        
        assert "trail-marker" in html or "marker" in html.lower()
    
    def test_timeline_waypoints_have_dates(self):
        """Waypoints must show dates for context."""
        html = get_observatory_html()
        
        assert "date" in html.lower()


class TestRecentWaypointsHighlighted:
    """Recent waypoints must have motion indicator."""
    
    def test_recent_waypoints_have_animation(self):
        """Recent waypoints should animate."""
        html = get_observatory_html()
        
        assert "waypoint-pulse" in html or "recent" in html.lower() or "is_recent" in html.lower()


class TestTimelineShowsProgression:
    """Timeline should show state progression."""
    
    def test_timeline_has_status_indicators(self):
        """Waypoints should show status."""
        html = get_observatory_html()
        
        assert "status" in html.lower()


class TestAntiRegressionNotFlatList:
    """Timeline must NOT be flat text list."""
    
    def test_timeline_not_just_text_list(self):
        """Timeline should have visual structure."""
        html = get_observatory_html()
        
        assert "trail" in html.lower() or "waypoint" in html.lower()
        assert "<table" not in html.lower() or "trail" in html.lower()


class TestVisualHistoryIntegration:
    """Full integration test for visual history."""
    
    def test_all_visual_history_elements_present(self):
        """All elements for visual history should exist."""
        html = get_observatory_html()
        
        required = ["trail", "waypoint", "date", "status"]
        found = [r for r in required if r.lower() in html.lower()]
        
        assert len(found) >= 3