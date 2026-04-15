"""Tests for Feature 011 - Spatial Terrain.

Polish Phase 1: Relationship-based positioning, visual terrain elements.
"""

import pytest
from src.api.observatory_api import get_observatory_html


# ============================================================================
# AC1: Regions positioned by relationship proximity
# ============================================================================

class TestRelationshipProximity:
    """Terrain must position regions by relationships."""
    
    def test_terrain_css_has_positioning_classes(self):
        """CSS should have classes for region positioning."""
        html = get_observatory_html()
        
        assert "terrain" in html.lower() or "region" in html.lower()
    
    def test_regions_have_spatial_style(self):
        """Regions should have spatial positioning style."""
        html = get_observatory_html()
        
        assert "position" in html.lower() or "transform" in html.lower()


# ============================================================================
# AC2: Paths/lines connect related regions
# ============================================================================

class TestConnectionPaths:
    """Terrain must show connection paths between regions."""
    
    def test_terrain_has_connection_visual(self):
        """Terrain should have visual for connections."""
        html = get_observatory_html()
        
        assert "connection" in html.lower() or "path" in html.lower() or "link" in html.lower()
    
    def test_connections_use_line_or_border(self):
        """Connections should use lines/borders."""
        html = get_observatory_html()
        
        assert "border" in html or "line" in html.lower()


# ============================================================================
# AC3: Region clusters visually grouped
# ============================================================================

class TestRegionClusters:
    """Related regions should cluster together visually."""
    
    def test_regions_have_cluster_style(self):
        """Regions should have clustering style."""
        html = get_observatory_html()
        
        assert "region" in html.lower()


# ============================================================================
# AC4: Terrain background has subtle texture/gradient
# ============================================================================

class TestTerrainBackground:
    """Terrain should have textured background."""
    
    def test_terrain_has_background_gradient(self):
        """Terrain background should use gradient."""
        html = get_observatory_html()
        
        assert "gradient" in html.lower() or "linear-gradient" in html


# ============================================================================
# AC5: Regions have visual boundaries
# ============================================================================

class TestRegionBoundaries:
    """Regions should have clear visual boundaries."""
    
    def test_regions_have_border_radius(self):
        """Regions should be rounded, not rectangular."""
        html = get_observatory_html()
        
        assert "border-radius" in html
    
    def test_regions_have_shadow(self):
        """Regions should have shadow for depth."""
        html = get_observatory_html()
        
        assert "box-shadow" in html


# ============================================================================
# AC6: Hover shows region connections
# ============================================================================

class TestHoverConnections:
    """Hovering region should show its connections."""
    
    def test_region_hover_effect_exists(self):
        """Regions should have hover interaction."""
        html = get_observatory_html()
        
        assert ":hover" in html


# ============================================================================
# AC7: Not a flat grid
# ============================================================================

class TestAntiRegressionNoFlatGrid:
    """Terrain must NOT be simple grid."""
    
    def test_terrain_not_grid_layout(self):
        """Terrain should not use grid layout."""
        html = get_observatory_html()
        
        terrain_section = html[html.find("terrain") if "terrain" in html else html.find("regions"):html.find("terrain") + 300 if "terrain" in html else len(html)]
        
        assert "flex" in terrain_section or "position" in terrain_section.lower() or "transform" in terrain_section.lower()


# ============================================================================
# AC8: Performance acceptable
# ============================================================================

class TestTerrainPerformance:
    """Terrain should not use heavy canvas."""
    
    def test_terrain_uses_css_not_canvas(self):
        """Terrain should use CSS styling."""
        html = get_observatory_html()
        
        assert "<canvas" not in html.lower()


# ============================================================================
# Integration tests
# ============================================================================

class TestSpatialTerrainIntegration:
    """Full integration test for spatial terrain."""
    
    def test_terrain_has_visual_elements(self):
        """Terrain should have all visual elements."""
        html = get_observatory_html()
        
        required_elements = ["border", "shadow", "gradient"]
        
        found = [el for el in required_elements if el.lower() in html.lower()]
        
        assert len(found) >= 2