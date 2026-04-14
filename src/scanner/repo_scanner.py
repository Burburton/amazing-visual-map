"""Repo Scanner for async-dev repositories.

Feature 001: Scan async-dev repo and extract canonical artifacts.
"""

from pathlib import Path
from dataclasses import dataclass, field
from typing import Any
import yaml
import re


@dataclass
class DiscoveredArtifact:
    artifact_type: str
    artifact_id: str
    file_path: Path
    parse_status: str
    project_id: str = ""
    title: str = ""
    summary: str = ""
    date: str | None = None
    status: str | None = None
    feature_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


ARTIFACT_PATTERNS = {
    "feature-spec": r"^features/.*/feature-spec\.yaml$",
    "exec-pack": r"^execution-packs/exec-.+\.md$",
    "exec-result": r"^execution-results/exec-.+\.md$",
    "review": r"^reviews/.+-review\.md$",
    "runstate": r"^runstate\.md$",
}


def detect_project_structure(repo_path: Path) -> list[Path]:
    projects_dir = repo_path / "projects"
    
    if not projects_dir.exists():
        return []
    
    project_paths = []
    for item in projects_dir.iterdir():
        if item.is_dir():
            has_structure = any([
                (item / "runstate.md").exists(),
                (item / "features").exists(),
                (item / "execution-packs").exists(),
                (item / "execution-results").exists(),
                (item / "reviews").exists(),
            ])
            if has_structure:
                project_paths.append(item)
    
    return project_paths


def scan_project(project_path: Path) -> list[DiscoveredArtifact]:
    artifacts = []
    project_id = project_path.name
    
    for artifact_type, pattern in ARTIFACT_PATTERNS.items():
        discovered = discover_artifacts_by_type(project_path, artifact_type, pattern, project_id)
        artifacts.extend(discovered)
    
    return artifacts


def discover_artifacts_by_type(
    project_path: Path, 
    artifact_type: str, 
    pattern: str,
    project_id: str = "",
) -> list[DiscoveredArtifact]:
    artifacts = []
    regex = re.compile(pattern)
    
    for file_path in project_path.rglob("*"):
        if file_path.is_file():
            relative = str(file_path.relative_to(project_path)).replace("\\", "/")
            if regex.match(relative):
                artifact = parse_artifact(file_path, artifact_type, project_id)
                artifacts.append(artifact)
    
    return artifacts


def parse_artifact(file_path: Path, artifact_type: str, project_id: str = "") -> DiscoveredArtifact:
    artifact_id = extract_artifact_id(file_path, artifact_type)
    
    try:
        if file_path.suffix == ".yaml":
            content = parse_yaml_file(file_path)
        elif file_path.suffix == ".md":
            content = parse_markdown_file(file_path)
        else:
            content = {}
        
        parse_status = "success"
        
        if not content:
            parse_status = "partial"
        
    except Exception:
        content = {}
        parse_status = "failed"
    
    return DiscoveredArtifact(
        artifact_type=artifact_type,
        artifact_id=artifact_id,
        file_path=file_path,
        parse_status=parse_status,
        project_id=project_id,
        title=content.get("name", "") or content.get("goal", "") or artifact_id,
        summary=content.get("description", "") or content.get("today_goal", "") or "",
        date=content.get("date") or extract_date_from_exec_id(artifact_id),
        status=content.get("status") or content.get("current_phase"),
        feature_id=content.get("feature_id"),
        metadata=content,
    )


def extract_artifact_id(file_path: Path, artifact_type: str) -> str:
    """Extract artifact ID from file path or content."""
    stem = file_path.stem
    
    if artifact_type == "feature-spec":
        parent = file_path.parent.name
        return parent
    
    if artifact_type in ("exec-pack", "exec-result"):
        return stem
    
    if artifact_type == "review":
        date_match = re.match(r"(\d{4}-\d{2}-\d{2})", stem)
        if date_match:
            return f"review-{date_match.group(1)}"
        return stem
    
    if artifact_type == "runstate":
        return "runstate"
    
    return stem


def extract_date_from_exec_id(exec_id: str) -> str | None:
    """Extract date from execution ID (exec-YYYYMMDD-###)."""
    match = re.match(r"exec-(\d{4})(\d{2})(\d{2})", exec_id)
    if match:
        year, month, day = match.groups()
        return f"{year}-{month}-{day}"
    return None


def parse_yaml_file(file_path: Path) -> dict[str, Any]:
    """Parse YAML file and return content."""
    with open(file_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def parse_markdown_file(file_path: Path) -> dict[str, Any]:
    """Parse markdown file and extract YAML block.
    
    Async-dev artifacts use fenced YAML blocks.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    yaml_block_match = re.search(r"```yaml\s*(.*?)\s*```", content, re.DOTALL)
    if yaml_block_match:
        yaml_content = yaml_block_match.group(1)
        return yaml.safe_load(yaml_content) or {}
    
    return {}


def scan_repo(repo_path: Path, project_id: str | None = None) -> list[DiscoveredArtifact]:
    """Main entry point: scan repo and return all artifacts.
    
    Input: repo_path (Path), optional project_id filter
    Output: list of DiscoveredArtifact
    """
    projects = detect_project_structure(repo_path)
    
    if project_id:
        projects = [p for p in projects if p.name == project_id]
    
    all_artifacts = []
    for project in projects:
        artifacts = scan_project(project)
        all_artifacts.extend(artifacts)
    
    return all_artifacts