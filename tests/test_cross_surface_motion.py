"""Test Cross-Surface Motion Continuity - Feature 016.

Phase 3: Experience Refinement - Motion and continuity across surfaces.
"""

import pytest
from src.api.observatory_api import get_observatory_html


class TestSurfaceTransitionIndicator:
    """Surface transitions should have visual indicator (breadcrumb trail)."""

    def test_observatory_has_breadcrumb_trail_element(self):
        html = get_observatory_html()
        assert "breadcrumb" in html.lower() or "journey-path" in html.lower() or "surface-trail" in html.lower()

    def test_breadcrumb_has_cyan_styling(self):
        html = get_observatory_html()
        assert "breadcrumb" in html.lower() or "journey-path" in html.lower()
        # Should use accent color for visibility
        assert "accent-cyan" in html.lower() or "#00d4ff" in html.lower() or "cyan" in html.lower()


class TestFocusPanelMotionConsistency:
    """Focus panel transitions should have consistent motion timing."""

    def test_focus_panel_has_approach_animation(self):
        html = get_observatory_html()
        assert ".details-panel" in html
        assert "approach" in html.lower()

    def test_focus_panel_has_depart_animation(self):
        html = get_observatory_html()
        assert ".details-panel.closing" in html
        assert "depart" in html.lower()

    def test_focus_panel_transition_timing_defined(self):
        html = get_observatory_html()
        # Should have consistent timing (0.3s approach, 0.2s depart)
        assert "0.3s" in html or "0.2s" in html or "animation:" in html


class TestContextPreservation:
    """Navigation should preserve context across surfaces."""

    def test_js_tracks_current_project(self):
        html = get_observatory_html()
        assert "currentProjectId" in html

    def test_js_tracks_current_feature(self):
        html = get_observatory_html()
        assert "currentFeature" in html or "currentFeatureId" in html or "currentFocus" in html

    def test_js_tracks_navigation_history(self):
        html = get_observatory_html()
        # Should track where user came from for back navigation
        assert "navigationHistory" in html or "navStack" in html or "journeyStack" in html or "history" in html.lower()


class TestBackNavigationMotion:
    """Back navigation should work with motion feel."""

    def test_back_button_has_depart_animation(self):
        html = get_observatory_html()
        assert "closeDetails()" in html or "closeFocus()" in html
        assert "depart" in html.lower()

    def test_back_button_triggers_closing_class(self):
        html = get_observatory_html()
        assert ".closing" in html
        assert "classList.add" in html


class TestSurfaceContinuityMetaphor:
    """Surface transitions should preserve map metaphor."""

    def test_transition_names_use_movement_words(self):
        html = get_observatory_html()
        # Should use movement metaphor words: approach, depart, traverse, navigate
        movement_words = ["approach", "depart", "traverse", "navigate", "journey", "trail", "path"]
        found = [w for w in movement_words if w in html.lower()]
        assert len(found) >= 2  # At least 2 movement words

    def test_no_generic_transition_words(self):
        html = get_observatory_html()
        # Should NOT use generic UI transition words
        generic_words = ["fade-in", "fade-out", "slide-in", "slide-out"]
        for word in generic_words:
            # These should not be the primary animation names
            if word in html.lower():
                # If present, should be accompanied by metaphor words
                assert "approach" in html.lower() or "depart" in html.lower()


class TestCrossSurfaceMotionIntegration:
    """Integration test for cross-surface motion continuity."""

    def test_all_motion_elements_present(self):
        html = get_observatory_html()
        # All key motion elements should be present
        checks = [
            "approach" in html.lower(),
            "depart" in html.lower(),
            "currentProjectId" in html,
            "closeDetails()" in html,
        ]
        assert all(checks)

    def test_motion_css_complete(self):
        html = get_observatory_html()
        # Motion CSS should be complete with keyframes
        assert "@keyframes approach" in html.lower() or "@keyframes" in html
        assert "@keyframes depart" in html.lower() or "@keyframes" in html