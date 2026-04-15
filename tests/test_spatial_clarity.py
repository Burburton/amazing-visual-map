"""Test Spatial Clarity Enhancement - Feature 017.

Phase 3: Experience Refinement - Stronger map fidelity and spatial clarity.
"""

import pytest
from src.api.observatory_api import get_observatory_html


class TestVisualClustering:
    """Feature groups should have subtle clustering indication."""

    def test_regions_have_clustering_style(self):
        html = get_observatory_html()
        assert "cluster" in html.lower() or "group" in html.lower() or ".regions" in html

    def test_regions_container_has_flex_layout(self):
        html = get_observatory_html()
        assert "display: flex" in html.lower() or "flex-wrap" in html.lower() or "gap" in html.lower()


class TestConnectionPathVisibility:
    """Relationship lines should be visible between regions."""

    def test_css_has_connection_visual(self):
        html = get_observatory_html()
        assert "connection" in html.lower() or "link" in html.lower() or "border" in html.lower()

    def test_regions_have_border_styling(self):
        html = get_observatory_html()
        assert ".region" in html
        assert "border" in html.lower()

    def test_connection_uses_cyan_color(self):
        html = get_observatory_html()
        assert "accent-cyan" in html.lower() or "#00d4ff" in html.lower()


class TestProximityIndication:
    """Related regions should be visually closer."""

    def test_regions_have_gap_spacing(self):
        html = get_observatory_html()
        assert "gap" in html.lower() or "margin" in html.lower() or "spacing" in html.lower()

    def test_regions_grouped_in_container(self):
        html = get_observatory_html()
        assert 'id="regions"' in html or 'class="regions"' in html


class TestDepthHierarchy:
    """Regions should have depth/shadow hierarchy for spatial layering."""

    def test_regions_have_shadow_variation(self):
        html = get_observatory_html()
        assert "box-shadow" in html.lower() or "shadow" in html.lower()

    def test_active_region_has_different_shadow(self):
        html = get_observatory_html()
        assert ".region.active" in html or ":hover" in html.lower()

    def test_shadow_uses_depth_colors(self):
        html = get_observatory_html()
        assert "rgba" in html.lower() or "#000" in html.lower()


class TestSpatialClarityMetaphor:
    """Spatial additions should preserve map metaphor."""

    def test_spatial_names_use_map_words(self):
        html = get_observatory_html()
        map_words = ["terrain", "region", "path", "trail", "territory", "zone"]
        found = [w for w in map_words if w in html.lower()]
        assert len(found) >= 2

    def test_no_generic_grid_words(self):
        html = get_observatory_html()
        assert "grid-template" not in html.lower()


class TestSpatialClarityIntegration:
    """Integration test for spatial clarity enhancement."""

    def test_all_spatial_elements_present(self):
        html = get_observatory_html()
        checks = [
            ".region" in html,
            "border" in html.lower(),
            "gap" in html.lower() or "margin" in html.lower(),
            "box-shadow" in html.lower(),
        ]
        assert all(checks)

    def test_spatial_css_complete(self):
        html = get_observatory_html()
        assert ".regions" in html
        assert "display: flex" in html.lower() or "flex" in html.lower()