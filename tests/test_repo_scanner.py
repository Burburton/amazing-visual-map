"""Tests for Feature 001 — Repo Scanner."""

import pytest
from pathlib import Path
from src.scanner.repo_scanner import (
    DiscoveredArtifact,
    detect_project_structure,
    scan_project,
    scan_repo,
    parse_artifact,
    extract_artifact_id,
    extract_date_from_exec_id,
)


@pytest.fixture
def temp_repo(temp_dir):
    repo_path = temp_dir / "test-repo"
    repo_path.mkdir()
    yield repo_path


@pytest.fixture
def temp_project(temp_repo):
    projects_dir = temp_repo / "projects"
    projects_dir.mkdir()
    
    project_path = projects_dir / "test-project"
    project_path.mkdir()
    
    features_dir = project_path / "features"
    features_dir.mkdir()
    
    packs_dir = project_path / "execution-packs"
    packs_dir.mkdir()
    
    results_dir = project_path / "execution-results"
    results_dir.mkdir()
    
    reviews_dir = project_path / "reviews"
    reviews_dir.mkdir()
    
    yield project_path


class TestDetectProjectStructure:
    """AC1: Detect async-dev project structure (projects/<id>/)"""
    
    def test_detects_valid_project(self, temp_project):
        temp_project / "runstate.md"
        
        repo_path = temp_project.parent.parent
        projects = detect_project_structure(repo_path)
        
        assert len(projects) == 1
        assert projects[0].name == "test-project"
    
    def test_detects_project_with_features_dir(self, temp_project):
        repo_path = temp_project.parent.parent
        projects = detect_project_structure(repo_path)
        
        assert len(projects) == 1
    
    def test_ignores_non_project_dirs(self, temp_repo):
        random_dir = temp_repo / "random-dir"
        random_dir.mkdir()
        
        projects = detect_project_structure(temp_repo)
        
        assert len(projects) == 0
    
    def test_empty_repo_returns_empty(self, temp_repo):
        projects = detect_project_structure(temp_repo)
        
        assert projects == []


class TestExtractFeatureSpec:
    """AC2: Extract feature specs from features/<id>/feature-spec.yaml"""
    
    def test_extract_feature_spec(self, temp_project):
        feature_dir = temp_project / "features" / "001-test-feature"
        feature_dir.mkdir()
        
        spec_path = feature_dir / "feature-spec.yaml"
        spec_path.write_text("feature_id: 001-test-feature\nname: Test Feature\n")
        
        artifacts = scan_project(temp_project)
        
        feature_specs = [a for a in artifacts if a.artifact_type == "feature-spec"]
        assert len(feature_specs) == 1
        assert feature_specs[0].artifact_id == "001-test-feature"
        assert feature_specs[0].parse_status == "success"
    
    def test_feature_spec_partial_parse(self, temp_project):
        feature_dir = temp_project / "features" / "002-partial"
        feature_dir.mkdir()
        
        spec_path = feature_dir / "feature-spec.yaml"
        spec_path.write_text("")
        
        artifacts = scan_project(temp_project)
        
        feature_specs = [a for a in artifacts if a.artifact_type == "feature-spec"]
        assert len(feature_specs) == 1
        assert feature_specs[0].parse_status == "partial"


class TestExtractExecutionPack:
    """AC3: Extract execution packs from execution-packs/*.md"""
    
    def test_extract_exec_pack(self, temp_project):
        pack_path = temp_project / "execution-packs" / "exec-20260414-001.md"
        pack_path.write_text("```yaml\nexecution_id: exec-20260414-001\ngoal: Test\n```")
        
        artifacts = scan_project(temp_project)
        
        packs = [a for a in artifacts if a.artifact_type == "exec-pack"]
        assert len(packs) == 1
        assert packs[0].artifact_id == "exec-20260414-001"
        assert packs[0].date == "2026-04-14"
    
    def test_exec_pack_without_yaml_block(self, temp_project):
        pack_path = temp_project / "execution-packs" / "exec-20260414-002.md"
        pack_path.write_text("No YAML block here")
        
        artifacts = scan_project(temp_project)
        
        packs = [a for a in artifacts if a.artifact_type == "exec-pack"]
        assert len(packs) == 1
        assert packs[0].parse_status == "partial"


class TestExtractExecutionResult:
    """AC4: Extract execution results from execution-results/*.md"""
    
    def test_extract_exec_result(self, temp_project):
        result_path = temp_project / "execution-results" / "exec-20260414-001.md"
        result_path.write_text("```yaml\nexecution_id: exec-20260414-001\nstatus: success\n```")
        
        artifacts = scan_project(temp_project)
        
        results = [a for a in artifacts if a.artifact_type == "exec-result"]
        assert len(results) == 1
        assert results[0].status == "success"


class TestExtractReview:
    """AC5: Extract reviews from reviews/*-review.md"""
    
    def test_extract_review(self, temp_project):
        review_path = temp_project / "reviews" / "2026-04-14-review.md"
        review_path.write_text("```yaml\ndate: '2026-04-14'\ntoday_goal: Test\n```")
        
        artifacts = scan_project(temp_project)
        
        reviews = [a for a in artifacts if a.artifact_type == "review"]
        assert len(reviews) == 1
        assert reviews[0].artifact_id == "review-2026-04-14"
        assert reviews[0].date == "2026-04-14"


class TestExtractRunstate:
    """AC6: Extract runstate from runstate.md"""
    
    def test_extract_runstate(self, temp_project):
        runstate_path = temp_project / "runstate.md"
        runstate_path.write_text("```yaml\ncurrent_phase: executing\n```")
        
        artifacts = scan_project(temp_project)
        
        runstates = [a for a in artifacts if a.artifact_type == "runstate"]
        assert len(runstates) == 1
        assert runstates[0].artifact_id == "runstate"
        assert runstates[0].status == "executing"


class TestGracefulHandling:
    """AC7: Handle missing artifacts gracefully"""
    
    def test_partial_project(self, temp_repo):
        projects_dir = temp_repo / "projects"
        projects_dir.mkdir()
        
        project_path = projects_dir / "partial-project"
        project_path.mkdir()
        
        pack_path = project_path / "execution-packs"
        pack_path.mkdir()
        (pack_path / "exec-001.md").write_text("```yaml\nexecution_id: exec-001\n```")
        
        repo_path = temp_repo
        artifacts = scan_repo(repo_path, project_id="partial-project")
        
        assert len(artifacts) == 1
        assert artifacts[0].artifact_type == "exec-pack"
    
    def test_empty_project(self, temp_project):
        artifacts = scan_project(temp_project)
        
        assert artifacts == []


class TestStructuredOutput:
    """AC8: Output structured artifact list"""
    
    def test_artifact_has_required_fields(self, temp_project):
        pack_path = temp_project / "execution-packs" / "exec-20260414-001.md"
        pack_path.write_text("```yaml\nexecution_id: exec-20260414-001\ngoal: Test\nfeature_id: 001-test\n```")
        
        artifacts = scan_project(temp_project)
        
        assert len(artifacts) == 1
        artifact = artifacts[0]
        
        assert artifact.artifact_type == "exec-pack"
        assert artifact.artifact_id == "exec-20260414-001"
        assert artifact.file_path.exists()
        assert artifact.parse_status in ("success", "partial", "failed")
        assert artifact.metadata is not None


class TestScanRepo:
    """Main entry point tests"""
    
    def test_scan_all_projects(self, temp_repo):
        projects_dir = temp_repo / "projects"
        projects_dir.mkdir()
        
        for i in range(3):
            project = projects_dir / f"project-{i}"
            project.mkdir()
            (project / "runstate.md").write_text("```yaml\ncurrent_phase: planning\n```")
        
        artifacts = scan_repo(temp_repo)
        
        assert len(artifacts) == 3
        assert all(a.artifact_type == "runstate" for a in artifacts)
    
    def test_scan_with_project_filter(self, temp_repo):
        projects_dir = temp_repo / "projects"
        projects_dir.mkdir()
        
        for i in range(3):
            project = projects_dir / f"project-{i}"
            project.mkdir()
            (project / "runstate.md").write_text("```yaml\n```")
        
        artifacts = scan_repo(temp_repo, project_id="project-1")
        
        assert len(artifacts) == 1


class TestUtilityFunctions:
    def test_extract_date_from_exec_id(self):
        date = extract_date_from_exec_id("exec-20260414-001")
        assert date == "2026-04-14"
        
        date = extract_date_from_exec_id("exec-001")
        assert date is None
    
    def test_extract_artifact_id_feature_spec(self):
        path = Path("features/001-test/feature-spec.yaml")
        id = extract_artifact_id(path, "feature-spec")
        assert id == "001-test"
    
    def test_extract_artifact_id_exec_pack(self):
        path = Path("execution-packs/exec-20260414-001.md")
        id = extract_artifact_id(path, "exec-pack")
        assert id == "exec-20260414-001"
    
    def test_extract_artifact_id_review(self):
        path = Path("reviews/2026-04-14-review.md")
        id = extract_artifact_id(path, "review")
        assert id == "review-2026-04-14"