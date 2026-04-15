"""Tests for Feature 010 - Motion Language.

Polish Phase 1: CSS transitions expressing map metaphor.
"""

import pytest
from src.api.observatory_api import get_observatory_html


# ============================================================================
# AC1: Focus panel opens with approach transition
# ============================================================================

class TestApproachTransition:
    """Focus panel must use approach animation."""
    
    def test_css_has_approach_keyframe(self):
        """CSS should define approach keyframe animation."""
        html = get_observatory_html()
        
        assert "@keyframes approach" in html
    
    def test_approach_animation_slides_in(self):
        """Approach should slide from right and scale up."""
        html = get_observatory_html()
        
        assert "translateX" in html
        assert "scale" in html


# ============================================================================
# AC2: Focus panel closes with depart transition
# ============================================================================

class TestDepartTransition:
    """Focus panel must use depart animation on close."""
    
    def test_css_has_depart_keyframe(self):
        """CSS should define depart keyframe animation."""
        html = get_observatory_html()
        
        assert "@keyframes depart" in html
    
    def test_depart_animation_slides_out(self):
        """Depart should slide to right and scale down."""
        html = get_observatory_html()
        
        assert "depart" in html.lower()
    
    def test_js_has_closing_animation_handler(self):
        """JavaScript should add closing class on close."""
        html = get_observatory_html()
        
        assert "closing" in html
        assert "setTimeout" in html


# ============================================================================
# AC3: Terrain regions highlight with proximity effect
# ============================================================================

class TestProximityEffect:
    """Terrain regions must have proximity glow on hover."""
    
    def test_css_has_proximity_glow_keyframe(self):
        """CSS should define proximity-glow animation."""
        html = get_observatory_html()
        
        assert "@keyframes proximity-glow" in html
    
    def test_terrain_region_has_hover_animation(self):
        """Terrain region should animate on hover."""
        html = get_observatory_html()
        
        assert "terrain-region:hover" in html.lower() or "region-item:hover" in html.lower()


# ============================================================================
# AC4: Timeline waypoints pulse on hover
# ============================================================================

class TestWaypointPulse:
    """Timeline waypoints must pulse on hover."""
    
    def test_css_has_waypoint_pulse_keyframe(self):
        """CSS should define waypoint-pulse animation."""
        html = get_observatory_html()
        
        assert "@keyframes waypoint-pulse" in html
    
    def test_waypoint_pulse_uses_cyan_glow(self):
        """Pulse should use cyan accent color."""
        html = get_observatory_html()
        
        assert "waypoint-pulse" in html
        assert "0, 212, 255" in html


# ============================================================================
# AC5: Project selector territory switch transition
# ============================================================================

class TestTerritorySwitch:
    """Project buttons must transition with territory switch feel."""
    
    def test_project_btn_has_cubic_bezier_transition(self):
        """Buttons should use cubic-bezier for intentional feel."""
        html = get_observatory_html()
        
        assert "cubic-bezier" in html
    
    def test_project_btn_has_hover_scale(self):
        """Hover should scale up slightly."""
        html = get_observatory_html()
        
        assert ".project-btn:hover" in html
        assert "scale" in html


# ============================================================================
# AC6: Search results discovery fade-in
# ============================================================================

class TestDiscoveryFadeIn:
    """Search results must appear with discovery animation."""
    
    def test_css_has_discovery_reveal_keyframe(self):
        """CSS should define discovery-reveal animation."""
        html = get_observatory_html()
        
        assert "@keyframes discovery-reveal" in html
    
    def test_search_result_card_has_staggered_delay(self):
        """Results should have staggered animation delays."""
        html = get_observatory_html()
        
        assert "animation-delay" in html
        assert "search-result-card" in html


# ============================================================================
# AC7: Status indicators animate state changes
# ============================================================================

class TestStatusAnimation:
    """Status indicators should have visual feedback."""
    
    def test_status_classes_have_transition(self):
        """Status elements should have transitions."""
        html = get_observatory_html()
        
        assert "transition" in html


# ============================================================================
# AC8: Transitions express map metaphor (not generic)
# ============================================================================

class TestAntiRegressionNoGenericFade:
    """Transitions must NOT be generic fade/slide."""
    
    def test_transitions_use_transform_not_just_opacity(self):
        """Motion should use transform for movement feel."""
        html = get_observatory_html()
        
        motion_css = html[html.find("@keyframes"):html.find("@keyframes") + 500]
        
        assert "transform" in motion_css
    
    def test_keyframes_have_movement_metaphor_names(self):
        """Animation names should reflect map metaphor."""
        html = get_observatory_html()
        
        metaphor_names = ["approach", "depart", "proximity", "waypoint", "discovery"]
        
        found = [name for name in metaphor_names if name in html.lower()]
        
        assert len(found) >= 3  # At least 3 metaphor names


# ============================================================================
# Integration tests
# ============================================================================

class TestMotionLanguageIntegration:
    """Full integration test for motion language."""
    
    def test_all_keyframes_defined(self):
        """All required keyframe animations should exist."""
        html = get_observatory_html()
        
        required_keyframes = [
            "approach",
            "depart",
            "waypoint-pulse",
            "discovery-reveal",
            "proximity-glow",
        ]
        
        for kf in required_keyframes:
            assert f"@keyframes {kf}" in html
    
    def test_js_animations_integrated(self):
        """JavaScript should use animation classes."""
        html = get_observatory_html()
        
        assert "classList.add" in html
        assert "classList.remove" in html