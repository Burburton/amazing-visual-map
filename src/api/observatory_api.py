"""Observatory API - serves artifact data for frontend.

Feature 003: Observatory Home backend.
"""

from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

from src.scanner.repo_scanner import scan_repo
from src.model.artifact_model import normalize_artifacts, calculate_state_summary


app = FastAPI(title="Amazing Visual Map Observatory")


@app.get("/api/project/{project_id}")
async def get_project_state(project_id: str, repo_path: str = "."):
    """Get project state for observatory display."""
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


def derive_next_action(summary: dict, blocked: list) -> str:
    """Derive recommended next action from state."""
    if summary["blocked"] > 0:
        return f"Resolve {summary['blocked']} blocked items before continuing"
    
    if summary["active"] > 0:
        return f"Continue active work ({summary['active']} items in progress)"
    
    if summary["completed"] > 0:
        return "All items complete - ready for review or next phase"
    
    return "No active work found - start planning next feature"


@app.get("/", response_class=HTMLResponse)
async def observatory_home():
    """Serve observatory home page."""
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
    </style>
</head>
<body>
    <div class="observatory">
        <div class="header">
            <h1>Project Observatory</h1>
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
    
    <script>
        const projectId = 'amazing-async-dev';
        const repoPath = 'G:/Workspace/amazing-async-dev';
        
        async function loadObservatory() {
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
                <div class="trail-item">
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
        
        loadObservatory();
    </script>
</body>
</html>
"""