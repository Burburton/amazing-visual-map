"""Observatory API - serves artifact data for frontend.

Feature 003: Observatory Home backend.
"""

from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

from src.scanner.repo_scanner import scan_repo
from src.model.artifact_model import (
    normalize_artifacts,
    calculate_state_summary,
    get_project_summary,
    search_artifacts,
)


app = FastAPI(title="Amazing Visual Map Observatory")


@app.get("/api/project/{project_id}")
async def get_project_state(project_id: str, repo_path: str = "."):
    repo = Path(repo_path)
    
    if not repo.exists():
        raise HTTPException(status_code=404, detail="Repository not found")
    
    discovered = scan_repo(repo, project_id=project_id)
    artifacts = normalize_artifacts(discovered)
    summary = calculate_state_summary(artifacts)
    
    features = [a for a in artifacts if a.artifact_type == "feature-spec"]
    recent = sorted(
        [a for a in artifacts if a.date],
        key=lambda x: x.date or "",
        reverse=True
    )[:10]
    blocked = [a for a in artifacts if a.status in ("blocked", "failed")]
    
    return {
        "project_id": project_id,
        "summary": summary,
        "features": [
            {
                "id": f.artifact_id,
                "title": f.title,
                "status": f.status,
            }
            for f in features
        ],
        "recent_movement": [
            {
                "id": r.artifact_id,
                "type": r.artifact_type,
                "date": r.date,
                "title": r.title,
            }
            for r in recent
        ],
        "friction_zones": [
            {
                "id": b.artifact_id,
                "type": b.artifact_type,
                "status": b.status,
                "title": b.title,
            }
            for b in blocked
        ],
        "next_action_hint": derive_next_action(summary, blocked),
    }


@app.get("/api/projects")
async def get_projects(repo_path: str = "."):
    repo = Path(repo_path)
    
    if not repo.exists():
        raise HTTPException(status_code=404, detail="Repository not found")
    
    discovered = scan_repo(repo)
    artifacts = normalize_artifacts(discovered)
    summary = get_project_summary(artifacts)
    
    return summary


@app.get("/api/timeline/{project_id}")
async def get_timeline(project_id: str, repo_path: str = "."):
    repo = Path(repo_path)
    
    if not repo.exists():
        raise HTTPException(status_code=404, detail="Repository not found")
    
    discovered = scan_repo(repo, project_id=project_id)
    artifacts = normalize_artifacts(discovered)
    
    events = build_timeline_events(artifacts)
    
    return {
        "project_id": project_id,
        "events": events,
    }


@app.get("/api/terrain/{project_id}")
async def get_terrain(project_id: str, repo_path: str = "."):
    repo = Path(repo_path)
    
    if not repo.exists():
        raise HTTPException(status_code=404, detail="Repository not found")
    
    discovered = scan_repo(repo, project_id=project_id)
    artifacts = normalize_artifacts(discovered)
    
    terrain = build_terrain_data(artifacts)
    
    return terrain


def build_terrain_data(artifacts) -> dict:
    features = [a for a in artifacts if a.artifact_type == "feature-spec"]
    
    regions = []
    connections = []
    
    row = 0
    col = 0
    grid_cols = 3
    
    for i, feature in enumerate(features):
        position = {"row": row, "col": col}
        
        regions.append({
            "id": feature.artifact_id,
            "name": feature.title,
            "status": feature.status or "active",
            "position": position,
        })
        
        related = [a for a in artifacts if a.feature_id == feature.artifact_id and a.artifact_type != "feature-spec"]
        for rel in related:
            connections.append({
                "from": feature.artifact_id,
                "to": rel.artifact_id,
                "type": rel.artifact_type,
            })
        
        col += 1
        if col >= grid_cols:
            col = 0
            row += 1
    
    return {
        "project_id": artifacts[0].project_id if artifacts else "unknown",
        "regions": regions,
        "connections": connections,
    }


@app.get("/api/search")
async def search(q: str = "", type: str | None = None, repo_path: str = "."):
    repo = Path(repo_path)
    
    if not repo.exists():
        raise HTTPException(status_code=404, detail="Repository not found")
    
    if not q:
        return {"results": [], "total": 0, "query": ""}
    
    discovered = scan_repo(repo)
    artifacts = normalize_artifacts(discovered)
    
    results = search_artifacts(artifacts, query=q, artifact_type=type)
    
    return {
        "results": results,
        "total": len(results),
        "query": q,
        "type_filter": type,
    }


@app.get("/api/focus/{project_id}/{feature_id}")
async def get_focus(project_id: str, feature_id: str, repo_path: str = "."):
    repo = Path(repo_path)
    
    if not repo.exists():
        raise HTTPException(status_code=404, detail="Repository not found")
    
    discovered = scan_repo(repo, project_id=project_id)
    artifacts = normalize_artifacts(discovered)
    
    focus = build_focus_data(artifacts, feature_id)
    
    if not focus:
        raise HTTPException(status_code=404, detail="Feature not found")
    
    return focus


def build_focus_data(artifacts, feature_id: str) -> dict | None:
    features = [a for a in artifacts if a.artifact_type == "feature-spec" and a.artifact_id == feature_id]
    
    if not features:
        return None
    
    feature = features[0]
    
    # Extract feature number (e.g., "001-init" -> 1, matching YAML integer parsing)
    feature_num_str = feature_id.split("-")[0] if "-" in feature_id else feature_id
    try:
        feature_num_int = int(feature_num_str)
    except ValueError:
        feature_num_int = None
    
    # Match by feature_id field (integer from YAML) or by artifact_id prefix
    related = [a for a in artifacts 
               if a.artifact_type != "feature-spec" 
               and (a.feature_id == feature_num_int or 
                    str(a.feature_id) == feature_num_str or
                    a.feature_id == feature_id)]
    
    timeline = build_timeline_events(related)
    
    narrative = generate_narrative(related)
    
    related_features = [a for a in artifacts 
                        if a.artifact_type == "feature-spec" 
                        and a.artifact_id != feature_id]
    
    return {
        "feature": {
            "id": feature.artifact_id,
            "name": feature.title,
            "status": feature.status or "active",
            "goal": feature.summary,
            "metadata": feature.metadata,
        },
        "related_artifacts": [
            {
                "id": a.artifact_id,
                "type": a.artifact_type,
                "date": str(a.date) if a.date else None,
                "status": a.status,
            }
            for a in related
        ],
        "related_features": [
            {
                "id": a.artifact_id,
                "name": a.title,
                "status": a.status or "active",
            }
            for a in related_features[:5]
        ],
        "timeline": timeline,
        "narrative": narrative,
    }


def generate_narrative(artifacts) -> str:
    if not artifacts:
        return "No execution history recorded for this feature."
    
    def get_date(a):
        if hasattr(a, 'date'):
            return a.date
        return a.get('date')
    
    def get_status(a):
        if hasattr(a, 'status'):
            return a.status or ""
        return a.get('status', '')
    
    def get_id(a):
        if hasattr(a, 'artifact_id'):
            return a.artifact_id
        return a.get('id', 'unknown')
    
    dated_artifacts = [a for a in artifacts if get_date(a)]
    sorted_artifacts = sorted(dated_artifacts, key=lambda x: str(get_date(x) or ""))
    
    if not sorted_artifacts:
        return "Execution history exists but dates are not recorded."
    
    first = sorted_artifacts[0]
    last = sorted_artifacts[-1]
    
    milestones = []
    for a in sorted_artifacts:
        status = get_status(a)
        date_str = str(get_date(a))
        if status in ("completed", "success"):
            milestones.append(f"Completed execution on {date_str}")
        elif status == "blocked":
            milestones.append(f"Blocked on {date_str}")
        elif status == "planning":
            milestones.append(f"Planning phase on {date_str}")
    
    total_runs = len(sorted_artifacts)
    first_date = str(get_date(first))
    first_id = get_id(first)
    first_status = get_status(first)
    last_status = get_status(last)
    last_date = str(get_date(last))
    
    beginning = f"This feature began with {first_id} on {first_date}."
    
    if total_runs > 1:
        middle = f"Through {total_runs} iterations, the feature progressed from {first_status or 'unknown'} to {last_status or 'active'}."
    else:
        middle = "Currently in initial development phase."
    
    if milestones:
        current = f"Key milestones: {', '.join(milestones[:3])}."
    else:
        current = f"Current state: {last_status or 'in progress'} as of {last_date}."
    
    return f"{beginning} {middle} {current}"


def build_timeline_events(artifacts) -> list[dict]:
    from datetime import datetime, timedelta, date
    
    now = datetime.now()
    recent_threshold = now - timedelta(days=7)
    
    dated_artifacts = [a for a in artifacts if a.date]
    sorted_artifacts = sorted(dated_artifacts, key=lambda x: str(x.date or ""), reverse=True)
    
    events = []
    for artifact in sorted_artifacts:
        is_recent = False
        if artifact.date:
            try:
                date_str = str(artifact.date) if isinstance(artifact.date, date) else artifact.date
                artifact_date = datetime.strptime(date_str, "%Y-%m-%d")
                is_recent = artifact_date >= recent_threshold
            except ValueError:
                pass
        
        events.append({
            "id": artifact.artifact_id,
            "type": artifact.artifact_type,
            "date": str(artifact.date) if artifact.date else None,
            "title": artifact.title,
            "status": artifact.status,
            "is_recent": is_recent,
        })
    
    return events


def derive_next_action(summary: dict, blocked: list) -> str:
    if summary["blocked"] > 0:
        return f"Resolve {summary['blocked']} blocked items before continuing"
    
    if summary["active"] > 0:
        return f"Continue active work ({summary['active']} items in progress)"
    
    if summary["completed"] > 0:
        return "All items complete - ready for review or next phase"
    
    return "No active work found - start planning next feature"


@app.get("/", response_class=HTMLResponse)
async def observatory_home():
    return HTMLResponse(content=get_observatory_html())


def get_observatory_html() -> str:
    """Return observatory HTML with dark theme and map-like visualization."""
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Amazing Visual Map - Observatory</title>
    <style>
        :root {
            --bg-dark: #0a0a0f;
            --bg-region: #16161f;
            --accent-cyan: #00d4ff;
            --accent-green: #00ff88;
            --accent-yellow: #ffd700;
            --accent-red: #ff4444;
            --text-primary: #ffffff;
            --text-secondary: #888899;
        }
        
        * { box-sizing: border-box; margin: 0; padding: 0; }
        
        body {
            font-family: 'Segoe UI', system-ui, sans-serif;
            background: var(--bg-dark);
            color: var(--text-primary);
            min-height: 100vh;
        }
        
        .observatory {
            max-width: 1200px;
            margin: 0 auto;
            padding: 40px 20px;
        }
        
        .header {
            text-align: center;
            margin-bottom: 60px;
        }
        
        .header h1 {
            font-size: 2.5rem;
            font-weight: 300;
            letter-spacing: 0.1em;
            color: var(--accent-cyan);
        }
        
        .pulse {
            display: flex;
            justify-content: center;
            gap: 30px;
            margin-top: 20px;
        }
        
        .pulse-item {
            text-align: center;
        }
        
        .pulse-value {
            font-size: 2rem;
            font-weight: 700;
        }
        
        .pulse-label {
            font-size: 0.8rem;
            color: var(--text-secondary);
            margin-top: 5px;
        }
        
        .pulse-active { color: var(--accent-cyan); }
        .pulse-completed { color: var(--accent-green); }
        .pulse-blocked { color: var(--accent-red); }
        
        .project-selector {
            display: flex;
            justify-content: center;
            gap: 10px;
            margin-top: 20px;
            flex-wrap: wrap;
        }
        
        .project-btn {
            background: var(--bg-region);
            border: 1px solid #222233;
            color: var(--text-secondary);
            padding: 8px 16px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 0.85rem;
            transition: all 0.2s ease;
        }
        
        .project-btn:hover {
            border-color: var(--accent-cyan);
            color: var(--accent-cyan);
        }
        
        .project-btn.active {
            border-color: var(--accent-cyan);
            color: var(--accent-cyan);
            background: rgba(0, 212, 255, 0.1);
        }
        
        .search-container {
            display: flex;
            justify-content: center;
            gap: 10px;
            margin-top: 15px;
        }
        
        .search-input {
            background: var(--bg-region);
            border: 1px solid #222233;
            color: var(--text-primary);
            padding: 10px 20px;
            border-radius: 4px;
            width: 300px;
            font-size: 0.9rem;
        }
        
        .search-input:focus {
            border-color: var(--accent-cyan);
            outline: none;
        }
        
        .search-btn {
            background: var(--accent-cyan);
            border: none;
            color: var(--bg-dark);
            padding: 10px 20px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 0.9rem;
        }
        
        .search-results {
            max-width: 800px;
            margin: 20px auto;
        }
        
        .search-result-card {
            background: var(--bg-region);
            border: 1px solid #222233;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 10px;
            cursor: pointer;
            transition: all 0.2s ease;
        }
        
        .search-result-card:hover {
            border-color: var(--accent-cyan);
        }
        
        .search-result-type {
            font-size: 0.7rem;
            color: var(--accent-cyan);
            margin-bottom: 5px;
        }
        
        .search-result-title {
            font-size: 1rem;
            color: var(--text-primary);
        }
        
        .search-result-summary {
            font-size: 0.8rem;
            color: var(--text-secondary);
            margin-top: 5px;
        }
        
        .search-result-status {
            display: inline-block;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 0.7rem;
            margin-top: 5px;
        }
        
        .search-result-status.active { background: rgba(0, 212, 255, 0.2); color: var(--accent-cyan); }
        .search-result-status.completed { background: rgba(0, 255, 136, 0.2); color: var(--accent-green); }
        .search-result-status.blocked { background: rgba(255, 68, 68, 0.2); color: var(--accent-red); }
        
        .project-count {
            font-size: 0.8rem;
            color: var(--text-secondary);
            margin-top: 10px;
        }
        
        .section {
            margin-top: 40px;
        }
        
        .section-title {
            font-size: 1.2rem;
            font-weight: 500;
            color: var(--text-secondary);
            letter-spacing: 0.05em;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 1px solid #222233;
        }
        
        .regions {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 15px;
        }
        
        .region {
            background: var(--bg-region);
            padding: 20px;
            border-radius: 8px;
            border: 1px solid #222233;
            position: relative;
            overflow: hidden;
        }
        
        .region::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 3px;
            background: var(--accent-cyan);
        }
        
        .region-title {
            font-size: 1rem;
            font-weight: 500;
            margin-bottom: 10px;
        }
        
        .region-status {
            font-size: 0.7rem;
            color: var(--text-secondary);
        }
        
        .trail {
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        
        .trail-item {
            display: flex;
            align-items: center;
            gap: 15px;
            padding: 10px;
            background: var(--bg-region);
            border-radius: 4px;
        }
        
        .trail-marker {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: var(--accent-cyan);
        }
        
        .trail-content {
            flex: 1;
        }
        
        .trail-title {
            font-size: 0.9rem;
        }
        
        .trail-date {
            font-size: 0.7rem;
            color: var(--text-secondary);
        }
        
        .friction-zone {
            background: linear-gradient(135deg, var(--bg-region) 0%, #1a1a22 100%);
            padding: 15px;
            border-radius: 8px;
            border: 1px solid var(--accent-red);
            margin-bottom: 10px;
        }
        
        .friction-title {
            font-size: 0.9rem;
            color: var(--accent-red);
        }
        
        .friction-status {
            font-size: 0.7rem;
            color: var(--text-secondary);
            margin-top: 5px;
        }
        
        .path-hint {
            background: linear-gradient(90deg, #0a0a0f 0%, #1a1a2f 50%, #0a0a0f 100%);
            padding: 20px;
            border-radius: 8px;
            border: 1px solid var(--accent-green);
            text-align: center;
            margin-top: 40px;
        }
        
        .path-hint-text {
            font-size: 1rem;
            color: var(--accent-green);
        }
        
        .path-hint-label {
            font-size: 0.7rem;
            color: var(--text-secondary);
            margin-top: 10px;
        }
        
        .empty-state {
            text-align: center;
            padding: 60px 20px;
            color: var(--text-secondary);
        }
        
        .empty-state h2 {
            font-size: 1.5rem;
            color: var(--text-primary);
            margin-bottom: 20px;
        }
        
        .narrative-section {
            background: linear-gradient(135deg, var(--bg-region) 0%, #1a1a2f 100%);
            padding: 15px;
            border-radius: 8px;
            border: 1px solid #222233;
            margin-top: 15px;
        }
        
        .narrative-title {
            font-size: 0.8rem;
            color: var(--accent-cyan);
            margin-bottom: 10px;
        }
        
        .narrative-text {
            font-size: 0.9rem;
            color: var(--text-primary);
            line-height: 1.5;
        }
        
        .details-panel {
            position: fixed;
            right: -400px;
            top: 0;
            width: 400px;
            height: 100vh;
            background: var(--bg-dark);
            border-left: 1px solid #222233;
            transition: right 0.3s ease;
            padding: 20px;
            overflow-y: auto;
        }
        
        .details-panel.open {
            right: 0;
        }
        
        .details-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }
        
        .details-title {
            font-size: 1.2rem;
            color: var(--accent-cyan);
        }
        
        .details-close {
            background: none;
            border: none;
            color: var(--text-secondary);
            font-size: 1.5rem;
            cursor: pointer;
        }
        
        .details-content {
            color: var(--text-primary);
        }
        
        .details-field {
            margin-bottom: 15px;
        }
        
        .details-label {
            font-size: 0.8rem;
            color: var(--text-secondary);
        }
        
        .details-value {
            font-size: 1rem;
            margin-top: 5px;
        }
        
        .waypoint-clickable {
            cursor: pointer;
            transition: background 0.2s ease;
        }
        
        .waypoint-clickable:hover {
            background: rgba(0, 212, 255, 0.1);
        }
        
        .waypoint-recent {
            border: 1px solid var(--accent-cyan);
        }
        
        /* Motion Language - Map Metaphor Transitions */
        
        @keyframes approach {
            from { transform: translateX(100%) scale(0.9); opacity: 0; }
            to { transform: translateX(0) scale(1); opacity: 1; }
        }
        
        @keyframes depart {
            from { transform: translateX(0) scale(1); opacity: 1; }
            to { transform: translateX(100%) scale(0.9); opacity: 0; }
        }
        
        @keyframes waypoint-pulse {
            0%, 100% { box-shadow: 0 0 0 0 rgba(0, 212, 255, 0); }
            50% { box-shadow: 0 0 8px 2px rgba(0, 212, 255, 0.3); }
        }
        
        @keyframes discovery-reveal {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        @keyframes proximity-glow {
            0%, 100% { box-shadow: 0 0 0 rgba(0, 212, 255, 0); }
            50% { box-shadow: 0 0 12px rgba(0, 212, 255, 0.2); }
        }
        
        .details-panel {
            animation: approach 0.3s ease-out;
        }
        
        .details-panel.closing {
            animation: depart 0.2s ease-in forwards;
        }
        
        .waypoint-clickable:hover {
            animation: waypoint-pulse 1.5s ease-in-out infinite;
        }
        
        .search-result-card {
            animation: discovery-reveal 0.3s ease-out;
        }
        
        .search-result-card:nth-child(1) { animation-delay: 0s; }
        .search-result-card:nth-child(2) { animation-delay: 0.05s; }
        .search-result-card:nth-child(3) { animation-delay: 0.1s; }
        .search-result-card:nth-child(4) { animation-delay: 0.15s; }
        .search-result-card:nth-child(5) { animation-delay: 0.2s; }
        
        .region-item:hover {
            animation: proximity-glow 2s ease-in-out infinite;
            border-color: var(--accent-cyan);
        }
        
        .project-btn {
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        .project-btn:hover {
            transform: scale(1.05);
        }
        
        .terrain-region {
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        
        .terrain-region:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        }
        
        .related-section {
            background: linear-gradient(135deg, var(--bg-region) 0%, #1a1a2f 100%);
            padding: 15px;
            border-radius: 8px;
            border: 1px solid #222233;
            margin-top: 15px;
        }
        
        .related-title {
            font-size: 0.8rem;
            color: var(--accent-green);
            margin-bottom: 10px;
        }
        
        .related-text {
            font-size: 0.9rem;
            color: var(--text-secondary);
            line-height: 1.5;
        }
    </style>
</head>
<body>
    <div class="observatory">
        <div class="header">
            <h1>Project Observatory</h1>
            <div class="project-selector" id="project-selector"></div>
            <div class="project-count" id="project-count">Loading projects...</div>
            <div class="search-container">
                <input type="text" class="search-input" id="search-input" placeholder="Search artifacts...">
                <button class="search-btn" onclick="performSearch()">Search</button>
            </div>
            <div class="search-results" id="search-results"></div>
            <div class="pulse">
                <div class="pulse-item">
                    <div class="pulse-value pulse-active" id="active-count">-</div>
                    <div class="pulse-label">Active</div>
                </div>
                <div class="pulse-item">
                    <div class="pulse-value pulse-completed" id="completed-count">-</div>
                    <div class="pulse-label">Completed</div>
                </div>
                <div class="pulse-item">
                    <div class="pulse-value pulse-blocked" id="blocked-count">-</div>
                    <div class="pulse-label">Blocked</div>
                </div>
            </div>
        </div>
        
        <div class="section" id="regions-section">
            <div class="section-title">Active Regions</div>
            <div class="regions" id="regions"></div>
        </div>
        
        <div class="section" id="trail-section">
            <div class="section-title">Recent Movement</div>
            <div class="trail" id="trail"></div>
        </div>
        
        <div class="section" id="friction-section">
            <div class="section-title">Friction Zones</div>
            <div id="friction-zones"></div>
        </div>
        
        <div class="path-hint">
            <div class="path-hint-text" id="next-action">-</div>
            <div class="path-hint-label">Recommended Path</div>
        </div>
    </div>
    
    <div class="details-panel" id="details-panel">
        <div class="details-header">
            <div class="details-title" id="details-title">Artifact Details</div>
            <button class="details-close" onclick="closeDetails()">x</button>
        </div>
        <div class="details-content" id="details-content"></div>
    </div>
    
    <script>
        const repoPath = 'G:/Workspace/amazing-async-dev';
        let currentProjectId = null;
        let projects = [];
        
        async function loadProjects() {
            try {
                const res = await fetch(`/api/projects?repo_path=${encodeURIComponent(repoPath)}`);
                projects = await res.json();
                renderProjectSelector(projects);
                if (projects.length > 0) {
                    selectProject(projects[0].project_id);
                }
            } catch (e) {
                document.getElementById('project-count').textContent = 'Failed to load projects';
            }
        }
        
        function renderProjectSelector(projects) {
            const selector = document.getElementById('project-selector');
            selector.innerHTML = projects.map(p => `
                <button class="project-btn" data-project="${p.project_id}" onclick="selectProject('${p.project_id}')">
                    ${p.project_id} (${p.count})
                </button>
            `).join('');
            
            document.getElementById('project-count').textContent = `${projects.length} projects discovered`;
        }
        
        function selectProject(projectId) {
            currentProjectId = projectId;
            
            document.querySelectorAll('.project-btn').forEach(btn => {
                btn.classList.toggle('active', btn.dataset.project === projectId);
            });
            
            loadProjectState(projectId);
        }
        
        async function loadProjectState(projectId) {
            try {
                const res = await fetch(`/api/project/${projectId}?repo_path=${encodeURIComponent(repoPath)}`);
                const data = await res.json();
                renderObservatory(data);
            } catch (e) {
                renderEmpty();
            }
        }
        
        function renderObservatory(data) {
            document.getElementById('active-count').textContent = data.summary.active;
            document.getElementById('completed-count').textContent = data.summary.completed;
            document.getElementById('blocked-count').textContent = data.summary.blocked;
            
            const regionsEl = document.getElementById('regions');
            regionsEl.innerHTML = data.features.map(f => `
                <div class="region">
                    <div class="region-title">${f.title || f.id}</div>
                    <div class="region-status">${f.status || 'active'}</div>
                </div>
            `).join('');
            
            const trailEl = document.getElementById('trail');
            trailEl.innerHTML = data.recent_movement.map(r => `
                <div class="trail-item waypoint-clickable" onclick="showDetails('${r.id}', '${r.type}', '${r.date || ''}', '${r.title || ''}')">
                    <div class="trail-marker"></div>
                    <div class="trail-content">
                        <div class="trail-title">${r.title || r.id}</div>
                        <div class="trail-date">${r.date || ''} - ${r.type}</div>
                    </div>
                </div>
            `).join('');
            
            const frictionEl = document.getElementById('friction-zones');
            if (data.friction_zones.length > 0) {
                frictionEl.innerHTML = data.friction_zones.map(f => `
                    <div class="friction-zone">
                        <div class="friction-title">${f.title || f.id}</div>
                        <div class="friction-status">${f.status} - ${f.type}</div>
                    </div>
                `).join('');
            } else {
                frictionEl.innerHTML = '<div class="empty-state"><p>No friction zones detected</p></div>';
            }
            
            document.getElementById('next-action').textContent = data.next_action_hint;
        }
        
        function renderEmpty() {
            document.getElementById('regions').innerHTML = '<div class="empty-state"><h2>No Project Data</h2><p>Point to an async-dev repository to see project state</p></div>';
        }
        
        function showDetails(id, type, date, title) {
            const panel = document.getElementById('details-panel');
            const titleEl = document.getElementById('details-title');
            const contentEl = document.getElementById('details-content');
            
            panel.classList.remove('closing');
            
            titleEl.textContent = title || id;
            contentEl.innerHTML = `
                <div class="details-field">
                    <div class="details-label">ID</div>
                    <div class="details-value">${id}</div>
                </div>
                <div class="details-field">
                    <div class="details-label">Type</div>
                    <div class="details-value">${type}</div>
                </div>
                <div class="details-field">
                    <div class="details-label">Date</div>
                    <div class="details-value">${date || 'Unknown'}</div>
                </div>
                <div class="narrative-section">
                    <div class="narrative-title">Story Narrative</div>
                    <div class="narrative-text">Click a feature region to see its execution narrative.</div>
                </div>
                <div class="related-section">
                    <div class="related-title">Related Features</div>
                    <div class="related-text">Explore connected features in this territory.</div>
                </div>
            `;
            
            panel.classList.add('open');
        }
        
        function closeDetails() {
            const panel = document.getElementById('details-panel');
            panel.classList.add('closing');
            setTimeout(() => {
                panel.classList.remove('open');
                panel.classList.remove('closing');
            }, 200);
        }
        
        async function performSearch() {
            const query = document.getElementById('search-input').value;
            if (!query) {
                document.getElementById('search-results').innerHTML = '';
                return;
            }
            
            try {
                const res = await fetch(`/api/search?q=${encodeURIComponent(query)}&repo_path=${encodeURIComponent(repoPath)}`);
                const data = await res.json();
                
                const resultsEl = document.getElementById('search-results');
                if (data.results.length === 0) {
                    resultsEl.innerHTML = '<div class="empty-state"><p>No results found for "' + query + '"</p></div>';
                } else {
                    resultsEl.innerHTML = data.results.map(r => `
                        <div class="search-result-card" onclick="showDetails('${r.id}', '${r.type}', '${r.date || ''}', '${r.title || ''}')">
                            <div class="search-result-type">${r.type}</div>
                            <div class="search-result-title">${r.title || r.id}</div>
                            <div class="search-result-summary">${r.summary || ''}</div>
                            ${r.status ? `<div class="search-result-status ${r.status}">${r.status}</div>` : ''}
                        </div>
                    `).join('');
                }
            } catch (e) {
                document.getElementById('search-results').innerHTML = '<div class="empty-state"><p>Search failed</p></div>';
            }
        }
        
        document.getElementById('search-input').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') performSearch();
        });
        
        loadProjects();
    </script>
</body>
</html>
"""