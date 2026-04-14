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
    date: str | None = None
    status: str | None = None
    feature_id: str | None = None
    relationships: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


def normalize_artifact(discovered: DiscoveredArtifact) -> ProjectArtifact:
    """Normalize discovered artifact into unified model."""
    relationships = extract_relationships(discovered)
    
    return ProjectArtifact(
        artifact_type=discovered.artifact_type,
        artifact_id=discovered.artifact_id,
        title=discovered.title or discovered.artifact_id,
        summary=discovered.summary[:100] if discovered.summary else "",
        source_path=discovered.file_path,
        parse_status=discovered.parse_status,
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
    """Calculate minimal state summary.
    
    Returns counts for active, completed, blocked states.
    """
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