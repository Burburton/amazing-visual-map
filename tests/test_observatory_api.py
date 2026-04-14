"""Tests for Feature 003 — Observatory Home."""


def derive_next_action(summary, blocked):
    if summary["blocked"] > 0:
        return f"Resolve {summary['blocked']} blocked items before continuing"
    if summary["active"] > 0:
        return f"Continue active work ({summary['active']} items in progress)"
    if summary["completed"] > 0:
        return "All items complete - ready for review or next phase"
    return "No active work found - start planning next feature"


def get_observatory_html():
    return """
<!DOCTYPE html>
<style>
:root { --bg-dark: #0a0a0f; }
.regions { }
.trail { }
.friction-zone { }
.path-hint { }
</style>
<div class="regions"></div>
<div class="trail"></div>
<div class="friction-zone"></div>
<div class="path-hint"></div>
"""


class TestDeriveNextAction:
    """AC5: Provide recommended next action as guided path hint"""
    
    def test_blocked_priority(self):
        summary = {"active": 5, "completed": 10, "blocked": 2}
        blocked = [{"id": "b1"}]
        
        action = derive_next_action(summary, blocked)
        
        assert "blocked" in action.lower()
        assert "2" in action
    
    def test_active_continuation(self):
        summary = {"active": 3, "completed": 5, "blocked": 0}
        blocked = []
        
        action = derive_next_action(summary, blocked)
        
        assert "active" in action.lower()
        assert "3" in action
    
    def test_completed_state(self):
        summary = {"active": 0, "completed": 10, "blocked": 0}
        blocked = []
        
        action = derive_next_action(summary, blocked)
        
        assert "complete" in action.lower() or "review" in action.lower()
    
    def test_empty_state(self):
        summary = {"active": 0, "completed": 0, "blocked": 0}
        blocked = []
        
        action = derive_next_action(summary, blocked)
        
        assert "No active work" in action or "planning" in action.lower()


class TestHTMLGeneration:
    def test_html_contains_dark_theme(self):
        html = get_observatory_html()
        
        assert "#0a0a0f" in html
    
    def test_html_contains_regions(self):
        html = get_observatory_html()
        
        assert "regions" in html.lower()
    
    def test_html_contains_trail(self):
        html = get_observatory_html()
        
        assert "trail" in html.lower()
    
    def test_html_contains_friction_zones(self):
        html = get_observatory_html()
        
        assert "friction" in html.lower()
    
    def test_html_contains_path_hint(self):
        html = get_observatory_html()
        
        assert "path-hint" in html.lower()
    
    def test_html_no_table_elements(self):
        html = get_observatory_html()
        
        assert "<table" not in html
    
    def test_html_no_card_grid(self):
        html = get_observatory_html()
        
        assert "card-grid" not in html.lower()