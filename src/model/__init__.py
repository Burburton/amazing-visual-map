"""Model package for artifact normalization."""

from src.model.artifact_model import (
    ProjectArtifact,
    normalize_artifact,
    normalize_artifacts,
    extract_relationships,
    calculate_state_summary,
)

__all__ = [
    "ProjectArtifact",
    "normalize_artifact",
    "normalize_artifacts",
    "extract_relationships",
    "calculate_state_summary",
]