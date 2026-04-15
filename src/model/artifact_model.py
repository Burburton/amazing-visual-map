"""Artifact Model for normalizing extracted artifacts.

Feature 002: Normalize artifacts into unified data model.
"""

from dataclasses import dataclass, field
from typing import Any
from pathlib import Path

from src.scanner.repo_scanner import DiscoveredArtifact


@dataclass
class ProjectArtifact:
    artifact_type: str
    artifact_id: str
    title: str
    summary: str
    source_path: Path
    parse_status: str
    project_id: str = ""
    date: str | None = None
    status: str | None = None
    feature_id: str | None = None
    relationships: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


def normalize_artifact(discovered: DiscoveredArtifact) -> ProjectArtifact:
    relationships = extract_relationships(discovered)
    
    return ProjectArtifact(
        artifact_type=discovered.artifact_type,
        artifact_id=discovered.artifact_id,
        title=discovered.title or discovered.artifact_id,
        summary=discovered.summary[:100] if discovered.summary else "",
        source_path=discovered.file_path,
        parse_status=discovered.parse_status,
        project_id=discovered.project_id,
        date=discovered.date,
        status=discovered.status,
        feature_id=discovered.feature_id,
        relationships=relationships,
        metadata=discovered.metadata,
    )


def extract_relationships(discovered: DiscoveredArtifact) -> list[str]:
    """Extract relationships from artifact metadata."""
    relationships = []
    metadata = discovered.metadata
    
    if discovered.artifact_type == "exec-pack":
        exec_id = discovered.artifact_id
        relationships.append(f"exec-result:{exec_id}")
        
        if metadata.get("feature_id"):
            relationships.append(f"feature:{metadata['feature_id']}")
    
    if discovered.artifact_type == "exec-result":
        exec_id = discovered.artifact_id
        relationships.append(f"exec-pack:{exec_id}")
        
        if metadata.get("feature_id"):
            relationships.append(f"feature:{metadata['feature_id']}")
    
    if discovered.artifact_type == "review":
        if metadata.get("feature_id"):
            relationships.append(f"feature:{metadata['feature_id']}")
    
    return relationships


def normalize_artifacts(discovered_list: list[DiscoveredArtifact]) -> list[ProjectArtifact]:
    """Normalize all discovered artifacts."""
    return [normalize_artifact(a) for a in discovered_list]


def calculate_state_summary(artifacts: list[ProjectArtifact]) -> dict[str, int]:
    active = 0
    completed = 0
    blocked = 0
    
    for artifact in artifacts:
        status = artifact.status or ""
        
        if status in ("executing", "planning", "reviewing"):
            active += 1
        elif status in ("completed", "success"):
            completed += 1
        elif status in ("blocked", "failed"):
            blocked += 1
    
    return {
        "active": active,
        "completed": completed,
        "blocked": blocked,
    }


def group_artifacts_by_project(artifacts: list[ProjectArtifact]) -> dict[str, list[ProjectArtifact]]:
    grouped: dict[str, list[ProjectArtifact]] = {}
    
    for artifact in artifacts:
        project_id = artifact.project_id or "unknown"
        if project_id not in grouped:
            grouped[project_id] = []
        grouped[project_id].append(artifact)
    
    return grouped


def get_project_summary(artifacts: list[ProjectArtifact]) -> list[dict[str, Any]]:
    grouped = group_artifacts_by_project(artifacts)
    
    summary = []
    for project_id, project_artifacts in grouped.items():
        summary.append({
            "project_id": project_id,
            "count": len(project_artifacts),
        })
    
    return sorted(summary, key=lambda x: x["project_id"])


def search_artifacts(
    artifacts: list[ProjectArtifact],
    query: str,
    artifact_type: str | None = None,
) -> list[dict[str, Any]]:
    results = []
    
    query_lower = query.lower()
    
    for artifact in artifacts:
        if artifact_type and artifact.artifact_type != artifact_type:
            continue
        
        title_match = query_lower in (artifact.title or "").lower()
        summary_match = query_lower in (artifact.summary or "").lower()
        id_match = query_lower in artifact.artifact_id.lower()
        
        if title_match or summary_match or id_match:
            results.append({
                "id": artifact.artifact_id,
                "type": artifact.artifact_type,
                "title": artifact.title,
                "summary": artifact.summary[:100] if artifact.summary else "",
                "status": artifact.status,
                "date": str(artifact.date) if artifact.date else None,
                "project_id": artifact.project_id,
            })
    
    return results[:50]