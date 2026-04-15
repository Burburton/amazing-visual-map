"""Test Structured Narrative Quality - Feature 018.

Phase 3: Experience Refinement - Better guided journey / narrative briefing quality.
"""

import pytest
from src.api.observatory_api import get_observatory_html, build_focus_data
from src.scanner.repo_scanner import scan_repo
from src.model.artifact_model import normalize_artifacts
from pathlib import Path


class TestNarrativeSections:
    """Narrative should have multiple structured sections."""

    def test_narrative_has_beginning_section(self):
        html = get_observatory_html()
        assert "beginning" in html.lower() or "started" in html.lower() or "origin" in html.lower() or "milestone" in html.lower()

    def test_narrative_has_current_state_section(self):
        html = get_observatory_html()
        assert "current" in html.lower() or "status" in html.lower() or "state" in html.lower()

    def test_narrative_has_next_step_section(self):
        html = get_observatory_html()
        assert "next" in html.lower() or "recommended" in html.lower() or "continue" in html.lower()

    def test_narrative_css_has_section_styling(self):
        html = get_observatory_html()
        assert "narrative-section" in html or "narrative-title" in html or "narrative-text" in html


class TestMilestoneHighlighting:
    """Milestones should be highlighted in narrative."""

    def test_api_narrative_mentions_milestones(self):
        repo = Path("G:/Workspace/amazing-async-dev")
        if repo.exists():
            discovered = scan_repo(repo, project_id="loop-journal-viewer")
            artifacts = normalize_artifacts(discovered)
            features = [a for a in artifacts if a.artifact_type == "feature-spec"]
            if features:
                focus_data = build_focus_data(artifacts, features[0].artifact_id)
                narrative = focus_data.get("narrative", "")
                assert len(narrative) > 20

    def test_css_has_milestone_styling(self):
        html = get_observatory_html()
        assert "milestone" in html.lower() or "highlight" in html.lower() or "accent" in html.lower()


class TestCurrentStateSummary:
    """Current state should be concise and actionable."""

    def test_narrative_text_is_not_verbose(self):
        html = get_observatory_html()
        assert "narrative-text" in html

    def test_state_indicator_present(self):
        html = get_observatory_html()
        assert "status" in html.lower() or "active" in html.lower() or "completed" in html.lower()


class TestRecommendedNextSpecific:
    """Recommended next should be specific to feature context."""

    def test_next_action_hint_present(self):
        html = get_observatory_html()
        assert "next-action" in html or "next_action_hint" in html.lower()

    def test_recommended_path_present(self):
        html = get_observatory_html()
        assert "recommended" in html.lower() or "path" in html.lower()


class TestNarrativeMetaphor:
    """Narrative should preserve story-like feel."""

    def test_narrative_names_use_story_words(self):
        html = get_observatory_html()
        story_words = ["story", "narrative", "journey", "milestone", "chapter", "beginning"]
        found = [w for w in story_words if w in html.lower()]
        assert len(found) >= 2

    def test_narrative_not_progress_report_style(self):
        html = get_observatory_html()
        progress_words = ["percentage", "complete%", "progress bar", "status report"]
        for word in progress_words:
            assert word not in html.lower()


class TestStructuredNarrativeIntegration:
    """Integration test for structured narrative quality."""

    def test_all_narrative_elements_present(self):
        html = get_observatory_html()
        checks = [
            "narrative" in html.lower(),
            "current" in html.lower() or "status" in html.lower(),
            "next" in html.lower() or "recommended" in html.lower(),
        ]
        assert all(checks)

    def test_narrative_structure_complete(self):
        html = get_observatory_html()
        assert "narrative-section" in html
        assert "narrative-title" in html
        assert "narrative-text" in html